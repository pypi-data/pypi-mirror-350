"""
The price downloader that downloads the prices directly into the list.
"""

from pathlib import Path
from typing import List, Tuple
import csv
import asyncclick as click
from loguru import logger
from pricedl.config import PriceDbConfig
from pricedl.price_flat_file import PriceFlatFile, PriceRecord
from pricedl.quote import Quote
from .model import Price, SecurityFilter, SecuritySymbol, SymbolMetadata


def get_securities(
    symbols_path: Path, security_filter: SecurityFilter
) -> List[SymbolMetadata]:
    """
    Load symbols list, applying the filters.
    """
    symbols_list = load_symbols(symbols_path)
    logger.debug(f"Loaded {len(symbols_list)} symbols from {symbols_path}")

    # filter
    if security_filter is None:
        return symbols_list
    else:
        symbols_list = filter_securities(symbols_list, security_filter)

    logger.debug(f"Filtered to {len(symbols_list)} symbols")

    return symbols_list


def get_paths() -> Tuple[Path, Path]:
    """
    Get the paths to the symbols and prices files.
    """
    config = PriceDbConfig()

    if config.symbols_path is None:
        raise ValueError("Symbols path not set in config")
    if config.prices_path is None:
        raise ValueError("Prices path not set in config")

    symbols_path = Path(config.symbols_path)
    prices_path = Path(config.prices_path)

    if not symbols_path.exists():
        raise FileNotFoundError(f"Symbols file not found: {symbols_path}")
    if not prices_path.exists():
        raise FileNotFoundError(f"Prices file not found: {prices_path}")

    return symbols_path, prices_path


async def dl_quotes(security_filter: SecurityFilter):
    """
    Download directly into the price file in ledger format.
    Maintains the latest prices in the price file by updating the prices for
    existing symbols and adding any new ones.
    """
    symbols_path, prices_path = get_paths()
    logger.debug(f"Symbols path: {symbols_path}")
    logger.debug(f"Prices path: {prices_path}")

    # load the symbols table for mapping
    securities = get_securities(symbols_path, security_filter)

    # load prices file
    prices_file = PriceFlatFile.load(prices_path)

    # progress bar
    with click.progressbar(length=len(securities), label="Downloading prices") as bar:
        for sec in securities:
            logger.debug(f"Processing symbol: {sec.symbol}, {sec.updater_symbol}")
            # Use the Updater Symbol, if specified. This is provider-specific.
            mnemonic = sec.updater_symbol if sec.updater_symbol else sec.symbol
            symbol = SecuritySymbol(sec.namespace or "", mnemonic)
            logger.debug(f"Fetching price for symbol {symbol}")

            # todo update progress bar

            price = await download_price(
                symbol, currency=sec.currency, agent=sec.updater
            )
            logger.debug(f"Price: {price}")

            # Convert the price to ledger format record.
            price_record = PriceRecord.from_price_model(price)
            # Use ledger symbol.
            price_record.symbol = sec.ledger_symbol or sec.symbol

            # Appent to the price file. The symbol is used as the key.
            prices_file.prices[price_record.symbol] = price_record

            # Save the price file after every price fetch.
            prices_file.save()

            # update progress bar
            bar.update(1)


def filter_securities(securities_list, filter_val):
    """Filter securities based on the provided filter criteria"""
    result = []

    for sym in securities_list:
        # Filter by agent/updater
        if filter_val.agent is not None:
            if sym.updater is None or sym.updater != filter_val.agent:
                continue

        # Filter by currency
        if filter_val.currency is not None:
            if sym.currency is None or sym.currency != filter_val.currency.upper():
                continue

        # Filter by exchange/namespace
        if filter_val.exchange is not None:
            if sym.namespace is None or sym.namespace != filter_val.exchange.upper():
                continue

        # Filter by symbol
        if filter_val.symbol is not None:
            if sym.symbol != filter_val.symbol.upper():
                continue

        # If it passed all filters, add to result
        result.append(sym)

    return result


def load_symbols(symbols_path: Path):
    """
    Loads the symbols from the symbols file.
    """
    with open(symbols_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        symbols_list = [SymbolMetadata(**row) for row in reader]

    logger.debug(f"Loaded {len(symbols_list)} symbols from {symbols_path}")
    return symbols_list


async def download_price(
    symbol: SecuritySymbol, currency: str | None, agent: str | None = None
) -> Price:
    """
    Download the price for the given symbol.
    """
    dl = Quote()
    if agent:
        dl.set_source(agent)
    if currency:
        dl.set_currency(currency)

    prices = await dl.fetch(symbol.namespace, [symbol.mnemonic])

    # price = dl.download(symbol, currency, agent)
    if prices is None:
        raise LookupError(f"No price downloaded for {symbol}")

    return prices[0]
