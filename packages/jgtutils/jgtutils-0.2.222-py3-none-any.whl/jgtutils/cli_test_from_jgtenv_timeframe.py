import os

import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

def parse_args(exclude_env_alias=True):
    parser = jgtcommon.new_parser("Timeframe Test Load from env","Test loading timeframe from env",enable_specified_settings=True)
    
    
    parser= jgtcommon.add_timeframe_standalone_argument(parser,from_jgt_env=True,required=True,exclude_env_alias=exclude_env_alias)
    args = jgtcommon.parse_args(parser)
    return args

def main():
    args = parse_args()
    
    print(args.timeframe)
    
def main_alias():
    args = parse_args(False)
    
    print(args.timeframe)
       
if __name__ == '__main__':
    main()
    
