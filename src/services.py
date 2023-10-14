from src.utils.rate_utils import implicit_rate
from src.utils.ticker_utils import expiration_date_str_from_product_name, stock_ticker_from_prduct_name


class ImplicitRateService:
    """
    Service class in charge of calculating implicit rates
    """

    def __init__(self, market_data_handler):
        self.market_data_handler = market_data_handler

    @property
    def implicit_bid_rate(self):
        return implicit_rate(self.market_data_handler.product_market_data["bid"]["price"],
                             self.market_data_handler.spot_market_data["ask"]["price"])

    @property
    def implicit_ask_rate(self):
        return implicit_rate(self.market_data_handler.product_market_data["ask"]["price"],
                             self.market_data_handler.spot_market_data["bid"]["price"])


class ProductService:
    def __init__(self, market_data_handler):
        self.market_data_handler = market_data_handler
        self.product_name = market_data_handler.product_name
        self.connected = True

    @property
    def is_active(self) -> bool:
        """
        A product_name is considered is_active when it receives not None bid and ask prices
        :return:
        """
        active_future = False
        active_spot = False
        if self.market_data_handler.implicit_bid_rate and self.market_data_handler.implicit_ask_rate:
            active_future = True
        if self.market_data_handler.spot_market_data['bid']['price'] and self.market_data_handler.spot_market_data['ask']['price']:
            active_spot = True
        return active_future and active_spot

    def __repr__(self):
        out = f"Product: {self.product_name} - Not Active"
        if self.is_active:
            out = f"Product: {self.product_name} - Ask Rate:{self.implicit_ask_rate} / Bid Rate:{self.implicit_bid_rate}"
        return out

    @property
    def implicit_ask_rate(self):
        return self.market_data_handler.implicit_ask_rate

    @property
    def implicit_bid_rate(self):
        return self.market_data_handler.implicit_bid_rate

    @property
    def date(self) -> str:
        """
        :return: The month/year of the product_name (i.e. 'OCT/23')
        """
        return expiration_date_str_from_product_name(self.product_name)


class ArbitrageRateService:
    def __init__(self, market_data_state, last_product):
        self.market_data_state = market_data_state
        self.last_product = last_product

    @property
    def compatible_date_products(self) -> list:
        """
        Search in the market data for products with the same end date
        :return:
        """
        return [product for product in self.market_data_state.values() if
                (product.date == self.last_product.date) and product.is_active]

    @property
    def arbitrage_opportunities(self) -> list:
        _arbitrage_opportunities = []
        if self.compatible_date_products:
            for product in self.compatible_date_products:
                if self.last_product.implicit_bid_rate > product.implicit_ask_rate:
                    _arbitrage_opportunities.append(f"""
                    Leg1 : Buy {stock_ticker_from_prduct_name(self.last_product.product_name)}, Sell {self.last_product.product_name} - Bid Rate: {self.last_product.implicit_bid_rate:.4%}
                    Leg2: Sell {stock_ticker_from_prduct_name(product.product_name)}, Buy {product.product_name} - Ask Rate: {product.implicit_ask_rate:.4%}
                    """)
                if product.implicit_bid_rate > self.last_product.implicit_ask_rate:
                    _arbitrage_opportunities.append(f"""
                    Leg1 : Buy {stock_ticker_from_prduct_name(product.product_name)}, Sell {product.product_name} - Bid Rate: {product.implicit_bid_rate:.4%}
                    Leg2: Sell {stock_ticker_from_prduct_name(self.last_product.product_name)}, Buy {self.last_product.product_name} - Ask Rate: {self.last_product.implicit_ask_rate:.4%}
                    """)
        return _arbitrage_opportunities


# from functools import partial
#
# import pyRofex
#
#
# def get_account_available_to_collateral(account=None):
#     account_summary = pyRofex.get_account_report(account=account)
#     return account_summary['accountData']['availableToCollateral']
#
#
# def send_order(side, ticker, size, price, order_type):
#     available = get_account_available_to_collateral()
#     if available > size * price:
#         order = pyRofex.send_order(ticker=ticker, side=side, size=size, price=price, order_type=order_type)
#         print(f"order sent: {order}")
#     else:
#         print(f"Unable to send order: needed {size * price}, available {available}")
#
#
# buy_order = partial(send_order, pyRofex.Side.BUY)
# sell_order = partial(send_order, pyRofex.Side.SELL)
#
#
# def cancel_order(client_order_id):
#     cancel_order = pyRofex.cancel_order(client_order_id=client_order_id)
#     return cancel_order