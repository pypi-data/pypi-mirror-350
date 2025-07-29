import json
import os
import unittest
from unittest.mock import patch

# Assuming read_fx_str_from_config is defined in jgtcommon.py
from jgtcommon import read_fx_str_from_config

# Path to the sample config JSON file
TEST_CONFIG_JSON_SAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'test_config_sample.json')

class TestReadFxStrFromConfigSampleFile(unittest.TestCase):
    @patch('jgtcommon.readconfig')
    def test_read_fx_str_from_configfile_demo_false(self, mock_readconfig):
        # Load the config data from the sample JSON file
        with open(TEST_CONFIG_JSON_SAMPLE_PATH, 'r') as file:
            config_data = json.load(file)
        
        # Mock the config data for demo=False
        mock_readconfig.return_value = config_data
        
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
    def test_read_fx_str_from_configfile_demo_true(self, mock_readconfig):
        # Load the config data from the sample JSON file
        with open(TEST_CONFIG_JSON_SAMPLE_PATH, 'r') as file:
            config_data = json.load(file)
        
        # Mock the config data for demo=True
        mock_readconfig.return_value = config_data
        
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