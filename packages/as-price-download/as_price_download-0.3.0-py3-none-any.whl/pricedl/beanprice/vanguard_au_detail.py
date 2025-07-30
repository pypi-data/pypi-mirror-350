"""
Bean-price-compatible price downloader for Vanguard Australia.

Use:

    uv run bean-price -e "AUD:as-price-download.vanguard_au_detail/HY"
"""

import asyncio
from datetime import datetime

from beanprice import source
from loguru import logger

from pricedl.model import SecuritySymbol
from pricedl.quotes.vanguard_au_2023_detail import VanguardAu3Downloader


class Source(source.Source):
    """
    Vanguard Australia price source
    ticker: HY
    """

    def get_latest_price(self, ticker) -> source.SourcePrice | None:
        try:
            symbol = ticker

            sec_symbol = SecuritySymbol("VANGUARD", symbol)
            v_price = asyncio.run(VanguardAu3Downloader().download(sec_symbol, ""))

            price = v_price.value

            min_time = datetime.min.time()
            time = datetime.combine(v_price.date, min_time)
            # The datetime must be timezone aware.
            time = time.astimezone()

            quote_currency = v_price.currency

            return source.SourcePrice(price, time, quote_currency)
        except Exception as e:
            logger.error(e)
            return None

    def get_historical_price(self, ticker, time):
        # return VanguardAu3Downloader().get_historical_price(ticker, time)
        pass
