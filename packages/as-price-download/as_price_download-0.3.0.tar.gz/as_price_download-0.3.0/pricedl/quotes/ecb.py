'''
Price downloader for ECB data (currencies).
'''

import datetime
from decimal import ROUND_HALF_UP, Decimal
import os
from pathlib import Path
import tempfile
import eurofx

from loguru import logger
import pandas as pd

from pricedl.model import Price
from pricedl.quote import Downloader


class EcbDownloader(Downloader):
    '''
    Downloader for ECB data (currencies).
    '''

    async def download(self, security_symbol, currency):
        '''
        Download the price for the given symbol.
        '''
        currency = currency.upper()
        if not currency == 'EUR':
            raise ValueError("Only EUR is supported")
        symbol = security_symbol.mnemonic.upper()
        logger.debug(f"Downloading price for {symbol} in {currency}")

        # Check if we have cached daily rates file.
        if self.daily_cache_exists():
            cache_date = Path(self.get_cache_path()).name.split(".")[0]
            logger.debug(f"Using cached daily rates: {cache_date}")
            daily_df = self.read_daily_cache()
        else:
            daily_df = eurofx.get_daily_data_df()
            # cache it
            self.write_daily_cache(daily_df)

        # daily = eurofx.get_daily_data()
        # historical = eurofx.get_historical_data()
        # currencies = eurofx.get_currency_list()

        # historical_df = eurofx.get_historical_data_df()
        # currencies_df_ = eurofx.get_currency_list_df()

        df = daily_df
        # rate = df.at['2025-05-10', 'USD']
        rate = df.iloc[0][symbol]
        # The rates inverted. They are for 1 Euro (EUR/AUD).
        inv_rate = Decimal(1 / rate)
        inv_rate = inv_rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

        # date
        timestamp = df.index[0]
        if isinstance(timestamp, str):
            date = datetime.datetime.strptime(timestamp, '%Y-%m-%d').date()
        elif isinstance(timestamp, pd.Timestamp):
            date = timestamp.date()
        else:
            logger.debug(f"timestamp: {timestamp}, {type(timestamp).__name__}")
            raise ValueError("Unsupported timestamp type")

        return Price(symbol=security_symbol,
                     date=date, value=inv_rate,
                     currency=currency, source="ECB")

    def daily_cache_exists(self):
        '''
        Checks if the daily rates file exists.
        '''
        cache_path = self.get_cache_path()
        return os.path.exists(cache_path)

    def get_cache_path(self):
        '''
        Returns the path to the cache file.
        '''
        temp_dir = tempfile.gettempdir()
        filename = datetime.date.today().isoformat()
        # Change extension to change the format.
        extension = "csv"
        return os.path.join(temp_dir, f"{filename}.{extension}")

    def write_daily_cache(self, df: pd.DataFrame):
        '''
        Caches the daily rates.
        '''
        cache_path = self.get_cache_path()

        # support different formats
        if cache_path.endswith(".csv"):
            df.to_csv(cache_path, index=True)
        elif cache_path.endswith(".feather"):
            df.to_feather(cache_path)
        else:
            raise ValueError(f"Unsupported file format: {cache_path}")

    def read_daily_cache(self) -> pd.DataFrame:
        '''
        Reads the cached daily rates.
        '''
        cache_path = self.get_cache_path()

        logger.debug(f"Reading cached daily rates from {cache_path}")

        # support different formats
        if cache_path.endswith(".csv"):
            df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        elif cache_path.endswith(".feather"):
            df = pd.read_feather(cache_path)
        else:
            raise ValueError(f"Unsupported file format: {cache_path}")
        return df
