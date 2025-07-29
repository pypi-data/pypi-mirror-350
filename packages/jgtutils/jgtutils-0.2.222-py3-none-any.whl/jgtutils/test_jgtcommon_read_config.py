import unittest
from unittest.mock import patch

# Assuming read_fx_str_from_config is defined in jgtcommon.py
from jgtcommon import read_fx_str_from_config


class TestReadFxStrFromConfig(unittest.TestCase):
    @patch('jgtcommon.readconfig')
    def test_read_fx_str_from_config_demo_false(self, mock_readconfig):
        # Mock the config data for demo=False
        mock_readconfig.return_value = {
            "user_id": "010101010",
            "account": "0001",
            "password": "MyRealFXCMPassword",
            "url": "https://www.fxcorporate.com/Hosts.jsp",
            "connection": "Real"
        }
        
        expected_result = (
            "010101010",
            "MyRealFXCMPassword",
            "https://www.fxcorporate.com/Hosts.jsp",
            "Real",
            "0001"
        )
        
        result = read_fx_str_from_config(demo=False)
        self.assertEqual(result, expected_result)

    @patch('jgtcommon.readconfig')
    def test_read_fx_str_from_config_demo_true(self, mock_readconfig):
        # Mock the config data for demo=True
        mock_readconfig.return_value = {
            "user_id": "U10D8798797",
            "password": "MyDemoFXCMPassword",
            "account": "002342343",
            "url": "https://www.fxcorporate.com/Hosts.jsp",
            "connection": "Demo"
        }
        
        expected_result = (
            "U10D8798797",
            "MyDemoFXCMPassword",
            "https://www.fxcorporate.com/Hosts.jsp",
            "Demo",
            "002342343"
        )
        
        result = read_fx_str_from_config(demo=True)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()