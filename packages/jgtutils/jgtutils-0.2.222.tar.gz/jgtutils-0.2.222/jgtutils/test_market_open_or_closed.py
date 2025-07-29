import unittest
from datetime import datetime, timezone

from jgtcommon import is_market_open


class TestMarketOpen(unittest.TestCase):
    def test_market_open_sunday(self):
        # Simulate Sunday at 21:00 UTC
        test_time = datetime(2023, 10, 1, 21, 0)  # Example date that is a Sunday
        self.assertTrue(is_market_open(test_time))

    def test_market_open_monday(self):
        # Simulate Monday at 10:00 UTC
        test_time = datetime(2023, 10, 2, 10, 0)  # Example date that is a Monday
        self.assertTrue(is_market_open(test_time))

    def test_market_open_friday_before_close(self):
        # Simulate Friday at 20:00 UTC
        test_time = datetime(2023, 10, 6, 20, 0)  # Example date that is a Friday
        self.assertTrue(is_market_open(test_time))
    
    def test_market_open_friday_just_before_close(self):
        # Simulate Friday at 21:00 UTC
        test_time = datetime(2024, 8, 9, 21, 14,0,0,tzinfo=timezone.utc)  # Example date that is a Friday when it is just closed
        result = is_market_open(test_time)
        self.assertTrue(result)

class TestMarketClosed(unittest.TestCase):
    def test_market_closed_saturday(self):
        # Simulate Saturday at 10:00 UTC
        test_time = datetime(2023, 10, 7, 10, 0)  # Example date that is a Saturday
        result = is_market_open(test_time)
        self.assertFalse(result)

    def test_market_closed_sunday(self):
        # Simulate Sunday at 10:00 UTC
        test_time = datetime(2023, 10, 8, 10, 0)  # Example date that is a Sunday
        result = is_market_open(test_time)
        self.assertFalse(result)

    def test_market_closed_friday_after_close(self):
        # Simulate Friday at 21:00 UTC
        test_time = datetime(2024, 8, 9, 21, 16,0,0,tzinfo=timezone.utc)  # Example date that is a Friday when it is just closed
        result = is_market_open(test_time)
        self.assertFalse(result)



    
if __name__ == '__main__':
    unittest.main()