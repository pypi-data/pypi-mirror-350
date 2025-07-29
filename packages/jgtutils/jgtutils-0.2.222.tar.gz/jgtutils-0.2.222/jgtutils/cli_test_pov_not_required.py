import os

import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

def parse_args():
    parser = jgtcommon.new_parser("Timeframe Test settings","Test loading custom timeframes from settings",enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    #parser=jgtcommon._preload_settings_from_args(parser)
    
    parser= jgtcommon.add_instrument_standalone_argument(parser)
    parser= jgtcommon.add_timeframe_standalone_argument(parser)
    
    args = jgtcommon.parse_args(parser)
    return args

from jgtconstants import INSTRUMENTS_DEFAULT, TIMEFRAMES_DEFAULT
def main():
    args = parse_args()
    instruments=jgtcommon.get_instruments(INSTRUMENTS_DEFAULT)
    timeframes=jgtcommon.get_timeframes(TIMEFRAMES_DEFAULT)
    print("instruments:",instruments)
    print("timeframes:",timeframes)
    timeframes2=jgtcommon.get_timeframes(None,"_default_timeframes_a")
    print("_default_timeframes_a:",timeframes2)
    instruments2=jgtcommon.get_instruments(None,"instruments")
    print("instruments2:",instruments2)
    
    
if __name__ == '__main__':
    main()
    
