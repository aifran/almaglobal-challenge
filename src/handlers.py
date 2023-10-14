import datetime

from src.services import ImplicitRateService, ProductService, ArbitrageRateService
from src.utils.date_utils import expiration_date
from src.utils.ticker_utils import rofex_ticker_from_product_name, expiration_date_int_from_product_name, spot_market_data

from copy import deepcopy

market_data_state = dict()


class ProductMarketDataHandler:
    """
    Handler class that is a layer between the market data message response and this repository
    """

    def __init__(self, message):
        self.message = message
        self.rate_service = ImplicitRateService(self)

    @property
    def product_name(self) -> str:
        """
        :return: The product_name name (i.e. 'DLR/OCT23')
        """
        return self.message["instrumentId"]["symbol"]

    @property
    def rofex_ticker(self) -> str:
        """
        :return: The rofex underlying name (i.e. 'DLR')
        """
        return rofex_ticker_from_product_name(self.product_name)

    @property
    def expiration_date(self) -> datetime.date:
        """
        :return: The expiration date of the product_name
        """
        expiration_month, expiration_year = expiration_date_int_from_product_name(self.product_name)
        return expiration_date(year=expiration_year, month=expiration_month)

    @property
    def product_market_data(self) -> dict:
        """
        :return: The bid price and size and the ask price and size of the product_name
        """
        _market_data = self.message['marketData']
        bid = _market_data['BI']
        ask = _market_data['OF']

        return {'bid': {'price': bid[0]['price'] if bid else None, 'size': bid[0]['size'] if bid else None},
                'ask': {'price': ask[0]['price'] if ask else None, 'size': ask[0]['size'] if ask else None}}

    @property
    def spot_market_data(self) -> dict:
        """
        :return: a dict with the bid price and size and the ask price and size
        NOTE: Although bid size and ask size are in the response they are always zero for the products used in this POC
        """
        return spot_market_data(self.rofex_ticker)

    @property
    def time(self):
        """
        The time of the sent message by the rofex API
        :return:
        """
        return datetime.datetime.fromtimestamp(self.message['timestamp'] // 1000)

    @property
    def implicit_ask_rate(self):
        return self.rate_service.implicit_ask_rate

    @property
    def implicit_bid_rate(self):
        return self.rate_service.implicit_bid_rate

    @property
    def std_out(self):
        return f"""
            --- Information about {self.product_name} {self.time}---
            * expiration date   : {self.expiration_date}
            * market data info  : {self.product_market_data}
            * spot info         : {self.spot_market_data}
            * ask implicit rate : {self.implicit_ask_rate}  
            * bid implicit rate : {self.implicit_bid_rate}  
            {30 * '-'}
            {30 * '-'}  
        """


def market_data_handler(message):
    global market_data_state
    market_data = ProductMarketDataHandler(message)
    print(market_data.std_out)
    product = ProductService(market_data)
    if product.is_active:
        arbitrage = ArbitrageRateService(market_data_state=deepcopy(market_data_state), last_product=product)
        opportunities = arbitrage.arbitrage_opportunities
        print("Arbitrage opportunities:")
        if opportunities:
            for op in opportunities:
                print(op)
        else:
            print("None")
    market_data_state[market_data.product_name] = product


def order_report_handler(message):
    print(f"OrderRouting msg: {message}")


def error_handler(message):
    print(f"Error msg: {message}")


def exception_handler(message):
    print(f"Exception msg: {message}")
