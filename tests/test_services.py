import unittest
from unittest.mock import patch, PropertyMock
from src.handlers import ProductMarketDataHandler, ImplicitRateService


class TestImplicitRateService(unittest.TestCase):

    @patch("src.handlers.ProductMarketDataHandler.spot_market_data", new_callable=PropertyMock)
    def test_bid_rate(self, mock_spot_market_data):
        msg = {'type': 'Md',
               'timestamp': 1695305477912,
               'instrumentId': {'marketId': 'ROFX', 'symbol': 'YPFD/OCT23'},
               'marketData': {'LA': None, 'OF': [{'price': 10550.0, 'size': 2}], 'BI': [{'price': 10450.0, 'size': 3}]}}

        mock_spot_market_data.return_value = {
            'bid' : {'price': 9450.0, 'size':10}, 'ask': {'price': 9850.0, 'size':20}}

        market_data_handler = ProductMarketDataHandler(msg)
        rate_service = ImplicitRateService(market_data_handler)

        bid_rate = rate_service.implicit_bid_rate
        ask_rate = rate_service.implicit_ask_rate

        self.assertTrue(abs(bid_rate-0.06091) <= 1e-5)
        self.assertTrue(abs(ask_rate-0.11640) <= 1e-5)