"""
Vanguard AU price downloader using the detail data.
https://www.vanguard.com.au/personal/api/products/personal/fund/8105/detail

Valid as of 2023-05.
As of 2023-10, the fund codes have changed.

The fund page is at
https://www.vanguard.com.au/personal/invest-with-us/fund?productType=managed+fund&portId=8105&tab=prices-and-distributions
but the prices are retrieved as JSON from
https://www.vanguard.com.au/personal/api/products/personal/fund/8105/prices?limit=-1
"""

import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, Tuple

import aiohttp

from pricedl.model import Price, SecuritySymbol
from pricedl.quote import Downloader


class VanguardAu3Downloader(Downloader):
    """Downloader for Vanguard mutual funds prices"""

    def __init__(self):
        self.funds_map: Dict[str, str] = {
            # "VANGUARD:BOND": "8123",
            # "VANGUARD:HINT": "8146",
            "VANGUARD:PROP": "8105",  # VAN0004AU
            "VANGUARD:HY": "8106",  # VAN0104AU
        }

    def get_url(self, symbol: SecuritySymbol) -> str:
        """Creates the URL for the fund"""
        sec_symbol_str = str(symbol)
        fund_id = self.funds_map.get(sec_symbol_str)
        if fund_id is None:
            raise ValueError(f"Fund ID not found for symbol: {sec_symbol_str}")

        result = f"https://www.vanguard.com.au/personal/api/products/personal/fund/{fund_id}/detail?limit=-1"
        # print(f"DEBUG: url: {result}") # Corresponds to log::debug!
        return result

    async def _dl_price(self, symbol: SecuritySymbol) -> Tuple[str, str, str]:
        """
        Returns the latest retail fund price.
        (date_str, price_str, currency_str)
        """
        url = self.get_url(symbol)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
                content = await response.text()

        content_json = json.loads(content)
        data = content_json["data"][0]

        prices = data["navPrices"]
        if not prices:
            raise ValueError(f"No price data found for symbol {symbol} at {url}")

        latest = prices[0]  # Assuming the first one is the latest

        date_str = latest[
            "asOfDate"
        ]  # No need to replace quotes, json.loads handles it
        price_str = str(latest["price"])  # Ensure it's a string for Decimal conversion
        currency_str = latest["currencyCode"]  # No need to replace quotes

        return date_str, price_str, currency_str

    async def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        # The `currency` parameter is not used, as the API returns the currency.
        # We'll keep it for interface consistency.
        if security_symbol.namespace.upper() != "VANGUARD":
            raise ValueError("Only Vanguard symbols are handled by this downloader!")

        date_str, price_str, currency_api = await self._dl_price(security_symbol)

        # Optionally, you could validate currency_api against the input `currency` if required.
        # For now, we use the currency from the API.

        return self._parse_price(date_str, price_str, currency_api)

    def _parse_price(self, date_str, price_str, currency_api) -> Price:
        """
        Parse price from the price strings.
        """
        # Parse date
        price_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        p = Price(
            symbol=SecuritySymbol("", ""),
            date=price_date,
            value=Decimal(price_str),
            currency=currency_api,
        )
        return p
