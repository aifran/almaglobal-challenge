import unittest

from src.utils.ticker_utils import rofex_ticker_from_product_name, expiration_date_str_from_product_name, expiration_date_int_from_product_name

class TestTickerUtils(unittest.TestCase):
    def test_rofex_ticker_from_product(self):
        self.assertEqual(rofex_ticker_from_product_name('GGAL/OCT23'), 'GGAL')
        self.assertEqual(rofex_ticker_from_product_name('DLR/OCT23'), 'DLR')
        self.assertEqual(rofex_ticker_from_product_name('YPFD/OCT23'), 'YPFD')

    def test_end_date_str_from_product(self):
        self.assertEqual(expiration_date_str_from_product_name('GGAL/OCT23'), 'OCT23')
        self.assertEqual(expiration_date_str_from_product_name('DLR/DIC23'), 'DIC23')
        self.assertEqual(expiration_date_str_from_product_name('YPFD/OCT23'), 'OCT23')

    def test_end_date_int_from_product(self):
        self.assertEqual(expiration_date_int_from_product_name('GGAL/OCT23'), (10, 2023))
        self.assertEqual(expiration_date_int_from_product_name('DLR/DIC23'), (12, 2023))
        self.assertEqual(expiration_date_int_from_product_name('YPFD/OCT23'), (10, 2023))