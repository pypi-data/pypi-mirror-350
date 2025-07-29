import os

import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

def parse_args(exclude_env_alias=True):
    parser = jgtcommon.new_parser("FXTransact Test Load from env","Test loading i/t and transact from env",enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    #parser=jgtcommon._preload_settings_from_args(parser)
    
    parser= jgtcommon.add_instrument_timeframe_arguments(parser,from_jgt_env=True,exclude_env_alias=exclude_env_alias)
    parser= jgtcommon.add_direction_rate_lots_arguments(parser,from_jgt_env=True,exclude_env_alias=exclude_env_alias)
    parser=jgtcommon.add_demo_flag_argument(parser,from_jgt_env=True)
    args = jgtcommon.parse_args(parser)
    return args

def main():
    args = parse_args()
    print_arguments(args)

def print_arguments(args):
    print(args.instrument)
    print(args.timeframe)
    print("Sell" if args.bs=="S" else "Buy" if args.bs=="B" else "Invalid")
    print("rate:",args.rate)
    print("stop:",args.stop)
    print("lots:",args.lots)
    print("Using Demo" if args.demo else "Using real")
    
def main_alias():
    args = parse_args(False)
    print_arguments(args)

if __name__ == '__main__':
    main()
    
