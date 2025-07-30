"""
Downloader using yfinance package.
"""

from datetime import datetime
import yfinance as yf

from pricedl.model import Price, SecuritySymbol
from pricedl.quote import Downloader

yahoo_namespaces = {
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


class YfinanceDownloader(Downloader):
    """
    Downloader using yfinance package.
    """

    def __init__(self):
        # self.yf = yfinance.Ticker
        pass

    def get_yahoo_symbol(self, sec_symbol: SecuritySymbol) -> str:
        """Get the Yahoo Finance symbol for the given security symbol."""
        current_namespace = sec_symbol.namespace
        yahoo_namespace = current_namespace

        if current_namespace in yahoo_namespaces:
            yahoo_namespace = yahoo_namespaces[current_namespace]

        if yahoo_namespace:
            return f"{sec_symbol.mnemonic}.{yahoo_namespace}"
        else:
            return sec_symbol.mnemonic

    async def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        """Download price for the given security symbol."""
        yahoo_symbol = self.get_yahoo_symbol(security_symbol)

        ticker = yf.Ticker(yahoo_symbol)

        # price = self.get_price_from_history(ticker, security_symbol)
        # price = self.get_price_from_fastinfo(ticker, security_symbol)
        price = self.get_price_from_info(ticker, security_symbol)
        return price

    def get_price_from_history(
        self, ticker: yf.Ticker, security_symbol: SecuritySymbol
    ) -> Price:
        """
        Get price from history
        """
        # Get historical data (for the last 1 day to ensure you get the latest available)
        hist = ticker.history(period="1d")

        # Get the last date and the last price
        timestamp = hist.index[-1]
        dt = timestamp.date()

        value = hist["Close"].iloc[-1]

        # date = ticker.fast_info.get("lastTradeDate")
        # value = ticker.fast_info.get("lastPrice")
        currency = ticker.fast_info.get("currency")

        price = Price(
            symbol=security_symbol,
            date=dt,
            time=None,
            value=value,
            currency=currency,
            source="yfinance",
        )
        return price

    def get_price_from_fastinfo(
        self, ticker: yf.Ticker, security_symbol: SecuritySymbol
    ) -> Price:
        """
        Get price from quick info
        """
        # Get the last date and the last price
        date = ticker.fast_info.get("lastTradeDate")
        value = ticker.fast_info.get("lastPrice")
        currency = ticker.fast_info.get("currency")

        price = Price(
            symbol=security_symbol,
            date=date,
            time=None,
            value=value,
            currency=currency,
            source="yfinance",
        )
        return price

    def get_price_from_info(
        self, ticker: yf.Ticker, security_symbol: SecuritySymbol
    ) -> Price:
        """
        Get price from info
        """
        # Get the last date and the last price
        # date = ticker.info.get("lastTradeDate")
        ts = ticker.info.get("regularMarketTime")
        dt = datetime.fromtimestamp(ts)
        # gmt_offset = ticker.info.get("gmtOffSetMilliseconds")

        value = ticker.info.get("regularMarketPrice")
        currency = ticker.info.get("currency")

        price = Price(
            symbol=security_symbol,
            date=dt.date(),
            time=dt.time(),
            value=value,
            currency=currency,
            source="yfinance",
        )
        return price
