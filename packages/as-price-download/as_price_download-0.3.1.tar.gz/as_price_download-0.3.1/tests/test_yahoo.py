'''
Test Yahoo Finance API
'''

import pytest
from pricedl.model import SecuritySymbol
from pricedl.quotes.yahoo_finance_downloader import YahooFinanceDownloader


@pytest.mark.asyncio
async def test_dl():
    '''
    Test download.
    '''
    dl = YahooFinanceDownloader()
    symbol = SecuritySymbol("ASX", "VHY")
    actual = await dl.download(symbol, 'AUD')

    assert actual is not None
    assert actual.value > 0
    assert actual.currency == "AUD"
    assert actual.symbol.mnemonic == "VHY"
    assert actual.symbol.namespace == "ASX"
    assert actual.date is not None
