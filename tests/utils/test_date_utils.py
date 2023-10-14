import unittest
from unittest.mock import patch

import datetime
from src.utils.date_utils import DateUtilsException, last_business_day_in_month, expiration_date, days_to_expiration


class TestDateUtils(unittest.TestCase):
    def test_last_business_day_in_month(self):
        self.assertEqual(last_business_day_in_month(month=9, year=2023), 29)
        self.assertEqual(last_business_day_in_month(month=10, year=2023), 31)
        with self.assertRaises(DateUtilsException) as e:
            last_business_day_in_month(month=14, year=2023)
        self.assertIn(str(e.exception), "Wrong month input")

    def test_expiration_date(self):
        self.assertEqual(expiration_date(month=9, year=2023), datetime.date(day=29, month=9, year=2023))
        self.assertEqual(expiration_date(month=10, year=2023), datetime.date(day=31, month=10, year=2023))

    def test_days_to_expiration(self):
        with patch('src.utils.date_utils.date') as mock_date:
            mock_date.today.return_value = datetime.date(2023, 9, 21)
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            self.assertEqual(days_to_expiration(month=9, year=2023), 8)
            self.assertEqual(days_to_expiration(month=10, year=2023), 40)
