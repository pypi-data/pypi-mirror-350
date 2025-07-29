"""
jgtutils package
"""

version='0.2.222'

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtos import (tlid_range_to_jgtfxcon_start_end_str,
                   tlid_range_to_start_end_datetime)

import jgtcommon as common
import jgtos as jos
import jgtpov as pov
import jgtwslhelper as wsl
from jgtcommon import readconfig,new_parser,parse_args,load_settings,get_settings,dt_from_last_week_as_string_fxformat as dt_from_last_week
from jgtpov import calculate_tlid_range as get_tlid_range
from FXTransact import (FXTransactDataHelper as ftdh,
                        FXTransactWrapper as ftw)

from jgtclihelper import (print_jsonl_message as printl)

from jgtenv import load_dotjgt_env_sh,load_dotjgtset_exported_env,load_dotfxtrade_env,load_env

def load_logging():
  from jgtutils import jgtlogging as jlog
