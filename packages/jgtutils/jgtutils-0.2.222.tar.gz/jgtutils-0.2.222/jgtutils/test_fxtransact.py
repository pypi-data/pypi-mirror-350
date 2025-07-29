import unittest
from unittest.mock import patch
from jgtfxhelper import mkfn_cfxdata_filepath
from FXTransact import FXTrade

class TestFXTrade(unittest.TestCase):
    def test_tofn_default_filename(self):
        trade = FXTrade(
            trade_id=123,
            account_id=456,
            account_name='Test Account',
            account_kind=1,
            offer_id=789,
            amount=1000,
            buy_sell='buy',
            open_rate=1.2345,
            open_time='2022-01-01 10:00:00',
            open_quote_id='quote123',
            open_order_id='order123',
            open_order_req_id='req123',
            open_order_request_txt='Test Order',
            commission=0.0,
            rollover_interest=0.0,
            trade_id_origin='',
            used_margin=0.0,
            value_date='',
            parties='',
            dividends=0.0,
            pl=0.0,
            gross_pl=0.0,
            close=0.0,
            stop=0.0,
            limit=0.0,
            stop_order_id='',
            limit_order_id='',
            instrument='EUR/USD',
            trail_rate=0.0,
            trail_step=0.0,
            close_commission=0.0,
            message=''
        )
        result = trade.tofn()
        self.assertEqual(result, 'trade_123.json')

    def test_tofn_custom_filename(self):
        trade = FXTrade(
            trade_id=123,
            account_id=456,
            account_name='Test Account',
            account_kind=1,
            offer_id=789,
            amount=1000,
            buy_sell='buy',
            open_rate=1.2345,
            open_time='2022-01-01 10:00:00',
            open_quote_id='quote123',
            open_order_id='order123',
            open_order_req_id='req123',
            open_order_request_txt='Test Order',
            commission=0.0,
            rollover_interest=0.0,
            trade_id_origin='',
            used_margin=0.0,
            value_date='',
            parties='',
            dividends=0.0,
            pl=0.0,
            gross_pl=0.0,
            close=0.0,
            stop=0.0,
            limit=0.0,
            stop_order_id='',
            limit_order_id='',
            instrument='EUR/USD',
            trail_rate=0.0,
            trail_step=0.0,
            close_commission=0.0,
            message=''
        )
        result = trade.tofn(ext='yaml', fn='my_trade')
        self.assertEqual(result, 'my_trade123.yaml')

if __name__ == '__main__':
    unittest.main()