'''
Tests for yfinance downloader.
'''

def test_vanguard():
    '''test downloading vanguard fund prices from yahoo finance'''
    import pricedl.quotes.yfinance_downloader as dl
    symbol = 'VAN0104AU.AX'
    result = dl.show_info(symbol)

    assert result is not None

