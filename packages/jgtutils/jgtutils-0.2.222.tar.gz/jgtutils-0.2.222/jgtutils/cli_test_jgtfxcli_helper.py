import os

import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon
import jgtwslhelper as wsl


def refreshPH(instrument:str, timeframe:str,quote_count:int=-1, quiet:bool=True,use_full:bool=False,verbose_level=0,tlid_range=None,keep_bid_ask=False):
  if not quiet:
    print(f"Refreshing {instrument} {timeframe}")
  try:
    wsl.getPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=verbose_level,keep_bid_ask=keep_bid_ask)
  except Exception as e:
    print("Error in refreshPH")
    raise e

def parse_args():
    parser = jgtcommon.new_parser("WSL JGTFxCLI Test settings","Test loading custom settings and launch",enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    #parser=jgtcommon._preload_settings_from_args(parser)
    
    parser= jgtcommon.add_instrument_timeframe_arguments(parser)
    parser=jgtcommon.add_bars_amount_V2_arguments(parser)
    parser=jgtcommon.add_keepbidask_argument(parser)
    parser=jgtcommon.add_tlid_range_argument(parser)
    parser=jgtcommon.add_verbose_argument(parser)
    
    args = jgtcommon.parse_args(parser)
    return args

def main():
    args = parse_args()
    
    #settings = jgtcommon.load_settings(args)
    print("Settings loaded:")
    print(jgtcommon.settings)
    try:
        tlid_range_value = args.tlidrange if args.tlidrange else None
        refreshPH(args.instrument, args.timeframe,quote_count=args.quotescount, quiet=False,use_full=False,verbose_level=args.verbose,tlid_range=tlid_range_value,keep_bid_ask=args.keep_bid_ask)
    except Exception as e:
        print("Error in main")
        raise e
    
if __name__ == '__main__':
    main()
    
