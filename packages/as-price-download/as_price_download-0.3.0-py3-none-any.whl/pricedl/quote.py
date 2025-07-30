"""
Quote implementation in Python.
Fetching prices.

Based on [Price Database](https://gitlab.com/alensiljak/price-database),
Python library.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from loguru import logger


from .model import Price, SecuritySymbol


class Downloader(ABC):
    """Base class for all the downloaders."""

    @abstractmethod
    async def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        """Download price for the given security symbol and currency."""
        pass


class Quote:
    """
    The price downloading facade.
    """

    def __init__(self):
        self.symbol: str | None = None
        self.exchange: str | None = None
        self.source: Optional[str] = None
        self.currency: Optional[str] = None

    async def fetch(self, exchange: str, symbols: List[str]) -> List[Price]:
        """Fetch prices for the given symbols."""
        result = []

        for symbol in symbols:
            # logging.debug(f"Downloading price for {symbol}")
            sec_sym = SecuritySymbol(exchange, symbol)

            price = await self.download(sec_sym)
            if price:
                result.append(price)

        return result

    async def download(self, security_symbol: SecuritySymbol) -> Optional[Price]:
        """Download price for the given security symbol."""
        if self.currency is not None:
            currency_val = self.currency
            if currency_val != currency_val.upper():
                raise ValueError("currency must be uppercase!")

        downloader = self.get_downloader()
        currency: str = self.currency or "EUR"

        logger.debug(
            f"Calling download with symbol {security_symbol} and currency {currency}"
        )

        try:
            price = await downloader.download(security_symbol, currency)
            price.source = self.source or ""

            # Set the symbol here.
            #price.symbol = security_symbol
            return price
        except Exception as error:
            raise ConnectionError(f"Error downloading price: {error}") from error

    def get_downloader(self) -> Downloader:
        """Get the appropriate downloader based on the source."""
        source = self.source.lower() if self.source else None

        if source == "yahoo_finance":
            logging.debug("using yahoo finance")
            # return YahooFinanceDownloader()
            raise NotImplementedError("not implemented")
        elif source == "yfinance":
            logging.debug("using yfinance")
            from .quotes.yfinance import YfinanceDownloader

            return YfinanceDownloader()
        elif source == "ecb":
            logging.debug("using ecb")
            from .quotes.ecb import EcbDownloader

            return EcbDownloader()
        elif source == "fixerio":
            logging.debug("using fixerio")
            from .quotes.fixerio import Fixerio

            return Fixerio()
        elif source == "vanguard_au":
            logging.debug("using vanguard")
            from .quotes.vanguard_au_2023_detail import VanguardAu3Downloader

            return VanguardAu3Downloader()
        else:
            raise ValueError(f"unknown downloader: {source}")

    def set_currency(self, currency: str):
        """Set the currency for price fetching."""
        self.currency = currency.upper()

    def set_source(self, source: str):
        """Set the source for price fetching."""
        self.source = source
