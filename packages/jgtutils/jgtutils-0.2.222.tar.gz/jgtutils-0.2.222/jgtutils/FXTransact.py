
import datetime
import json
import ruamel.yaml;yaml = ruamel.yaml.YAML()
OUTPUT_YAML_DISABLED=True

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtos import sanitize_filename
from jgtclihelper import print_jsonl_message
from jgtfxhelper import offer_id_to_instrument as _offer_id_to_instrument

import jgtfxhelper

ORDER_FILE_PREFIX="order_"
TRADE_FILE_PREFIX="trade_"
TRADES_FILE_PREFIX="trades"
ORDERS_FILE_PREFIX="orders"
FXTRANSAC_FILE_PREFIX="fxtransact"
TRADE_FXMVSTOP_PREFIX = "fxmvstop_"
ORDER_ADD_PREFIX="fxaddorder_"
ORDER_RM_PREFIX="fxrmorder_"
TRADE_FXRM_PREFIX="fxrmtrade_"
FXREPORT_FILE_PREFIX="fxreport_"

#JGTAPP__PREFIX="fxmvstopgator_"

#@STCGoal FUTURE YAML Simplified Representation
"""
orders:
- order_id: 170013060
  status: W
  amount: 2000
  instrument: NZD/CAD
  rate: 0.82661
  stop: 0.82787
  filled_amount: 0
  expire_date: '1899-12-30 00:00:00'
  time_in_force: GTC
  status_time: '2024-08-16 13:19:21'
trades: []
"""

class FXTrades:
    def __init__(self, trades=None):
        self.trades = trades or []
    
    def add_trade(self, trade_data):
        #support json string or string
        input_is_string = isinstance(trade_data, str)
        if input_is_string:
            try:
                trade_data = FXTrade.from_string(trade_data)
            except ValueError:
                trade_data = FXTrade.from_json_string(trade_data)
        else:
            self.trades.append(trade_data)
    
    def to_dict(self):
        return {
            "trades": [trade.to_dict() for trade in self.trades]
        }
    
    def tojson(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def toyaml(self):
        return yaml.dump(self.to_dict())
    
    def tofn(self,ext="json",fb=TRADES_FILE_PREFIX):
        return FXTrades.mkfn(ext,fb)
    
    @staticmethod
    def mkfn(ext="json",fn=None):
        if fn is None:
            fn=TRADES_FILE_PREFIX
        trades_filename = f"{fn}.{ext}"
        return sanitize_filename(trades_filename)
    
    @staticmethod
    def mkpath(ext="json",use_local=True,fn=None):
        fn=FXTrades.mkfn(ext,fn)
        return jgtfxhelper.mkfn_cfxdata_filepath(fn,use_local=use_local)
    
    def get_path(self,ext="json",use_local=True,fn=TRADES_FILE_PREFIX):
        return FXTrades.mkpath(ext,use_local,fn)
        
    def tojsonfile(self, filename:str=None,use_local=True):
        if not filename:
            filename = self.get_path(use_local=use_local)
        try:            
            with open(filename, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def toyamlfile(self, filename:str=None):
        if not filename:
            filename = self.tofn("yaml")
        if not OUTPUT_YAML_DISABLED:
            try:
                with open(filename, 'w') as f:
                    f.write(self.toyaml())
            except Exception as e:
                print(f"Error writing to file: {e}")
    
    @classmethod
    def from_string(cls, trades_string):
        trades = []
        for trade_string in trades_string.split('\n'):
            trades.append(FXTrade.from_string(trade_string))
        return cls(trades)

class FXTrade:
    def __init__(self, trade_id, account_id, account_name, account_kind, offer_id, amount, buy_sell, open_rate, open_time, open_quote_id, open_order_id, open_order_req_id, open_order_request_txt, commission, rollover_interest, trade_id_origin, used_margin, value_date, parties, dividends, pl, gross_pl, close, stop, limit, stop_order_id, limit_order_id, instrument, trail_rate, trail_step, close_commission,message=''):
        self.trade_id = trade_id
        self.account_id = account_id
        self.account_name = account_name
        self.account_kind = account_kind
        self.offer_id = offer_id
        self.amount = amount
        self.buy_sell = buy_sell
        self.open_rate = open_rate
        self.open_time = datetime.datetime.strptime(open_time, '%Y-%m-%d %H:%M:%S') if open_time else None
        self.open_quote_id = open_quote_id
        self.open_order_id = open_order_id
        self.open_order_req_id = open_order_req_id
        self.open_order_request_txt = open_order_request_txt
        self.commission = commission
        self.rollover_interest = rollover_interest
        self.trade_id_origin = trade_id_origin
        self.used_margin = used_margin
        self.value_date = value_date
        self.parties = parties
        self.dividends = dividends
        self.pl = pl
        self.gross_pl = gross_pl
        self.close = close
        self.stop = stop
        self.limit = limit
        self.stop_order_id = stop_order_id
        self.limit_order_id = limit_order_id
        self.instrument = instrument
        self.trail_rate = trail_rate
        self.trail_step = trail_step
        self.close_commission = close_commission
        self.message = message

    def to_dict(self):
        return {
            "trade_id": self.trade_id,
            "account_id": self.account_id,
            "account_name": self.account_name,
            "account_kind": self.account_kind,
            "offer_id": self.offer_id,
            "amount": self.amount,
            "buy_sell": self.buy_sell,
            "open_rate": self.open_rate,
            "open_time": str(self.open_time),
            "open_quote_id": self.open_quote_id,
            "open_order_id": self.open_order_id,
            "open_order_req_id": self.open_order_req_id,
            "open_order_request_txt": self.open_order_request_txt,
            "commission": self.commission,
            "rollover_interest": self.rollover_interest,
            "trade_id_origin": self.trade_id_origin,
            "used_margin": self.used_margin,
            "value_date": self.value_date,
            "parties": self.parties,
            "dividends": self.dividends,
            "pl": self.pl,
            "gross_pl": self.gross_pl,
            "close": self.close,
            "stop": self.stop,
            "limit": self.limit,
            "stop_order_id": self.stop_order_id,
            "limit_order_id": self.limit_order_id,
            "instrument": self.instrument,
            "trail_rate": self.trail_rate,
            "trail_step": self.trail_step,
            "close_commission": self.close_commission,
            "message": self.message
        }
    
    def from_json_string(self, json_string):
        trade_data = json.loads(json_string)
        return FXTrade(
            trade_id=trade_data.get('trade_id', 0),
            account_id=trade_data.get('account_id', 0),
            account_name=trade_data.get('account_name', ''),
            account_kind=trade_data.get('account_kind', 0),
            offer_id=trade_data.get('offer_id', 0),
            amount=trade_data.get('amount', 0),
            buy_sell=trade_data.get('buy_sell', ''),
            open_rate=trade_data.get('open_rate', 0.0),
            open_time=trade_data.get('open_time', ''),
            open_quote_id=trade_data.get('open_quote_id', ''),
            open_order_id=trade_data.get('open_order_id', ''),
            open_order_req_id=trade_data.get('open_order_req_id', ''),
            open_order_request_txt=trade_data.get('open_order_request_txt', ''),
            commission=trade_data.get('commission', 0.0),
            rollover_interest=trade_data.get('rollover_interest', 0.0),
            trade_id_origin=trade_data.get('trade_id_origin', ''),
            used_margin=trade_data.get('used_margin', 0.0),
            value_date=trade_data.get('value_date', ''),
            parties=trade_data.get('parties', ''),
            dividends=trade_data.get('dividends', 0.0),
            pl=trade_data.get('pl', 0.0),
            gross_pl=trade_data.get('gross_pl', 0.0),
            close=trade_data.get('close', 0.0),
            stop=trade_data.get('stop', 0.0),
            limit=trade_data.get('limit', 0.0),
            stop_order_id=trade_data.get('stop_order_id', ''),
            limit_order_id=trade_data.get('limit_order_id', ''),
            instrument=trade_data.get('instrument', ''),
            trail_rate=trade_data.get('trail_rate', 0.0),
            trail_step=trade_data.get('trail_step', 0.0),
            close_commission=trade_data.get('close_commission', 0.0),
            message=trade_data.get('message', '')
        )
    
    def tojson(self,indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def toyaml(self):
        return yaml.dump(self.to_dict())
    
    def tofn(self,ext="json",fn=TRADE_FILE_PREFIX):
        return FXTrade.mkfn(self.trade_id,ext,fn)
    
    def get_path(self,ext="json",use_local=True,fn=TRADE_FILE_PREFIX):
        return FXTrade.mkpath(self.trade_id,ext,use_local,fn)
    
    @staticmethod
    def mkfn(trade_id,ext="json",fn=None):
        if fn is None:
            fn=TRADE_FILE_PREFIX
        transaction_file = f"{fn}{trade_id}.{ext}"
        return sanitize_filename(transaction_file)
    
    @staticmethod
    def mkpath(trade_id,ext="json",use_local=True,fn=None):
        fn=FXTrade.mkfn(trade_id,ext,fn)
        return jgtfxhelper.mkfn_cfxdata_filepath(fn,use_local=use_local)
    
    @staticmethod
    def from_path(fpath:str):
        try:
            with open(fpath, 'r') as f:
                trade_data = f.read()
                return FXTrade.from_json_string(trade_data)
        except Exception as e:
            print(f"Error reading from file: {e}")
        return None
    
    # @staticmethod
    # def create_path(use_local):
    #     fxtransact_filepath=jgtfxhelper.mkfn_cfxdata_filepath(TRADE_FILE_PREFIX,use_local=use_local)
    #     return fxtransact_filepath
    
    @staticmethod
    def from_id(trade_id,use_local=True):
        fpath=FXTrade.mkpath(trade_id,use_local=use_local)
        return FXTrade.from_path(fpath)
    
    
    
    def tojsonfile(self, filename:str=None,use_local=True):
        if not filename:
            filename = self.get_path(use_local=use_local)
            # if use_local:
            #     filename = jgtfxhelper.mkfn_cfxdata_filepath(filename,use_local=use_local) #@STCGoal Gets saved in the local data directory if flag use_local is given without a filename
        try:
            with open(filename, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def toyamlfile(self, filename:str=None):
        if not filename:
            filename = self.tofn("yaml")
        if not OUTPUT_YAML_DISABLED:
            try:
                with open(filename, 'w') as f:
                    f.write(self.toyaml())
            except Exception as e:
                print(f"Error writing to file: {e}")
    
    @classmethod
    def from_string(cls, trade_string):
        trade_data = {}
        trades = trade_string.split(';')
        #raise if not a valid trade string
        if len(trades) < 2:
            raise ValueError("Invalid trade string")
        for item in trades:
            if '=' in item:
                key, value = item.split('=')
                key = key.strip()
                value = value.strip()
                trade_data[key] = value
        return cls(
            trade_id=int(trade_data.get('trade_id', 0)),
            account_id=int(trade_data.get('account_id', 0)),
            account_name=trade_data.get('account_name', ''),
            account_kind=int(trade_data.get('account_kind', 0)),
            offer_id=int(trade_data.get('offer_id', 0)),
            amount=int(trade_data.get('amount', 0)),
            buy_sell=trade_data.get('buy_sell', ''),
            open_rate=float(trade_data.get('open_rate', 0.0)),
            open_time=trade_data.get('open_time', ''),
            open_quote_id=trade_data.get('open_quote_id', ''),
            open_order_id=trade_data.get('open_order_id', ''),
            open_order_req_id=trade_data.get('open_order_req_id', ''),
            open_order_request_txt=trade_data.get('open_order_request_txt', ''),
            commission=float(trade_data.get('commission', 0.0)),
            rollover_interest=float(trade_data.get('rollover_interest', 0.0)),
            trade_id_origin=trade_data.get('trade_id_origin', ''),
            used_margin=float(trade_data.get('used_margin', 0.0)),
            value_date=trade_data.get('value_date', ''),
            parties=trade_data.get('parties', ''),
            dividends=float(trade_data.get('dividends', 0.0)),
            pl=float(trade_data.get('pl', 0.0)),
            gross_pl=float(trade_data.get('gross_pl', 0.0)),
            close=float(trade_data.get('close', 0.0)),
            stop=float(trade_data.get('stop', 0.0)),
            limit=float(trade_data.get('limit', 0.0)),
            stop_order_id=trade_data.get('stop_order_id', ''),
            limit_order_id=trade_data.get('limit_order_id', ''),
            instrument=trade_data.get('instrument', ''),
            trail_rate=float(trade_data.get('trail_rate', 0.0)),
            trail_step=float(trade_data.get('trail_step', 0.0)),
            close_commission=float(trade_data.get('close_commission', 0.0))
        )

    def __repr__(self):
        return f"Trade(trade_id={self.trade_id}, account_id={self.account_id}, account_name='{self.account_name}', account_kind={self.account_kind}, offer_id={self.offer_id}, amount={self.amount}, buy_sell='{self.buy_sell}', open_rate={self.open_rate}, open_time='{self.open_time}', open_quote_id='{self.open_quote_id}', open_order_id='{self.open_order_id}', open_order_req_id='{self.open_order_req_id}', open_order_request_txt='{self.open_order_request_txt}', commission={self.commission}, rollover_interest={self.rollover_interest}, trade_id_origin='{self.trade_id_origin}', used_margin={self.used_margin}, value_date='{self.value_date}', parties='{self.parties}', dividends={self.dividends}, pl={self.pl}, gross_pl={self.gross_pl}, close={self.close}, stop={self.stop}, limit={self.limit}, stop_order_id='{self.stop_order_id}', limit_order_id='{self.limit_order_id}', instrument='{self.instrument}', trail_rate={self.trail_rate}, trail_step={self.trail_step}, close_commission={self.close_commission}, message='{self.message}')"


class FXOrders:
    def __init__(self, orders=None):
        self.orders = orders or []
    
    def add_order(self, order_data):
        #support json string or string
        input_is_string = isinstance(order_data, str)
        if input_is_string:
            try:
                order_data = FXOrder.from_string(order_data)
            except ValueError:
                order_data = FXOrder.from_json_string(order_data)
        else:
            self.orders.append(order_data)
    
    def to_dict(self):
        return {
            "orders": [order.to_dict() for order in self.orders]
        }
    def tojson(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def toyaml(self):
        return yaml.dump(self.to_dict())
    
    @staticmethod
    def mkfn(ext="json",fn=None):
        if fn is None:
            fn=ORDERS_FILE_PREFIX
        orders_filename = f"{fn}.{ext}"
        return sanitize_filename(orders_filename)      
    
    @staticmethod
    def mkpath(ext="json",use_local=True,fn=None):
        fn=FXOrders.mkfn(ext,fn)
        return jgtfxhelper.mkfn_cfxdata_filepath(fn,use_local=use_local)
    
    def get_path(self,ext="json",fn=ORDERS_FILE_PREFIX,use_local=True):
        return FXOrders.mkpath(ext,use_local,fn)
    
    def tojsonfile(self, filename:str=None,use_local=True):
        if not filename:
            filename = self.get_path(use_local=use_local)
        try:
            with open(filename, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def toyamlfile(self, filename:str=None):
        if not filename:
            filename = self.get_path("yaml")
        if not OUTPUT_YAML_DISABLED:
            try:
                with open(filename, 'w') as f:
                    f.write(self.toyaml())
            except Exception as e:
                print(f"Error writing to file: {e}")
                
    @classmethod
    def from_string(cls, orders_string):
        orders = []
        for order_string in orders_string.split('\n'):
            orders.append(FXOrder.from_string(order_string))
        return cls(orders)


class FXOrder:
    def __init__(self, order_id, request_id, rate, execution_rate, rate_min, rate_max, trade_id, account_id, account_name, offer_id, net_quantity, buy_sell, stage, type, status, status_time, amount, lifetime, at_market, trail_step, trail_rate, time_in_force, account_kind, request_txt, contingent_order_id, contingency_type, primary_id, origin_amount, filled_amount, working_indicator, peg_type, peg_offset, peg_offset_min, peg_offset_max, expire_date, value_date, parties, side, stop, limit, stop_order_id, limit_order_id, type_stop, type_limit, stop_trail_step, stop_trail_rate,message=''):
        self.order_id = order_id
        self.request_id = request_id
        self.rate = rate
        self.execution_rate = execution_rate
        self.rate_min = rate_min
        self.rate_max = rate_max
        self.trade_id = trade_id
        self.account_id = account_id
        self.account_name = account_name
        self.offer_id = offer_id
        self.net_quantity = net_quantity
        self.buy_sell = buy_sell
        self.stage = stage
        self.type = type
        self.status = status
        self.status_time = datetime.datetime.strptime(status_time, '%Y-%m-%d %H:%M:%S')
        self.amount = amount
        self.lifetime = lifetime
        self.at_market = at_market
        self.trail_step = trail_step
        self.trail_rate = trail_rate
        self.time_in_force = time_in_force
        self.account_kind = account_kind
        self.request_txt = request_txt
        self.contingent_order_id = contingent_order_id
        self.contingency_type = contingency_type
        self.primary_id = primary_id
        self.origin_amount = origin_amount
        self.filled_amount = filled_amount
        self.working_indicator = working_indicator
        self.peg_type = peg_type
        self.peg_offset = peg_offset
        self.peg_offset_min = peg_offset_min
        self.peg_offset_max = peg_offset_max
        self.expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d %H:%M:%S')
        self.value_date = value_date
        self.parties = parties
        self.side = side
        self.stop = stop
        self.limit = limit
        self.stop_order_id = stop_order_id
        self.limit_order_id = limit_order_id
        self.type_stop = type_stop
        self.type_limit = type_limit
        self.stop_trail_step = stop_trail_step
        self.stop_trail_rate = stop_trail_rate
        self.instrument = _offer_id_to_instrument(offer_id)
        self.message = message

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "request_id": self.request_id,
            "rate": self.rate,
            "execution_rate": self.execution_rate,
            "rate_min": self.rate_min,
            "rate_max": self.rate_max,
            "trade_id": self.trade_id,
            "account_id": self.account_id,
            "account_name": self.account_name,
            "offer_id": self.offer_id,
            "net_quantity": self.net_quantity,
            "buy_sell": self.buy_sell,
            "stage": self.stage,
            "type": self.type,
            "status": self.status,
            "status_time": str(self.status_time),
            "amount": self.amount,
            "lifetime": self.lifetime,
            "at_market": self.at_market,
            "trail_step": self.trail_step,
            "trail_rate": self.trail_rate,
            "time_in_force": self.time_in_force,
            "account_kind": self.account_kind,
            "request_txt": self.request_txt,
            "contingent_order_id": self.contingent_order_id,
            "contingency_type": self.contingency_type,
            "primary_id": self.primary_id,
            "origin_amount": self.origin_amount,
            "filled_amount": self.filled_amount,
            "working_indicator": self.working_indicator,
            "peg_type": self.peg_type,
            "peg_offset": self.peg_offset,
            "peg_offset_min": self.peg_offset_min,
            "peg_offset_max": self.peg_offset_max,
            "expire_date": str(self.expire_date),
            "value_date": self.value_date,
            "side": self.side,
            "stop": self.stop,
            "limit": self.limit,
            "stop_order_id": self.stop_order_id,
            "limit_order_id": self.limit_order_id,
            "type_stop": self.type_stop,
            "type_limit": self.type_limit,
            "stop_trail_step": self.stop_trail_step,
            "stop_trail_rate": self.stop_trail_rate,
            "instrument": self.instrument,
            "message": self.message
        }

    def tojson(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def toyaml(self):
        return yaml.dump(self.to_dict())
    
    
    def tofn(self,ext="json",fn=ORDER_FILE_PREFIX):
        return FXOrder.mkfn(self.order_id,ext,fn)
    
    def get_path(self,ext="json",use_local=True,fn=ORDER_FILE_PREFIX):
        return FXOrder.mkpath(self.order_id,ext,use_local,fn)
    
    @staticmethod
    def mkfn(order_id,ext="json",fn=None):
        if fn is None:
            fn=ORDER_FILE_PREFIX
        transaction_filename = f"{fn}{order_id}.{ext}"
        return sanitize_filename(transaction_filename)
    
    @staticmethod
    def mkpath(order_id,ext="json",use_local=True,fn=None):
        fn=FXOrder.mkfn(order_id,ext,fn)
        return jgtfxhelper.mkfn_cfxdata_filepath(fn,use_local=use_local)
        
    @staticmethod
    def from_path(fpath:str):
        try:
            with open(fpath, 'r') as f:
                order_data = f.read()
                return FXOrder.from_json_string(order_data)
        except Exception as e:
            print(f"Error reading from file: {e}")
        return None
    
    @staticmethod
    def from_id(order_id,use_local=True):
        fpath=FXOrder.mkpath(order_id,use_local=use_local)
        return FXOrder.from_path(fpath)     
    
    def tojsonfile(self, filename:str=None,use_local=False):
        if not filename:
            filename = self.get_path(use_local=use_local)
            # if use_local:
            #     filename = jgtfxhelper.mkfn_cfxdata_filepath(filename,use_local=use_local) #@STCGoal Gets saved in the local data directory if flag use_local is given without a filename
        try:
            with open(filename, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def toyamlfile(self, filename:str=None):
        if not filename:
            filename = self.tofn("yaml")
        if not OUTPUT_YAML_DISABLED:
            try:
                with open(filename, 'w') as f:
                    f.write(self.toyaml())
            except Exception as e:
                print(f"Error writing to file: {e}")
    
    def from_json_string(self,json_string):
        order_data = json.loads(json_string)
        offer_id = order_data.get('offer_id', 0)
        return FXOrder(
            order_id=order_data.get('order_id', 0),
            request_id=order_data.get('request_id', ''),
            rate=order_data.get('rate', 0.0),
            execution_rate=order_data.get('execution_rate', 0.0),
            rate_min=order_data.get('rate_min', 0.0),
            rate_max=order_data.get('rate_max', 0.0),
            trade_id=order_data.get('trade_id', 0),
            account_id=order_data.get('account_id', 0),
            account_name=order_data.get('account_name', ''),
            offer_id=offer_id,
            net_quantity=order_data.get('net_quantity', False),
            buy_sell=order_data.get('buy_sell', ''),
            stage=order_data.get('stage', ''),
            type=order_data.get('type', ''),
            status=order_data.get('status', ''),
            status_time=order_data.get('status_time', ''),
            amount=order_data.get('amount', 0),
            lifetime=order_data.get('lifetime', 0.0),
            at_market=order_data.get('at_market', 0.0),
            trail_step=order_data.get('trail_step', 0),
            trail_rate=order_data.get('trail_rate', 0.0),
            time_in_force=order_data.get('time_in_force', ''),
            account_kind=order_data.get('account_kind', 0),
            request_txt=order_data.get('request_txt', ''),
            contingent_order_id=order_data.get('contingent_order_id', 0),
            contingency_type=order_data.get('contingency_type', 0),
            primary_id=order_data.get('primary_id', ''),
            origin_amount=order_data.get('origin_amount', 0),
            filled_amount=order_data.get('filled_amount', 0),
            working_indicator=order_data.get('working_indicator', False),
            peg_type=order_data.get('peg_type', ''),
            peg_offset=order_data.get('peg_offset', 0.0),
            peg_offset_min=order_data.get('peg_offset_min', 0.0),
            peg_offset_max=order_data.get('peg_offset_max', 0.0),
            expire_date=order_data.get('expire_date', ''),
            value_date=order_data.get('value_date', ''),
            parties=order_data.get('parties', ''),
            side=order_data.get('side', 0),
            stop=order_data.get('stop', 0.0),
            limit=order_data.get('limit', 0.0),
            stop_order_id=order_data.get('stop_order_id', ''),
            limit_order_id=order_data.get('limit_order_id', ''),
            type_stop=order_data.get('type_stop', 0),
            type_limit=order_data.get('type_limit', 0),
            stop_trail_step=order_data.get('stop_trail_step', 0),
            stop_trail_rate=order_data.get('stop_trail_rate', 0.0),
            instrument=_offer_id_to_instrument(offer_id),
            message=order_data.get('message', '')
        )
    
            
    @classmethod
    def from_string(cls, order_string):
        order_data = {}
        orders = order_string.split(';')
        #raise if not a valid order string
        if len(orders) < 2:
            raise ValueError("Invalid order string")
        for item in orders:
            if '=' in item:
                key, value = item.split('=')
                key = key.strip()
                value = value.strip()
                order_data[key] = value
        contingent_order_id = order_data.get('contingent_order_id', 0)
        if contingent_order_id == '':
            contingent_order_id='0'
        return cls(
            order_id=int(order_data.get('order_id', 0)),
            request_id=order_data.get('request_id', ''),
            rate=float(order_data.get('rate', 0.0)),
            execution_rate=float(order_data.get('execution_rate', 0.0)),
            rate_min=float(order_data.get('rate_min', 0.0)),
            rate_max=float(order_data.get('rate_max', 0.0)),
            trade_id=int(order_data.get('trade_id', 0)),
            account_id=int(order_data.get('account_id', 0)),
            account_name=order_data.get('account_name', ''),
            offer_id=int(order_data.get('offer_id', 0)),
            net_quantity=order_data.get('net_quantity', 'False') == 'True',
            buy_sell=order_data.get('buy_sell', ''),
            stage=order_data.get('stage', ''),
            type=order_data.get('type', ''),
            status=order_data.get('status', ''),
            status_time=order_data.get('status_time', ''),
            amount=int(order_data.get('amount', 0)),
            lifetime=float(order_data.get('lifetime', 0.0)),
            at_market=float(order_data.get('at_market', 0.0)),
            trail_step=int(order_data.get('trail_step', 0)),
            trail_rate=float(order_data.get('trail_rate', 0.0)),
            time_in_force=order_data.get('time_in_force', ''),
            account_kind=int(order_data.get('account_kind', 0)),
            request_txt=order_data.get('request_txt', ''),
            contingent_order_id=int(contingent_order_id),
            contingency_type=int(order_data.get('contingency_type', 0)),
            primary_id=order_data.get('primary_id', ''),
            origin_amount=int(order_data.get('origin_amount', 0)),
            filled_amount=int(order_data.get('filled_amount', 0)),
            working_indicator=order_data.get('working_indicator', 'False') == 'True',
            peg_type=order_data.get('peg_type', ''),
            peg_offset=float(order_data.get('peg_offset', 0.0)),
            peg_offset_min=float(order_data.get('peg_offset_min', 0.0)),
            peg_offset_max=float(order_data.get('peg_offset_max', 0.0)),
            expire_date=order_data.get('expire_date', ''),
            value_date=order_data.get('value_date', ''),
            parties=order_data.get('parties', ''),
            side=int(order_data.get('side', 0)),
            stop=float(order_data.get('stop', 0.0)),
            limit=float(order_data.get('limit', 0.0)),
            stop_order_id=order_data.get('stop_order_id', ''),
            limit_order_id=order_data.get('limit_order_id', ''),
            type_stop=int(order_data.get('type_stop', 0)),
            type_limit=int(order_data.get('type_limit', 0)),
            stop_trail_step=int(order_data.get('stop_trail_step', 0)),
            stop_trail_rate=float(order_data.get('stop_trail_rate', 0.0))
        )

    def __repr__(self):
        return f"FXOrder(order_id={self.order_id}, request_id='{self.request_id}', rate={self.rate}, execution_rate={self.execution_rate}, rate_min={self.rate_min}, rate_max={self.rate_max}, trade_id={self.trade_id}, account_id={self.account_id}, account_name='{self.account_name}', offer_id={self.offer_id}, net_quantity={self.net_quantity}, buy_sell='{self.buy_sell}', stage='{self.stage}', type='{self.type}', status='{self.status}', status_time='{self.status_time}', amount={self.amount}, lifetime={self.lifetime}, at_market={self.at_market}, trail_step={self.trail_step}, trail_rate={self.trail_rate}, time_in_force='{self.time_in_force}', account_kind={self.account_kind}, request_txt='{self.request_txt}', contingent_order_id={self.contingent_order_id}, contingency_type={self.contingency_type}, primary_id='{self.primary_id}', origin_amount={self.origin_amount}, filled_amount={self.filled_amount}, working_indicator={self.working_indicator}, peg_type='{self.peg_type}', peg_offset={self.peg_offset}, peg_offset_min={self.peg_offset_min}, peg_offset_max={self.peg_offset_max}, expire_date='{self.expire_date}', value_date='{self.value_date}', parties='{self.parties}', side={self.side}, stop={self.stop}, limit={self.limit}, stop_order_id='{self.stop_order_id}', limit_order_id='{self.limit_order_id}', type_stop={self.type_stop}, type_limit={self.type_limit}, stop_trail_step={self.stop_trail_step}, stop_trail_rate={self.stop_trail_rate}, instrument='{self.instrument}', message='{self.message}')"

#Wrapper classes for FXTrade and FXOrder
class FXTransactWrapper:
    def __init__(self, trades:FXTrades=None, orders:FXOrders=None):
        self.trades = trades if trades else FXTrades()
        self.orders = orders if orders else FXOrders()
    
    def to_dict(self):
        return {
            "trades": self.trades.to_dict()["trades"] if self.trades else None,
            "orders": self.orders.to_dict()["orders"] if self.orders else None
        }
    
    def add_trades(self, trades:FXTrades):
        self.trades = trades if trades else FXTrades()
    
    def add_trade(self, trade_data:FXTrade):
        self.trades.add_trade(trade_data)
        
    def get_trade(self, trade_id):
        for trade in self.trades.trades:
            if str(trade['trade_id']) == str(trade_id):
                return trade
        return None
    
    def add_orders(self, orders:FXOrders):
        self.orders = orders if orders else FXOrders()
    
    def add_order(self, order_data:FXOrder):
        self.orders.add_order(order_data)
    
    def get_order(self, order_id):
        for order in self.orders.orders:
            if str(order['order_id']) == str(order_id):
                return order
        return None
    
    def find_matching_trade(self,order,quiet=False):
        for trade in self.trades:
            #open_order_id
            order_id_name = 'OrderID'
            if not order_id_name in order:
                order_id_name = 'order_id' #Compatibility with old order_id
            if trade['open_order_id'] == order[order_id_name]:
                msg = "Matched trade found by open_order_id"
                if not quiet:
                    print_jsonl_message(msg, trade)
                return trade
            
            if (trade['instrument'] == order['instrument'] and
                trade['open_rate'] == order['entry_rate'] and
                trade['stop'] == order['stop_rate'] and
                trade['amount'] == order['lots']):
                if not quiet:
                    msg = "Matched trade found by instrument, entry_rate, stop_rate, and lots:"
                    if not quiet:
                        print_jsonl_message(msg, trade)
                return trade
        return None

    @staticmethod
    def from_ds(trade_id=None,use_local=True):
        fxtransact_filepath = FXTransactWrapper.create_path(use_local=use_local)
        return FXTransactWrapper.from_path(fxtransact_filepath)

    @staticmethod
    def make_fxtransact_filename(trade_id=None,fn=FXTRANSAC_FILE_PREFIX,ext="json"):
        suffix = f"_{trade_id}" if trade_id else ""
        fpath = f"{fn}{suffix}.{ext}"
        return FXTransactWrapper.sanitize_filename(ext, fpath)

    @staticmethod
    def sanitize_filename(ext, fpath):
        return fpath.replace("__","_").replace("_.",".").replace(f".{ext}.{ext}",f".{ext}")
    
    @staticmethod
    def create_path(trade_id=None,fn=FXTRANSAC_FILE_PREFIX,ext="json",use_local=True):
        fpath = FXTransactWrapper.make_fxtransact_filename(trade_id=trade_id,fn=fn,ext=ext)
        fxtransact_filepath=jgtfxhelper.mkfn_cfxdata_filepath(fpath,use_local=use_local)
        return fxtransact_filepath
    
    
    def tojson(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def toyaml(self):
        return yaml.dump(self.to_dict())
    
    def _to_filename(self,ext="json",fn=FXTRANSAC_FILE_PREFIX):
        return f"{fn}.{ext}"
    
    @staticmethod
    def mkfilename(ext="json",fn=None):
        if fn is None:
            fn=FXTRANSAC_FILE_PREFIX
        fname = f"{fn}.{ext}"
        return fname
    
    @staticmethod
    def mkpath(ext="json",use_local=True,fn=None):
        fn=FXTransactWrapper.mkfilename(ext,fn)
        fpath = jgtfxhelper.mkfn_cfxdata_filepath(fn,use_local=use_local,ext=ext)
        return fpath
    
    @staticmethod
    def from_path(filename:str=None,use_local=True):
        fpath=FXTransactWrapper.mkpath("json",use_local,fn=filename)
        if os.path.exists(fpath):
            with open(fpath,"r") as f:
                json_string = f.read()
                return FXTransactWrapper.fromjsonstring(json_string)
        else:
            return None
        
    # @staticmethod
    # def from_path(filename:str):
    #     try:
    #         with open(filename,"r") as f:
    #             json_string = f.read()
    #             return FXTransactWrapper.fromjsonstring(json_string)
    #     except Exception as e:
    #         print(f"Error reading file: {e}")
    #         return None
    
    def to_path(self, fullpath:str=None,use_local=True):
        if not fullpath:
            filename = self._to_filename()
            fullpath=FXTransactWrapper.mkpath("json",use_local,fn=filename)
        try:
            with open(fullpath, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
      
    
    def tojsonfile(self, filename:str=None,use_local=True):
        if not filename:
            filename = self._to_filename()
        try:
            fpath=FXTransactWrapper.mkpath("json",use_local,fn=filename)
            with open(fpath, 'w') as f:
                f.write(self.tojson())
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def toyamlfile(self, filename:str=None):
        if not filename:
            filename = self._to_filename("yaml")
        if not OUTPUT_YAML_DISABLED:
            try:
                
                with open(filename, 'w') as f:
                    f.write(self.toyaml())
            except Exception as e:
                print(f"Error writing to file: {e}")
    
    @staticmethod
    def fromyamlstring(yaml_string):
        data = yaml.load(yaml_string)
        trades = data.get('trades', [])
        orders = data.get('orders', [])
        return FXTransactWrapper(
            trades=FXTrades(trades),
            orders=FXOrders(orders)
        )
    
    @staticmethod
    def fromjsonstring(json_string):
        data = json.loads(json_string)
        trades = data.get('trades', [])
        orders = data.get('orders', [])
        return FXTransactWrapper(
            trades=FXTrades(trades),
            orders=FXOrders(orders)
        )
    
    
    @staticmethod
    def fromyamlfile(filename:str):
        try:
            with open(filename,"r") as f:
                yaml_string = f.read()
                return FXTransactWrapper.fromyamlstring(yaml_string)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
            

class FXTransactDataHelper:
    
    @staticmethod
    def load_fxtransact_from_file(filename:str):
        return FXTransactWrapper.from_path(filename)
    
    @staticmethod
    def save_fxtransact_to_file(fxtransactwrapper:FXTransactWrapper,str_table:str="all",str_connection:str="",save_prefix:str= "fxtransact_",prefix_to_connection:bool=True,str_order_id=None,str_instrument=None,quiet=True,str_trade_id=None,use_local=True):
        connection_prefix = str_connection.lower()+"_" if prefix_to_connection else ""
        
        fn = connection_prefix+save_prefix
        savefile = fn+".json"
        
        if str_order_id:
            savefile = fn+str_order_id+".json"
        if str_trade_id:
            savefile = fn+str_trade_id+".json"
        if str_instrument:
            savefile = fn+str_instrument.replace("/","-")+".json"
        if str_table == "orders":
            savefile = fn+"orders.json"
        if str_table == "trades":
            savefile = fn+"trades.json"
        
        saved_file_fix = sanitize_filename(savefile)
        
        save_fullpath=jgtfxhelper.mkfn_cfxdata_filepath(saved_file_fix,use_local)
       
        #@STCIssue HOW TO SAVE THE DATA WELL
        #fxtransactwrapper.tojsonfile(save_fullpath)
        fxtransactwrapper.to_path(save_fullpath,use_local)
        if not OUTPUT_YAML_DISABLED:
            fxtransactwrapper.toyamlfile(saved_file_fix.replace(".json",".yaml"))
        if not quiet:print("FXTransact saved to file: "+saved_file_fix)
        return saved_file_fix
    
    @staticmethod
    def save_fxorder_to_file(fxorder:FXOrder,str_connection:str="",save_prefix:str=ORDER_FILE_PREFIX,prefix_to_connection:bool=True,str_order_id=None,str_instrument=None,quiet=True,use_local=True):
        connection_prefix = str_connection.lower()+"_" if prefix_to_connection else ""
        
        fn = connection_prefix+save_prefix
        savefile = fn+".json"
        
        if str_order_id:
            savefile = fn+str_order_id+".json"
        if str_instrument:
            savefile = fn+str_instrument.replace("/","-")+".json"

        saved_file_fix = sanitize_filename(savefile)
        
        save_fullpath=jgtfxhelper.mkfn_cfxdata_filepath(saved_file_fix,use_local)
        
        fxorder.tojsonfile(save_fullpath)
        if not OUTPUT_YAML_DISABLED:
            fxorder.toyamlfile(saved_file_fix.replace(".json",".yaml"))
        if not quiet:print("FXOrder saved to file: "+saved_file_fix)
        return saved_file_fix
    
    @staticmethod
    def save_fxtrade_to_file(fxtrade:FXTrade,str_connection:str="",save_prefix:str=TRADE_FILE_PREFIX,prefix_to_connection:bool=True,str_order_id=None,str_instrument=None,quiet=True,use_local=True):
        connection_prefix = str_connection.lower()+"_" if prefix_to_connection else ""
        
        fn = connection_prefix+save_prefix
        savefile = fn+".json"
        
        if str_order_id:
            savefile = fn+str_order_id+".json"
        if str_instrument:
            savefile = fn+str_instrument.replace("/","-")+".json"

        saved_file_fix = sanitize_filename(savefile)
        save_fullpath=jgtfxhelper.mkfn_cfxdata_filepath(saved_file_fix,use_local)
        
        fxtrade.tojsonfile(save_fullpath)
        if not quiet:print("FXTrade saved to file: "+saved_file_fix)
        return saved_file_fix
    
    @staticmethod
    def load_fxorder_from_file(filename:str):
        try:
            with open(filename,"r") as f:
                json_string = f.read()
                return FXOrder.from_json_string(json_string)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def load_fxorder_from_id(id:str):
        try:
            prefix = ORDER_FILE_PREFIX
            filename=jgtfxhelper.mkfn_cfxdata_filepath(prefix+id+".json")
            if not os.path.exists(filename):
                prefix=FXTRANSAC_FILE_PREFIX+"_"
            if not os.path.exists(filename):
                print("File not found: "+filename)
                return None
            with open(filename,"r") as f:
                json_string = f.read()
                return FXOrder.from_json_string(json_string)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
       
    @staticmethod
    def load_fxtrade_from_file(filename:str):
        try:
            with open(filename,"r") as f:
                json_string = f.read()
                return FXTrade.from_json_string(json_string)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def load_fxorders_from_file(filename:str):
        return FXOrders.from_string(filename)

    @staticmethod
    def load_fxtrades_from_file(filename:str):
        return FXTrades.from_string(filename)
    
    @staticmethod
    def load_fxtrade_from_fxtransact(fxtransact: FXTransactWrapper, str_trade_id) -> FXTrade:
        for trade in fxtransact.trades.trades:
            if str(trade['trade_id']) == str(str_trade_id):
                return trade
        return None
    
    @staticmethod
    def load_fxorder_from_fxtransact(fxtransact: FXTransactWrapper, str_order_id) -> FXOrder:
        for order in fxtransact.orders.orders:
            if str(order['order_id']) == str(str_order_id):
                return order
        return None

