'''
Use yfinance to download stock data from Yahoo Finance
'''
import argparse
import yfinance as yf
from loguru import logger


def get_data(ticker):
    ''' get data for a single ticker i.e. MSFT '''
    dat = yf.Ticker(ticker)
    return dat.info

def dl_historical_prices(ticker, start, end):
    ''' download historical prices for a ticker
    i.e. AAPL, start='2022-01-01', end='2023-01-01'
    '''
    data = yf.download(ticker, start, end)
    return data

def get_latest_price(ticker):
    ''' get latest price for a ticker '''
    data = yf.Ticker(ticker)
    return data.info['regularMarketPrice']

def show_quick_info(ticker):
    ''' show quick info for a ticker '''
    data = yf.Ticker(ticker)

    print(data.fast_info)
    #print(data.info)
    # print(data.fast_info.get('regularMarketPrice'))
    # print(data.fast_info.get('previousClose'))
    # print(data.fast_info.get('regularMarketPreviousClose'))
    print(data.fast_info.get('lastPrice'))
    print(data.fast_info.get('currency'))
    print(data.fast_info.get('timezone'))

def get_price(ticker):
    ''' show info for a ticker '''
    data = yf.Ticker(ticker)

    market_price = data.fast_info.get('regularMarketPrice')
    current_price = data.info['currentPrice']
    currency = data.info['currency']

    result = f'{market_price} / {current_price} {currency}'
    return result

def show_info(ticker):
    ''' show info for a ticker '''
    data = yf.Ticker(ticker)

    print(data.info)
    print(data.info.get('regularMarketPrice'))

    return data.info

def get_requested_symbol():
    '''get symbol from the CLI'''
    argparser = argparse.ArgumentParser(description='Get stock price')
    argparser.add_argument('symbol', help='Stock symbol')
    args = argparser.parse_args()
    return args.symbol

def main():
    ''' dev test'''
    symbol = get_requested_symbol()
    symbol = symbol.upper()
    logger.info(f'Getting price for {symbol}')

    show_info(symbol)
    #show_vg_fund()
    #show_quick_info(symbol)

if __name__ == '__main__':
    # print(get_latest_price('OPI'))
    main()
