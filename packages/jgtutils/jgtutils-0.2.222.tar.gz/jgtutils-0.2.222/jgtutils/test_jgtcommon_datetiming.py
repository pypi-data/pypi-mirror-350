import unittest
from datetime import datetime, timezone
from jgtcommon import valid_datetime

class TestValidDatetime(unittest.TestCase):
    def test_valid_datetime(self):
        
        ##date_format = '%m.%d.%Y %H:%M:%S'
        
        # Test case 1: Valid datetime in the correct format
        str_datetime = "01.13.2022 12:00:00"
        result = valid_datetime(True)(str_datetime)
        expected_result = datetime(2022, 1, 13, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected_result)
        
        
        str_datetime = "01.13.2022 15:00:00"
        result = valid_datetime(True)(str_datetime)
        expected_result = datetime(2022, 1, 13, 15, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()