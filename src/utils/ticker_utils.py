import yfinance as yf

from src.utils.mappings import month_to_number, rofex_to_yf_tickers


def rofex_ticker_from_product_name(product: str) -> str:
    """
    :param product: expects a future product name (i.e. 'DLR/OCT23')
    :return: returns the underlying rofex name (i.e. 'DLR')
    """
    return product.split('/')[0]

def stock_ticker_from_prduct_name(product: str) -> str:
    """
    :param product: expects a future product name (i.e. 'DLR/OCT23')
    :return: returns the underlying yahoo finance name (i.e. 'ARS=X')
    """
    return rofex_to_yf_tickers[rofex_ticker_from_product_name(product)]

def expiration_date_str_from_product_name(product: str) -> str:
    """
    :param product: expects a future product name (i.e. 'DLR/OCT23')
    :return: returns the product_name expiration month and year as str (i.e. 'OCT23')
    """
    return product.split('/')[1]


def expiration_date_int_from_product_name(product: str) -> tuple[int, int]:
    """
    :param product: expects a future product name (i.e. 'DLR/OCT23')
    :return: return the expiration month and year as a tuple of ints (i.e. (10, 2023))
    """
    str_date = expiration_date_str_from_product_name(product)
    month = month_to_number[str_date[:3]]
    year = 2000 + int(str_date[3:])
    return month, year


def spot_market_data(rofex_ticker: str) -> dict:
    """
    :param rofex_ticker: expects the underlying rofex ticker name (i.e. 'DLR')
    :return: a dict with the bid price and size and the ask price and size
    NOTE: Although bid size and ask size are in the response they are always zero for the products used in this POC
    """
    ticker = rofex_to_yf_tickers[rofex_ticker]
    stock_info = yf.Ticker(ticker).info
    return {'bid' : {'price': stock_info['bid'], 'size':stock_info['bidSize']}, 'ask': {'price': stock_info['ask'], 'size':stock_info['askSize']}}