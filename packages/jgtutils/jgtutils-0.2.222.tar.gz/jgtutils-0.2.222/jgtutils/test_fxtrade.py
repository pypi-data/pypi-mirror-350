import unittest
from unittest.mock import patch, MagicMock
from FXTransact import FXTrade

class TestFXTrade(unittest.TestCase):
    @patch('FXTransact.FXTrade.from_id')
    def test_from_id_valid_trade_id(self, mock_from_id):
        trade_id = 123
        mock_trade = MagicMock(spec=FXTrade)
        mock_trade.trade_id = trade_id
        mock_from_id.return_value = mock_trade

        trade = FXTrade.from_id(trade_id)
        self.assertIsInstance(trade, FXTrade)
        self.assertEqual(trade.trade_id, trade_id)

    @patch('FXTransact.FXTrade.from_id')
    def test_from_id_invalid_trade_id(self, mock_from_id):
        trade_id = -1
        mock_from_id.return_value = None

        trade = FXTrade.from_id(trade_id)
        self.assertIsNone(trade)
        
    

if __name__ == '__main__':
    unittest.main()