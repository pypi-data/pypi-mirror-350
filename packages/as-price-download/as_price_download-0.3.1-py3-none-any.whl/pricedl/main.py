"""
Main entry point for the script executable.
"""

import importlib.metadata

import asyncclick as click
from loguru import logger
import dotenv

import pricedl.direct_dl
from pricedl.config import PriceDbConfig
from pricedl.model import SecurityFilter

dotenv.load_dotenv()


@click.group()
# @click.option("--debug/--no-debug", default=False, help="Enable debug logging")
def cli():
    """PriceDB - Retrieve, store, and export commodity prices in Ledger format."""
    # logger.level = logging.DEBUG
    # level = logging.DEBUG if debug else logging.INFO
    # logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    cfg = PriceDbConfig()
    logger.debug(f"Config file: {cfg.config_path}")


@cli.group("config")
def config_cmd():
    """Configuration commands."""


@config_cmd.command("show")
def config_show():
    """Show current configuration."""
    config = PriceDbConfig()
    click.echo(f"Configuration file: {config.config_path}")
    click.echo(f"Prices path: {config.prices_path}")

    # Show all config values
    for key, value in config.config_data.items():
        click.echo(f"{key}: {value}")


# @config_cmd.command("set")
# @click.argument("key")
# @click.argument("value")
# def config_set(key, value):
#     '''Set a configuration value.'''
#     config = PriceDbConfig()
#     config.set_value(key, value)
#     click.echo(f"Set {key} to {value}")


@cli.command("dl")
@click.option(
    "--exchange", "-x", default=None, help="Exchange for the securities to update"
)
@click.option(
    "--symbol", "-s", default=None, help="Symbol to download (NAMESPACE:MNEMONIC)"
)
@click.option("--currency", "-c", default=None, help="Currency for the price")
@click.option("--agent", "-a", default=None, help="Agent for the price")
@click.option("--file", "-f", default=None, help="Path to CSV file with symbols")
async def download(exchange, symbol, currency, agent, file):
    """Download prices for symbols."""
    if currency:
        currency = currency.strip()
        currency = currency.upper()

    sec_filter = SecurityFilter(currency, agent, exchange, symbol)
    logger.debug(f"Filter: {sec_filter}")
    await pricedl.direct_dl.dl_quotes(sec_filter)


def get_version():
    """Identifies the package version"""
    try:
        version = importlib.metadata.version("pricedb-python")
    except importlib.metadata.PackageNotFoundError:
        version = None
    return version


def main():
    """
    Entry point for the `pricedb` utility.
    """
    version = get_version()
    print(f"PriceDb v{version}")

    cli()


if __name__ == "__main__":
    main()
