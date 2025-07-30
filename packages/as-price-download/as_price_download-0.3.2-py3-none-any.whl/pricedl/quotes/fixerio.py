# fixerio_translated.py

import asyncio
import json
import os
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

import requests

from pricedl.model import Price, SecuritySymbol
from pricedl.quote import Downloader

# --- Global Constants ---
APP_NAME = "pricedb-py"  # Adapted for Python version


def get_fixerio_api_key() -> str:
    """Loads Fixerio API key from the environment variable."""
    api_key = os.getenv("FIXERIO_API_KEY")
    if not api_key:
        logger.error("FIXERIO_API_KEY environment variable not set.")
        raise ValueError("FIXERIO_API_KEY environment variable not set.")
    if len(api_key) != 32:  # Original Rust test checks for length 32
        logger.warning(f"FIXERIO_API_KEY length is not 32. Key: '{api_key[:4]}...'")
    return api_key


def get_cache_dir() -> Path:
    """Gets the application-specific cache directory within the system's temp directory."""
    cache_base_path = Path(tempfile.gettempdir()) / APP_NAME.lower() / "fixerio_cache"
    cache_base_path.mkdir(parents=True, exist_ok=True)
    return cache_base_path


def get_rate_file_path(date_iso_str: str) -> Path:
    """Assembles the full file path for the given date string."""
    cache_path = get_cache_dir()
    filename = f"fixerio_{date_iso_str}.json"
    return cache_path / filename


def get_todays_file_path() -> Path:
    """Gets the cache file path for today's rates."""
    today_str = date.today().strftime("%Y-%m-%d")
    return get_rate_file_path(today_str)


def map_rates_to_price(rates_json: Dict[str, Any], target_symbol: str) -> Price:
    """
    Maps the JSON rates data from Fixer.io to a Price object.
    'target_symbol' is the currency for which we want the price (e.g., "AUD").
    The price will be relative to the base currency specified in rates_json["base"].
    """
    try:
        date_str = rates_json["date"]
        base_currency = rates_json["base"].upper()
        rates_dict = rates_json["rates"]
    except KeyError as e:
        logger.error(f"Rates JSON is missing expected field: {e}. Data: {rates_json}")
        raise ValueError(f"Invalid rates JSON structure: missing {e}") from e

    rate_value_for_target = rates_dict.get(target_symbol.upper())

    if rate_value_for_target is None:
        logger.error(
            f"Target symbol '{target_symbol.upper()}' not found in rates for base '{base_currency}'. Available: {list(rates_dict.keys())}"
        )
        raise KeyError(
            f"Symbol '{target_symbol.upper()}' not found in rates for base '{base_currency}'"
        )

    try:
        value_decimal = Decimal(str(rate_value_for_target))
    except Exception as e:
        logger.error(
            f"Could not convert rate '{rate_value_for_target}' to Decimal for {target_symbol}: {e}"
        )
        raise ValueError(f"Invalid rate value for {target_symbol}") from e

    if value_decimal.is_zero():
        logger.error(
            f"Rate for symbol '{target_symbol}' against base '{base_currency}' is zero, cannot invert."
        )
        raise ValueError("Rate is zero, cannot calculate inverse price.")

    inverse_rate = Decimal(1) / value_decimal
    logger.debug(f"Inverse rate for {target_symbol}/{base_currency}: {inverse_rate}")

    rounded_str_py = f"{inverse_rate:.6f}"
    final_decimal_for_price = Decimal(rounded_str_py)

    logger.debug(
        f"Rounded rate for {target_symbol}/{base_currency} (6dp): {final_decimal_for_price}"
    )

    sign, digits_tuple, exponent_int = final_decimal_for_price.as_tuple()

    if sign:
        logger.error(
            f"Negative price encountered for {target_symbol}/{base_currency} after inversion and rounding."
        )
        raise ValueError("Negative price encountered, which is not expected.")

    val_mantissa = 0
    if digits_tuple:
        val_mantissa = int("".join(map(str, digits_tuple)))

    val_scale = 0
    if isinstance(exponent_int, int):
        if exponent_int < 0:
            val_scale = -exponent_int
    else:
        logger.error(
            "Unexpected exponent type for Decimal %s: %s",
            final_decimal_for_price,
            exponent_int,
        )
        raise ValueError(f"Unexpected exponent type for Decimal: {exponent_int}")

    val_denom = 10**val_scale

    symbol = SecuritySymbol("CURRENCY", f"{target_symbol.upper()}")
    return Price(
        symbol=symbol,
        date=date_str,
        time=None,
        # value=val_mantissa,
        # denom=val_denom,
        currency=base_currency,
    )


def read_rates_from_cache() -> Dict[str, Any]:
    """Reads rates JSON from today's cache file."""
    file_path = get_todays_file_path()
    logger.debug(f"Loading rates from cache file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return json.loads(content)
    except FileNotFoundError:
        logger.warning(f"Cache file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing rates JSON from {file_path}: {e}")
        raise
    except IOError as e:
        logger.error(f"Error reading rates file {file_path}: {e}")
        raise


# --- Fixerio Class (Downloader Implementation) ---


class Fixerio(Downloader):
    """
    Downloader for currency exchange rates from Fixer.io.
    Implements caching of daily rates.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_fixerio_api_key()
        self.base_url = "http://data.fixer.io/api/latest"

    def _cache_rates(self, rates: Dict[str, Any]):
        """Saves the retrieved rates into a cache file."""
        try:
            file_date = rates["date"]
        except KeyError:
            logger.error("Rates JSON missing 'date' field, cannot cache.")
            raise ValueError("Rates JSON missing 'date' field for caching.")

        file_path = get_rate_file_path(file_date)
        content = json.dumps(rates, indent=2)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Successfully cached rates for {file_date} to {file_path}")
        except IOError as e:
            logger.error(f"Could not cache rates to {file_path}: {e}")
            raise IOError(f"Could not cache rates to {file_path}") from e

    def _download_rates_from_api(self, base_currency_api: str) -> Dict[str, Any]:
        """
        Downloads the latest rates from Fixer.io API.
        base_currency_api: The base currency for the API request (e.g., "EUR").
        """
        params = {"access_key": self.api_key, "base": base_currency_api.upper()}

        url = self.base_url

        logger.info(f"Downloading rates from Fixer.io: URL={url}, Params={params}")
        try:
            response = requests.get(url, params=params, timeout=15)
            logger.debug(f"Request URL: {response.url}")
            response.raise_for_status()
            result_json = response.json()

            if not result_json.get("success", False):
                error_info = result_json.get("error", {})
                err_msg = (
                    f"Fixer.io API error: Code {error_info.get('code')}, "
                    f"Type: {error_info.get('type')}, Info: {error_info.get('info')}"
                )
                logger.error(err_msg)
                raise ValueError(err_msg)

            logger.debug(f"Successfully downloaded rates: {result_json}")
            return result_json
        except requests.ConnectionError as e:
            logger.error(e)
            raise ConnectionError() from e
        except requests.RequestException as e:
            logger.error(e)
            raise requests.RequestException(f"Error retrieving quotes: {e}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from {url}: {e}")
            raise ValueError(f"Error decoding JSON response: {e}") from e

    def _latest_rates_cached_and_valid(
        self, requested_base_currency: str
    ) -> Optional[Dict[str, Any]]:
        """
        Checks if today's rates are cached and if the cached base currency matches.
        Returns the cached data if valid, otherwise None.
        """
        file_path = get_todays_file_path()
        if file_path.exists():
            logger.debug(f"Cache file exists for today: {file_path}")
            try:
                cached_data = read_rates_from_cache()
                cached_base = cached_data.get("base", "").upper()
                if cached_base == requested_base_currency.upper():
                    logger.info(
                        f"Using valid cached rates for base {requested_base_currency}."
                    )
                    return cached_data
                else:
                    logger.warning(
                        f"Cached rates base '{cached_base}' does not match requested base "
                        f"'{requested_base_currency.upper()}'. Will re-download."
                    )
                    return None
            except Exception as e:
                logger.warning(
                    f"Failed to read or validate cache file {file_path} ({e}). Will re-download."
                )
                return None
        logger.debug(f"Cache file for today does not exist: {file_path}")
        return None

    def download(
        self, security_symbol: SecuritySymbol, request_base_currency: str
    ) -> Price:
        """
        Download latest rates for the target currency specified in security_symbol,
        relative to the request_base_currency.
        Caches the (daily) prices.
        """
        target_mnemonic = security_symbol.mnemonic.upper()
        api_base_param = request_base_currency.upper()

        if ":" in target_mnemonic:
            err_msg = (
                f"SecuritySymbol mnemonic '{target_mnemonic}' should not contain ':'."
            )
            logger.error(err_msg)
            raise ValueError(err_msg)

        rates_json: Optional[Dict[str, Any]] = None

        cached_data = self._latest_rates_cached_and_valid(api_base_param)
        if cached_data:
            rates_json = cached_data
        else:
            logger.info(
                f"No valid cache for base '{api_base_param}', downloading new rates from API."
            )
            try:
                rates_json = self._download_rates_from_api(api_base_param)
                self._cache_rates(rates_json)
            except Exception as e:
                logger.error(f"Failed to download or cache rates: {e}")
                raise

        if not rates_json:
            crit_msg = "Failed to obtain rates data from cache or API."
            logger.critical(crit_msg)
            raise RuntimeError(crit_msg)

        logger.debug(
            f"Mapping rates for target '{target_mnemonic}' using data with base '{rates_json.get('base')}'"
        )

        price_object = map_rates_to_price(rates_json, target_mnemonic)

        return price_object


# --- Example Usage (Optional) ---
async def main_example():
    """Example of how to use the Fixerio class."""
    logger.info("Starting Fixerio example...")

    # Ensure API key is set before initializing Fixerio or running example
    if not os.getenv("FIXERIO_API_KEY"):
        logger.error("FIXERIO_API_KEY not set. Skipping live API call example.")
        print("Please set the FIXERIO_API_KEY environment variable to run the example.")
        return

    fixerio_downloader = Fixerio()

    eur_base = "EUR"
    symbols_to_test = [
        SecuritySymbol("CURRENCY", "USD"),
        SecuritySymbol("CURRENCY", "GBP"),
        SecuritySymbol("CURRENCY", "AUD"),
    ]

    for symbol in symbols_to_test:
        try:
            logger.info(
                "--- Attempting to download price for %s against base %s ---",
                symbol.mnemonic,
                eur_base,
            )
            price = fixerio_downloader.download(symbol, eur_base)
            price_decimal = price.value
            print(
                f"Price for {symbol.mnemonic}: {price_decimal:.6f} {price.currency} "
                f"(Date: {price.date}, Raw: val={price.value})"
            )
        except Exception as e:
            print(f"Error downloading price for {symbol.mnemonic}: {e}")
            logger.error("Detailed error for %s: ", symbol.mnemonic, exc_info=True)
        print("-" * 20)


if __name__ == "__main__":
    # To run the example:
    # 2. Set the FIXERIO_API_KEY environment variable.

    if os.getenv("FIXERIO_API_KEY"):
        asyncio.run(main_example())
    else:
        print("FIXERIO_API_KEY environment variable is not set.")
        print(
            "The Fixerio class and its methods are defined, but the example usage requires an API key."
        )
