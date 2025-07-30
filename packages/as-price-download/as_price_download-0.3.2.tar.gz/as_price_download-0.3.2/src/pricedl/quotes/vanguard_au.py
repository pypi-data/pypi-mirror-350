"""
Vanguard AU price downloader.
Deprecated as of 2023-04.
"""

import json
from loguru import logger
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional

import requests

# --- Model classes (equivalent to crate::model) ---


class SecuritySymbol:
    """
    Represents a security symbol with a namespace and mnemonic.
    """

    def __init__(self, full_symbol: str):
        if ":" not in full_symbol:
            raise ValueError(
                f"Invalid symbol format: '{full_symbol}'. Expected 'NAMESPACE:MNEMONIC'."
            )
        self.namespace, self.mnemonic = full_symbol.split(":", 1)

    def __str__(self) -> str:
        return f"{self.namespace.upper()}:{self.mnemonic.upper()}"

    def __repr__(self) -> str:
        return f"SecuritySymbol('{str(self)}')"


@dataclass
class Price:
    """
    Represents the price of a security on a specific date.
    """

    symbol: Optional[SecuritySymbol] = None
    date: Optional[str] = None  # YYYY-MM-DD
    value: int = 0  # Price * 10^scale (mantissa)
    denom: int = 1  # 10^scale
    currency: str | None = None

    def __repr__(self) -> str:
        return (
            f"Price(symbol={self.symbol!r}, date='{self.date}', "
            f"value={self.value}, denom={self.denom}, currency='{self.currency}')"
        )


# --- FundInfo data structure ---


@dataclass
class FundInfo:
    """
    Holds extracted information for a fund before parsing into a Price object.
    """

    name: str = ""
    identifier: str = ""
    date: str = ""  # Raw date string, e.g., "27 Apr 2023"
    value: str = ""  # Raw price string, e.g., "$1.2345"
    mstar_id: str = ""


# --- Downloader implementation ---


class VanguardAuDownloader:
    """
    Downloader for Vanguard Australia fund prices.
    Note: This API was deprecated as of April 2023.
    """

    _FUNDS_MAP: Dict[str, str] = {
        "VANGUARD:BOND": "8123",
        "VANGUARD:HINT": "8146",
        "VANGUARD:PROP": "8147",
        "VANGUARD:HY": "8148",
    }
    _API_URL = "https://api.vanguard.com/rs/gre/gra/1.7.0/datasets/auw-retail-listview-data.jsonp"

    def __init__(self):
        # The funds map is static, initialized above.
        pass

    def _dl_fund_data(self) -> Dict[str, Any]:
        """
        Fetches retail fund prices data from the Vanguard API.
        Returns the parsed 'fundData' dictionary.
        """
        logger.debug(f"Fetching fund data from {self._API_URL}")
        response = requests.get(self._API_URL, timeout=30)
        response.raise_for_status()  # Will raise an exception for 4XX/5XX status
        content = response.text

        # Clean-up the JSONP response
        if content.startswith("callback(") and content.endswith(")"):
            logger.debug("Cleaning up JSONP callback wrapper.")
            json_str = content[9:-1]  # Remove "callback(" and ")"
        else:
            json_str = content

        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            raise ValueError(f"Invalid JSON response: {e}") from e

        if "fundData" not in parsed_json:
            logger.error("'fundData' not found in JSON response.")
            raise ValueError("'fundData' key missing from API response")

        return parsed_json["fundData"]

    def _get_fund_info(self, fund_data: Dict[str, Any], fund_id: str) -> FundInfo:
        """
        Extracts specific fund information from the provided data dictionary.
        """
        if fund_id not in fund_data:
            raise KeyError(f"Fund ID '{fund_id}' not found in fund data.")

        info_json = fund_data[fund_id]
        # logging.debug(f"Raw info for fund_id {fund_id}: {info_json}")

        try:
            return FundInfo(
                name=info_json["name"],
                identifier=info_json["identifier"],
                date=info_json["asOfDate"],  # e.g., "28 Apr 2023"
                value=info_json["navPrice"],  # e.g., "$1.2345"
                mstar_id=info_json["mStarID"],
            )
        except KeyError as e:
            logger.error(f"Missing expected key in fund info for {fund_id}: {e}")
            raise ValueError(
                f"Data for fund {fund_id} is incomplete: missing {e}"
            ) from e

    def _parse_price(self, fund_info: FundInfo) -> Price:
        """
        Parses FundInfo into a Price object.
        """
        price = Price()

        # Parse date: "28 Apr 2023" -> "YYYY-MM-DD"
        try:
            date_obj = datetime.strptime(fund_info.date, "%d %b %Y").date()
            price.date = date_obj.isoformat()
        except ValueError as e:
            logger.error(f"Failed to parse date string '{fund_info.date}': {e}")
            raise ValueError(f"Invalid date format '{fund_info.date}'") from e

        # Parse value: "$1.2345" -> mantissa and denominator
        value_str = fund_info.value.lstrip("$")
        try:
            decimal_val = Decimal(value_str)
        except InvalidOperation as e:
            logger.error(f"Failed to parse decimal value '{value_str}': {e}")
            raise ValueError(f"Invalid price value format '{value_str}'") from e

        # sign, digits_tuple, exponent = decimal_val.as_tuple()

        # if (
        #     not digits_tuple and exponent == 0 and decimal_val.is_zero()
        # ):  # Handles Decimal('0')
        #     mantissa_int = 0
        # else:
        #     mantissa_str = "".join(map(str, digits_tuple))
        #     mantissa_int = int(mantissa_str)

        # if sign:
        #     mantissa_int = -mantissa_int

        # price.value = mantissa_int

        # if exponent < 0:
        #     price.denom = 10 ** abs(exponent)
        # elif exponent > 0:  # e.g. Decimal('123E2') -> (0, (1,2,3), 2). Value is 12300.
        #     # Mantissa should be 12300, denom 1.
        #     price.value = mantissa_int * (10**exponent)
        #     price.denom = 1
        # else:  # exponent == 0
        #     price.denom = 1

        price.value = decimal_val
        
        price.currency = "AUD"  # Hardcoded as in the original Rust code

        return price

    def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        """
        Downloads and parses the price for the given security symbol.
        The 'currency' parameter is for interface consistency but not used by this specific downloader.
        """
        if security_symbol.namespace.upper() != "VANGUARD":
            raise ValueError(
                f"Only Vanguard symbols are handled by this downloader. Got: {security_symbol}"
            )

        symbol_str = str(security_symbol)
        if symbol_str not in self._FUNDS_MAP:
            raise ValueError(
                f"Symbol '{symbol_str}' not found in Vanguard AU funds map."
            )

        fund_id = self._FUNDS_MAP[symbol_str]
        logger.debug(f"Symbol '{symbol_str}' maps to fund_id '{fund_id}'")

        fund_data_dict = self._dl_fund_data()

        # logging.debug(f"Full fund data dict: {fund_data_dict}")

        fund_info = self._get_fund_info(fund_data_dict, fund_id)
        logger.debug(f"Extracted fund info: {fund_info}")

        parsed_price = self._parse_price(fund_info)
        parsed_price.symbol = security_symbol  # Assign the symbol to the price object

        logger.debug(f"Parsed price: {parsed_price}")
        return parsed_price


def main_test():
    """
    Example usage and test for the VanguardAuDownloader.
    """
    downloader = VanguardAuDownloader()

    # Test with a known symbol
    # Use VANGUARD:HY as in the original commented-out test
    test_symbol_str = "VANGUARD:HY"
    try:
        symbol = SecuritySymbol(test_symbol_str)
        print(f"\nAttempting to download price for: {symbol}")
        # The currency "AUD" is passed but not actively used by this downloader's logic
        # as the API provides AUD prices.
        price = downloader.download(symbol, "AUD")

        print(f"\nSuccessfully downloaded price for {symbol}:")
        print(f"  Date: {price.date}")
        print(f"  Value: {price.value}")
        # print(f"  Actual Price: {Decimal(price.value) / Decimal(price.denom)}")
        print(f"  Currency: {price.currency}")
        print(f"  Full Price Object: {price!r}")

        assert price.currency == "AUD", f"Expected AUD, got {price.currency}"
        assert price.value != 0 or price.denom != 0, (
            "Price value or denom should not be zero (unless actual price is 0)"
        )
        assert price.symbol == symbol
        print("\nTest assertions passed for VANGUARD:HY.")

    except ValueError as ve:
        print(f"\nConfiguration or data error for {test_symbol_str}: {ve}")
        logger.error(f"ValueError for {test_symbol_str}: {ve}", exc_info=True)
    except requests.ConnectionError as ce:
        print(f"\nNetwork or API error for {test_symbol_str}: {ce}")
        logger.error(f"ClientError for {test_symbol_str}: {ce}", exc_info=True)
    except Exception as e:
        print(f"\nAn unexpected error occurred for {test_symbol_str}: {e}")
        logger.error(f"Unexpected error for {test_symbol_str}: {e}", exc_info=True)

    # Test with a symbol not in the map
    unknown_symbol_str = "VANGUARD:UNKNOWN"
    try:
        symbol_unknown = SecuritySymbol(unknown_symbol_str)
        print(f"\nAttempting to download price for unknown symbol: {symbol_unknown}")
        downloader.download(symbol_unknown, "AUD")
    except ValueError as e:
        print(f"Correctly failed for unknown symbol '{unknown_symbol_str}': {e}")
    except Exception as e:
        print(f"Unexpected error for unknown symbol '{unknown_symbol_str}': {e}")

    # Test with a non-Vanguard symbol
    invalid_namespace_str = "OTHER:XYZ"
    try:
        symbol_invalid_ns = SecuritySymbol(invalid_namespace_str)
        print(
            f"\nAttempting to download price for invalid namespace: {symbol_invalid_ns}"
        )
        downloader.download(symbol_invalid_ns, "AUD")
    except ValueError as e:
        print(f"Correctly failed for invalid namespace '{invalid_namespace_str}': {e}")
    except Exception as e:
        print(f"Unexpected error for invalid namespace '{invalid_namespace_str}': {e}")


if __name__ == "__main__":
    main_test()
