"""
Yahoo Finance downloader implementation.
"""

import logging
from datetime import datetime, timezone, timedelta
import requests
from typing import Dict
from decimal import Decimal

from ..model import Price, SecuritySymbol
from ..quote import Downloader


class YahooFinanceDownloader(Downloader):
    """YahooFinanceDownloader"""

    def __init__(self):
        self.url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        self.namespaces = {
            "AMS": "AS",
            "ASX": "AX",
            "BATS": "",
            "BVME": "MI",
            "FWB": "F",
            "LSE": "L",
            "NASDAQ": "",
            "NYSE": "",
            "NYSEARCA": "",
            "XETRA": "DE",
        }

    def assemble_url(self, symbol: SecuritySymbol) -> str:
        """Assemble the URL for the Yahoo Finance API request."""
        current_namespace = symbol.namespace
        local_namespace = current_namespace

        if current_namespace in self.namespaces:
            local_namespace = self.namespaces[current_namespace]

        url = f"{self.url}{symbol.mnemonic}"

        if local_namespace:
            url = f"{url}.{local_namespace}"

        return url

    def get_price_from_json(self, body: Dict) -> Price:
        """Extract the Price from JSON response."""
        chart = body.get("chart", {})
        error = chart.get("error")

        # Ensure that there is no error
        assert error is None, f"Error in Yahoo Finance response: {error}"

        meta = chart.get("result", [{}])[0].get("meta", {})
        assert meta, "No metadata found in Yahoo Finance response"

        # Price
        market_price = meta.get("regularMarketPrice")
        value = Decimal(str(market_price))

        # Currency
        currency = meta.get("currency")

        # Date and Time
        seconds = meta.get("regularMarketTime")
        offset = meta.get("gmtoffset", 0)

        # Create timezone with the offset
        tz = timezone(timedelta(seconds=offset))

        # Create datetime from timestamp
        dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
        # Apply the timezone offset
        dt = dt.astimezone(tz)

        # Set date and time
        d = dt.date()
        t = dt.time()

        result = Price(
            symbol=SecuritySymbol("", ""),
            date=d,
            time=t,
            value=value,
            currency=currency,
            source="yahoo",
        )

        return result

    def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        """Download price data from Yahoo Finance."""
        url = self.assemble_url(security_symbol)

        logging.debug("fetching from %s", url)

        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        headers = {"User-Agent": user_agent}

        response = requests.get(url, headers=headers, timeout=30)
        if not response.ok:
            print(f"Received a non-success status: {response}")
            response.raise_for_status()

        body = response.json()

        result = self.get_price_from_json(body)

        # Set the symbol
        result.symbol = security_symbol

        return result
