


# Copyright 2019 Gehtsoft USA LLC
# Copyright 2023 JGWill (extended/variations)

# Licensed under the license derived from the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# http://fxcodebase.com/licenses/open-source/license.html

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import ruamel.yaml;yaml = ruamel.yaml.YAML()

import os
import sys
import traceback
#import logging
from datetime import datetime, time, timezone, timedelta
from enum import Enum
from typing import List

import tlid

#------------------------#

# common.py



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtenv import load_env
from jgtpov import i2fn,t2fn,fn2i,fn2t

from jgtos import (tlid_dt_to_string, tlid_range_to_jgtfxcon_start_end_str,
                   tlid_range_to_start_end_datetime, tlidmin_to_dt)

from jgtclihelper import add_exiting_quietly
from jgtcliconstants import (ACCOUNT_ARGNAME, ARG_GROUP_BARS_DESCRIPTION,
                                      ARG_GROUP_BARS_TITLE,
                                      ARG_GROUP_CLEANUP_DESCRIPTION,
                                      ARG_GROUP_CLEANUP_TITLE, ARG_GROUP_INDICATOR_DESCRIPTION, ARG_GROUP_INDICATOR_TITLE,
                                      ARG_GROUP_INTERACTION_DESCRIPTION,
                                      ARG_GROUP_INTERACTION_TITLE,
                                      ARG_GROUP_OUTPUT_DESCRIPTION,
                                      ARG_GROUP_OUTPUT_TITLE,
                                      ARG_GROUP_POV_DESCRIPTION,
                                      ARG_GROUP_POV_TITLE,
                                      ARG_GROUP_RANGE_DESCRIPTION,
                                      ARG_GROUP_RANGE_TITLE,
                                      ARG_GROUP_VERBOSITY_DESCRIPTION,
                                      ARG_GROUP_VERBOSITY_TITLE,
                                      BALLIGATOR_FLAG_ARGNAME,
                                      BALLIGATOR_FLAG_ARGNAME_ALIAS, BUYSELL_ARGNAME, BUYSELL_ARGNAME_ALIAS, DATEFROM_ARGNAME, DATEFROM_ARGNAME_ALIAS, DATETO_ARGNAME, DATETO_ARGNAME_ALIAS,
                                      DONT_DROPNA_VOLUME_FLAG_ARGNAME,
                                      DONT_DROPNA_VOLUME_FLAG_ARGNAME_ALIAS,
                                      DROPNA_VOLUME_FLAG_ARGNAME,
                                      DROPNA_VOLUME_FLAG_ARGNAME_ALIAS,
                                      FRESH_FLAG_ARGNAME,
                                      FRESH_FLAG_ARGNAME_ALIAS,
                                      FULL_FLAG_ARGNAME,
                                      FULL_FLAG_ARGNAME_ALIAS,
                                      GATOR_OSCILLATOR_FLAG_ARGNAME,
                                      GATOR_OSCILLATOR_FLAG_ARGNAME_ALIAS, INPUT_FILE_ARGNAME, INPUT_FILE_ARGNAME_ALIAS, INSTRUMENT_ARGNAME, INSTRUMENT_ARGNAME_ALIAS, JSON_FLAG_ARGNAME, JSON_FLAG_ARGNAME_ALIAS,
                                      KEEP_BID_ASK_FLAG_ARGNAME,
                                      KEEP_BID_ASK_FLAG_ARGNAME_ALIAS, LOTS_ARGNAME, LOTS_ARGNAME_ALIAS, MD_FLAG_ARGNAME, MD_FLAG_ARGNAME_ALIAS,
                                      MFI_FLAG_ARGNAME, MFI_FLAG_ARGNAME_ALIAS,
                                      NO_MFI_FLAG_ARGNAME,
                                      NO_MFI_FLAG_ARGNAME_ALIAS,
                                      NOT_FRESH_FLAG_ARGNAME,
                                      NOT_FRESH_FLAG_ARGNAME_ALIAS,
                                      NOT_FULL_FLAG_ARGNAME,
                                      NOT_FULL_FLAG_ARGNAME_ALIAS, ORDERID_ARGNAME, ORDERID_ARGNAME_ALIAS, OUTPUT_ARGNAME, OUTPUT_ARGNAME_ALIAS, PIPS_ARGNAME, PN_ARGNAME, PN_ARGNAME_ALIAS, PN_COLUMN_LIST_ARGNAME, PN_COLUMN_LIST_ARGNAME_ALIAS, PN_GROUP_NAME, PN_LIST_FLAG_ARGNAME, PN_LIST_FLAG_ARGNAME_ALIAS,
                                      QUOTES_COUNT_ARGNAME,
                                      QUOTES_COUNT_ARGNAME_ALIAS, RATE_ARGNAME, RATE_ARGNAME_ALIAS, REAL_FLAG_ARGNAME,
                                      REMOVE_BID_ASK_FLAG_ARGNAME,
                                      REMOVE_BID_ASK_FLAG_ARGNAME_ALIAS, SELECTED_COLUMNS_ARGNAME, SELECTED_COLUMNS_ARGNAME_ALIAS, SELECTED_COLUMNS_GROUP_NAME, SELECTED_COLUMNS_HELP, STOP_ARGNAME, STOP_ARGNAME_ALIAS,
                                      TALLIGATOR_FLAG_ARGNAME,
                                      TALLIGATOR_FLAG_ARGNAME_ALIAS, TIMEFRAME_ARGNAME, TIMEFRAME_ARGNAME_ALIAS, TLID_DATETO_ARGNAME, TLID_DATETO_ARGNAME_ALIAS,
                                      TLID_RANGE_ARG_DEST, TLID_RANGE_ARGNAME,
                                      TLID_RANGE_ARGNAME_ALIAS,
                                      TLID_RANGE_HELP_STRING, TRADEID_ARGNAME, TRADEID_ARGNAME_ALIAS)

args:argparse.Namespace=None # Default args when we are done parsing
try :
    import __main__

    # logging.basicConfig(filename='{0}.log'.format(__main__.__file__), level=logging.INFO,
    #                 format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
    # console = logging.StreamHandler(sys.stdout)
    # console.setLevel(logging.INFO)
    # logging.getLogger('').addHandler(console)
    

except:
    #print('logging failed - dont worry')
    pass

try :    
    #if __main__ has a .parser then set the default parser to that
    if hasattr(__main__,'parser'):
        default_parser=__main__.parser
    else:
        if hasattr(__main__,'default_parser'):
            default_parser=__main__.default_parser
        else: 
            if hasattr(__main__,'__parser__'):
                default_parser=__main__.__parser__
            else:
                default_parser = argparse.ArgumentParser(description='JGWill Trading Utilities')
except:
    default_parser = argparse.ArgumentParser(description='JGWill Trading Utilities')
    pass



settings: dict = None

# try:
#     #indicator's group
#     indicator_group = default_parser.add_argument_group(INDICATOR_GROUP_TITLE, 'Indicators to use in the processing.')
#     #indicator_group = _get_group_by_title(default_parser, INDICATOR_GROUP_TITLE)
# except:
#     pass

def _load_settings_from_path(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            loaded_data = json.load(f)
            return loaded_data
    return {}

def _load_settings_from_path_yaml(path,key=None):
    if os.path.exists(path):
        with open(path, 'r') as f:
            if key is not None:
                try:
                    yaml_value = yaml.load(f)
                except yaml.YAMLError as exc:
                    print(exc)
                if yaml_value is not None and key in yaml_value:
                    return yaml_value[key]
                else:
                    return {}
            yaml_data = yaml.load(f)
            if yaml_data is None:
                return {}
            return yaml_data
    return {}
def load_settings(custom_path=None,old=None):
    global args
    if custom_path is None and args is not None and hasattr(args,SETTING_ARGNAME):
        custom_path = getattr(args,SETTING_ARGNAME,None)
    
    system_settings_path = os.path.join('/etc', 'jgt', 'settings.json')
    home_settings_path = os.path.join(os.path.expanduser('~'), '.jgt', 'settings.json')
    current_settings_path = os.path.join(os.getcwd(), '.jgt', 'settings.json')
    yaml_current_settings_path = os.path.join(os.getcwd(), '.jgt', 'settings.yml')
    jgt_yaml_current_settings_path = os.path.join(os.getcwd(), 'jgt.yml')
    jubook_jgt_yaml_current_settings_path = os.path.join(os.getcwd(), '_config.yml')
    
    _settings={}
    if old is not None:
        _settings=old
    
    
    system_settings=_load_settings_from_path(system_settings_path)
     # Merge settings
    update_settings(_settings, system_settings)

    #load json from env JGT_SETTINGS if exist
    if 'JGT_SETTINGS_SYSTEM' in os.environ:
        env_settings_system=json.loads(os.environ['JGT_SETTINGS_SYSTEM'])
        update_settings(_settings, env_settings_system)
        
    
    user_settings = _load_settings_from_path(home_settings_path)
     # Merge settings, with user directory settings taking precedence
    update_settings(_settings, user_settings)
    
    if 'JGT_SETTINGS' in os.environ:
        env_settings_user=json.loads(os.environ['JGT_SETTINGS'])
        update_settings(_settings, env_settings_user)
    
    if 'JGT_SETTINGS_USER' in os.environ:
        env_settings_user=json.loads(os.environ['JGT_SETTINGS_USER'])
        update_settings(_settings, env_settings_user)
    
    
    current_settings = _load_settings_from_path(current_settings_path)    
    # Merge settings, with current directory settings taking precedence
    update_settings(_settings, current_settings)
    
    current_settings_yaml = _load_settings_from_path_yaml(yaml_current_settings_path)
    update_settings(_settings, current_settings_yaml)
    
    
    jubook_jgt_current_settings_yaml = _load_settings_from_path_yaml(jubook_jgt_yaml_current_settings_path,key='jgt')
    update_settings(_settings, jubook_jgt_current_settings_yaml)
    
    jgt_current_settings_yaml = _load_settings_from_path_yaml(jgt_yaml_current_settings_path)
    update_settings(_settings, jgt_current_settings_yaml)
    
    if custom_path is not None and custom_path != '':
        custom_settings={}
        if '.json' in custom_path:
            custom_settings = _load_settings_from_path(custom_path)
        else:
            if '.yml' in custom_path:
                custom_settings = _load_settings_from_path_yaml(custom_path)
        update_settings(_settings, custom_settings)
    
    if 'JGT_SETTINGS_PROCESS' in os.environ:
        env_settings_process=json.loads(os.environ['JGT_SETTINGS_PROCESS'])
        update_settings(_settings,env_settings_process )
    
    _settings_loaded(_settings)
    
    return _settings

def update_settings(old_settings, new_settings,keys=['patterns']):
    #if our old settings has a key in our keys list, then we will update it on their own (meaning we will not merge it directly but update it independently)
    for key in keys:
        if key in old_settings:
            tst_key_value_old=old_settings[key]
            if new_settings is not None and key in new_settings:
                test_if_key_not_none = new_settings[key]
                if test_if_key_not_none is not None:
                    old_settings[key].update(new_settings[key])
                #new_settings.pop(key)
                tst_key_value_new=old_settings[key]
                #remove the key from the new settings
                new_settings.pop(key)
                #print("Updated key: "+key)
    if new_settings is not None:
        old_settings.update(new_settings)
    #print("Updated settings")

def _settings_loaded(_settings):
    return

def get_settings(custom_path=None)->dict:
    global settings
    if settings is None or len(settings)==0:
        settings = load_settings(custom_path=custom_path)
    return settings

def load_arg_default_from_settings(argname:str,default_value,alias:str=None,from_jgt_env=False,exclude_env_alias=False):
    global settings
    if settings is None or len(settings)==0:
        settings=load_settings()
    
    _value = settings.get(argname,default_value)
    if alias is not None and _value==default_value:
        _value = settings.get(alias,default_value) #try alias might be used
    
    if from_jgt_env:
        _alias=None if exclude_env_alias else alias
        _value = load_arg_from_jgt_env(argname, _alias)
    
    return _value

def load_arg_from_jgt_env(argname, alias=None):
    _value=None
    loaded=load_env()
        #if loaded:
    if argname in os.environ :
        #or alias in os.environ:
        _value = os.getenv(argname,None)
    if alias is not None and _value is None:
        _value = os.getenv(alias,None)
    return _value

def load_arg_default_from_settings_if_exist(argname:str,alias:str=None):
    global settings
    if settings is None or len(settings)==0:
        settings=load_settings()
    
    _value = settings.get(argname,None)
    if alias is not None and _value==None:
        _value = settings.get(alias,None) #try alias might be used
    return _value

def add_settings_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    try:
        parser.add_argument('-'+SETTING_ARGNAME_ALIAS,'--'+SETTING_ARGNAME,
                        type=str,
                            help='Load settings from a specific settings file (overrides default settings (/etc/jgt/settings.json and HOME/.jgt/settings.json and .jgt/settings.json)).',
                            required=False)
    #argparse.ArgumentError: argument -ls/--settings: conflicting option strings: -ls, --settings
    except argparse.ArgumentError as e:
        if not 'argument -ls/--settings: conflicting option strings: -ls, --settings' in str(e):
            raise e
        pass

    return parser

def _preload_settings_from_args(parser: argparse.ArgumentParser=None):
    global default_parser,settings
    if parser is None:
        parser=default_parser
    
    args, unknown = parser.parse_known_args()
    custom_path = getattr(args,SETTING_ARGNAME,None)
    settings = load_settings(custom_path)
    
    return parser

def new_parser(description: str,epilog: str=None,prog: str=None,enable_specified_settings=True,add_exiting_quietly_flag=False,exiting_quietly_message:str=None,exiting_quietly_handler=None)->argparse.ArgumentParser:
    global default_parser
    if add_exiting_quietly_flag or exiting_quietly_handler is not None:
        #print("We are adding exiting quietly")
        add_exiting_quietly(exiting_quietly_message,exiting_quietly_handler)
        
    default_parser = argparse.ArgumentParser(description=description,epilog=epilog,prog=prog)
    
    if enable_specified_settings:
        default_parser=add_settings_argument(default_parser)
        if not '--help' in sys.argv:
            default_parser=_preload_settings_from_args(default_parser)
    
    return default_parser

# Get a group by its title
def _get_group_by_title(parser, title,description=""):
    for group in parser._action_groups:
        if group.title == title:
            return group
    #create it
    return parser.add_argument_group(title, description)


def init_default_parser(description: str):
    global default_parser
    default_parser = argparse.ArgumentParser(description=description)
    return default_parser




def _add_a_flag_helper(_description:str,  _argname_alias:str, _argname_full:str, parser: argparse.ArgumentParser,_action_value="store_true",group_title="",group_description="",load_default_from_settings=True,flag_default_value=False):


    __alias_cmd_prefix = "-"
    __full_arg_prefix = "--"
    
    __flag_setting_value=load_arg_default_from_settings(_argname_full,flag_default_value)
    
    _argname_alias = __alias_cmd_prefix+_argname_alias
    _argname_full = __full_arg_prefix+_argname_full
    if group_title=="":
        parser.add_argument(
        _argname_alias,
        _argname_full,
        action=_action_value,
        help=_description,
        default=__flag_setting_value
        )
    else:
        #try get group name or create it.
        group = _get_group_by_title(parser, group_title,group_description)
        group.add_argument(
            _argname_alias,
            _argname_full,
            action=_action_value,
            help=_description,
            default=__flag_setting_value
        )
    
    return parser






def add_main_arguments(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('--login',
                        metavar="LOGIN",
                        required=True,
                        help='Your user name.')

    parser.add_argument('--password',
                        metavar="PASSWORD",
                        required=True,
                        help='Your password.')

    parser.add_argument('--urlserver',
                        metavar="URL",
                        required=True,
                        help='The server URL. For example,\
                                 https://www.fxcorporate.com/Hosts.jsp.')

    parser.add_argument('--connection',
                        metavar="CONNECTION",
                        required=True,
                        help='The connection name. For example, \
                                 "Demo" or "Real".')


    parser.add_argument('-session',
                        help='The database name. Required only for users who\
                                 have accounts in more than one database.\
                                 Optional parameter.')

    parser.add_argument('-pin',
                        help='Your pin code. Required only for users who have \
                                 a pin. Optional parameter.')
    return parser

def add_candle_open_price_mode_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument('--openpricemode',
                        metavar="CANDLE_OPEN_PRICE_MODE",
                        default="prev_close",
                        help='Ability to set the open price candles mode. \
                        Possible values are first_tick, prev_close. For more information see description \
                        of O2GCandleOpenPriceMode enumeration. Optional parameter.')
    return parser

from jgtcliconstants import (DEMO_FLAG_ARGNAME)

def add_demo_flag_argument(parser: argparse.ArgumentParser=None,load_default_from_settings=True,flag_default_value=False,from_jgt_env=False)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    type_of_account_group=_get_group_by_title(parser,"Type of Account","Real or Demo")
    
    demo_value = load_arg_default_from_settings_if_exist(DEMO_FLAG_ARGNAME,"demo_arg") 
    if from_jgt_env:
        demo_value = load_arg_from_jgt_env(DEMO_FLAG_ARGNAME,"demo_arg")
    #if load_default_from_settings else flag_default_value
    real_value = load_arg_default_from_settings_if_exist(REAL_FLAG_ARGNAME) 
    if from_jgt_env:
        real_value = load_arg_from_jgt_env(REAL_FLAG_ARGNAME)
    
    #turn "--demo" into True
    if demo_value is not None and isinstance(demo_value,str) :
        _value:str=demo_value
        if _value.lower() == "true" or _value.lower() == "1" or _value.lower() == "--demo" or _value.lower() == "-demo" or _value.lower() == "demo":
            demo_value=True
        elif _value.lower() == "false" or _value.lower() == "0" or _value.lower() == "--real" or _value.lower() == "-real" or _value.lower() == "real":
            demo_value=False
    #support real=1 or real=0
    if real_value is not None and isinstance(real_value,str) :
        if real_value.lower() == "true" or real_value.lower() == "1" or real_value.lower() == "--real" or real_value.lower() == "-real" or real_value.lower() == "real":
            real_value=True
        elif real_value.lower() == "false" or real_value.lower() == "0" or real_value.lower() == "--demo" or real_value.lower() == "-demo" or real_value.lower() == "demo":
            real_value=False
            
    if real_value is not None and real_value:
        demo_value=False
    elif real_value is not None and not real_value:
        demo_value=True
    
    
    
    type_of_excl=type_of_account_group.add_mutually_exclusive_group()
    type_of_excl.add_argument('-'+DEMO_FLAG_ARGNAME,'--'+DEMO_FLAG_ARGNAME,
                        action='store_true',
                        help='Use the demo server. Optional parameter.',
                        default=demo_value)
    type_of_excl.add_argument('-'+REAL_FLAG_ARGNAME,'--'+REAL_FLAG_ARGNAME,
                        action='store_true',
                        help='Use the real server. Optional parameter.',
                        default=real_value)
    return parser

def add_instrument_timeframe_arguments(parser: argparse.ArgumentParser=None, timeframe: bool = True,load_instrument_from_settings=True,load_timeframe_from_settings=True, from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    
    global default_parser
    instrument_required=True
    
    if parser is None:
        parser=default_parser
    pov_group=_get_group_by_title(parser,ARG_GROUP_POV_TITLE,ARG_GROUP_POV_DESCRIPTION)
    instrument_setting_value=None 
    if load_instrument_from_settings :
        instrument_setting_value=load_arg_default_from_settings(INSTRUMENT_ARGNAME,None,alias=INSTRUMENT_ARGNAME_ALIAS)
    if from_jgt_env: #Cascade to env with no alias by default
        instrument_alias = INSTRUMENT_ARGNAME_ALIAS if not exclude_env_alias else None # we wont load from env var "i" by default
        instrument_setting_value= load_arg_from_jgt_env(INSTRUMENT_ARGNAME,instrument_alias)
    
    if instrument_setting_value is not None:
        instrument_required=False
    
    pov_group.add_argument('-'+INSTRUMENT_ARGNAME_ALIAS,'--'+INSTRUMENT_ARGNAME,
                        metavar="INSTRUMENT",
                        help='An instrument which you want to use in sample. \
                                  For example, "EUR/USD".',
                                  default=instrument_setting_value,
                                  required=instrument_required)

    if timeframe:
        timeframe_required=True
        timeframe_setting_value=None 
        if load_timeframe_from_settings :
            timeframe_setting_value=load_arg_default_from_settings(TIMEFRAME_ARGNAME,None,alias=TIMEFRAME_ARGNAME_ALIAS)
        if from_jgt_env:
            timeframe_alias = TIMEFRAME_ARGNAME_ALIAS if not exclude_env_alias else None
            timeframe_setting_value= load_arg_from_jgt_env(TIMEFRAME_ARGNAME,timeframe_alias)
        if timeframe_setting_value is not None:
            timeframe_required=False
            
        pov_group.add_argument('-'+TIMEFRAME_ARGNAME_ALIAS,'--'+TIMEFRAME_ARGNAME,
                            metavar="TIMEFRAME",
                            help='Time period which forms a single candle. \
                                      For example, m1 - for 1 minute, H1 - for 1 hour.',
                                      default=timeframe_setting_value,
                                      required=timeframe_required)

    return parser

def add_instrument_standalone_argument(parser: argparse.ArgumentParser=None,load_from_settings=True,required=False,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    instrument_value=None
    if load_from_settings :   
        instrument_value=load_arg_default_from_settings(INSTRUMENT_ARGNAME,None,INSTRUMENT_ARGNAME_ALIAS,from_jgt_env=False)
    if from_jgt_env: #Cascade to env with no alias by default
        instrument_value= load_arg_from_jgt_env(INSTRUMENT_ARGNAME,INSTRUMENT_ARGNAME_ALIAS if not exclude_env_alias else None) 
    
    if instrument_value is not None:
        required=False #We might read it from env
    parser.add_argument('-'+INSTRUMENT_ARGNAME_ALIAS,'--'+INSTRUMENT_ARGNAME,
                        metavar="INSTRUMENT",
                        help='An instrument which you want to use in sample. \
                                  For example, "EUR/USD".',
                                  default=instrument_value,
                                  required=required)
    return parser

TIMEFRAME_DEFAULT_STANDALONE = "D1"
def add_timeframe_standalone_argument(parser: argparse.ArgumentParser=None,load_from_settings=True,required=False,load_default_timeframe=False,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    timeframe_value=None
    if load_from_settings :
        timeframe_value=load_arg_default_from_settings(TIMEFRAME_ARGNAME,TIMEFRAME_DEFAULT_STANDALONE if load_default_timeframe else None,TIMEFRAME_ARGNAME_ALIAS,from_jgt_env=False) 
    
    if from_jgt_env: #Cascade to env with no alias by default
        timeframe_value= load_arg_from_jgt_env(TIMEFRAME_ARGNAME,TIMEFRAME_ARGNAME_ALIAS if not exclude_env_alias else None)
    
    if timeframe_value is not None:
        required=False #We might read it from env
    parser.add_argument("-"+TIMEFRAME_ARGNAME_ALIAS,"--"+TIMEFRAME_ARGNAME, help="Timeframe", default=timeframe_value, required=required)
    return parser


def add_direction_buysell_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True, required=True,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    bs_value=None
    if load_from_settings :
        bs_value=load_arg_default_from_settings(BUYSELL_ARGNAME,None,BUYSELL_ARGNAME_ALIAS,from_jgt_env=False) 
    if from_jgt_env: #Cascade to env with no alias by default
        bs_value= load_arg_from_jgt_env(BUYSELL_ARGNAME,BUYSELL_ARGNAME_ALIAS if not exclude_env_alias else None)
        #support env var direction
        # if bs_value is None:
        #     bs_value=load_arg_from_jgt_env("direction")
        
    if bs_value is not None:
        required=False
        if isinstance(bs_value,str) and  bs_value.lower() =="sell":
            bs_value="S"
        elif isinstance(bs_value,str) and  bs_value.lower() =="buy":
            bs_value="B"
    
    
    parser.add_argument('-'+BUYSELL_ARGNAME_ALIAS,'--'+BUYSELL_ARGNAME, metavar="TYPE", required=required,
                        help='The order direction. Possible values are: B - buy, S - sell.',default=bs_value)
    return parser

def add_rate_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True, required=True,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    rate_value=None
    if load_from_settings :
        rate_value=load_arg_default_from_settings(RATE_ARGNAME,None,RATE_ARGNAME_ALIAS,from_jgt_env=False) 
    if from_jgt_env: #Cascade to env with no alias by default
        rate_value= load_arg_from_jgt_env(RATE_ARGNAME,RATE_ARGNAME_ALIAS if not exclude_env_alias else None)
        
    
    if rate_value is not None:
        required=False
        if isinstance(rate_value,str):
            rate_value=float(rate_value)
    
    parser.add_argument('-'+RATE_ARGNAME_ALIAS,'--'+RATE_ARGNAME, metavar="RATE", required=required, type=float,
                            help='Desired price of an entry order.',
                            default=rate_value)
    return parser

def add_stop_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True,pips_flag=False,required=True,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    stop_value=None
    if load_from_settings :
        stop_value=load_arg_default_from_settings(STOP_ARGNAME,None,STOP_ARGNAME_ALIAS) 
    if from_jgt_env: #Cascade to env with no alias by default
        stop_value= load_arg_from_jgt_env(STOP_ARGNAME,STOP_ARGNAME_ALIAS if not exclude_env_alias else None)
    
    if stop_value is not None:
        required=False
        if isinstance(stop_value,str):
            stop_value=float(stop_value)
                          
    parser.add_argument('-'+STOP_ARGNAME_ALIAS,'-'+STOP_ARGNAME,'--'+STOP_ARGNAME, metavar="STOP", required=required, type=float,
                            help='Desired price of the stop order.',
                            default=stop_value)
    if pips_flag:
        pips_value=load_arg_default_from_settings(PIPS_ARGNAME,False,from_jgt_env=from_jgt_env) if load_from_settings else False
        parser.add_argument('-'+PIPS_ARGNAME,'--'+PIPS_ARGNAME,
                        action='store_true',
                        help='The value is in pips. Optional parameter.',default=pips_value)
    return parser

def add_lots_arguments(parser,load_from_settings=True,default_value = 1,from_jgt_env=False,exclude_env_alias=True):
    global default_parser
    if parser is None:
        parser=default_parser
    
    lots_value=default_value
    if load_from_settings :
        lots_value=load_arg_default_from_settings(LOTS_ARGNAME,default_value,LOTS_ARGNAME_ALIAS) 
    if from_jgt_env: #Cascade to env with no alias by default
        _lots_value= load_arg_from_jgt_env(LOTS_ARGNAME,LOTS_ARGNAME_ALIAS if not exclude_env_alias else None)
        lots_value=_lots_value if _lots_value is not None else lots_value
    
    if isinstance(lots_value,str):
        lots_value=int(lots_value)
        
    parser.add_argument('-'+LOTS_ARGNAME_ALIAS,'-'+LOTS_ARGNAME,'--'+LOTS_ARGNAME, metavar="LOTS", default=lots_value, type=int,
                            help='Trade amount in lots.')

def add_direction_rate_lots_arguments(parser: argparse.ArgumentParser=None, direction: bool = True, rate: bool = True,
                                      lots: bool = True, stop: bool = True,load_from_settings=True,lots_default_value=1,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser

    if direction:
        add_direction_buysell_arguments(parser,load_from_settings,from_jgt_env=from_jgt_env,exclude_env_alias=exclude_env_alias)
    if rate:
        add_rate_arguments(parser,load_from_settings,from_jgt_env=from_jgt_env,exclude_env_alias=exclude_env_alias)
    if lots:
        add_lots_arguments(parser,load_from_settings,lots_default_value,from_jgt_env=from_jgt_env,exclude_env_alias=exclude_env_alias)
    if stop:
        add_stop_arguments(parser,load_from_settings,from_jgt_env=from_jgt_env,exclude_env_alias=exclude_env_alias)
    
    return parser


def add_orderid_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True,required=True,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    orderid_value=None
    if load_from_settings :
        orderid_value=load_arg_default_from_settings(ORDERID_ARGNAME,None,ORDERID_ARGNAME_ALIAS) 
    
    if from_jgt_env: #Cascade to env with no alias by default
        orderid_value= load_arg_from_jgt_env(ORDERID_ARGNAME,ORDERID_ARGNAME_ALIAS if not exclude_env_alias else None)
        #support order_id
        if orderid_value is None:
            orderid_value=load_arg_from_jgt_env("order_id")
        #OrderID
        if orderid_value is None:
            orderid_value=load_arg_from_jgt_env("OrderID")
    
    if orderid_value is not None:
        required=False
    
    parser.add_argument('-'+ORDERID_ARGNAME_ALIAS,'--'+ORDERID_ARGNAME, metavar="OrderID", required=required,
                        help='The order identifier.',
                        default=orderid_value)
    return parser

def add_tradeid_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True,required=False,from_jgt_env=False,exclude_env_alias=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    tradeid_value=None
    if load_from_settings :
        tradeid_value=load_arg_default_from_settings(TRADEID_ARGNAME,None,TRADEID_ARGNAME_ALIAS) 
    if from_jgt_env: #Cascade to env with no alias by default
        tradeid_value= load_arg_from_jgt_env(TRADEID_ARGNAME,TRADEID_ARGNAME_ALIAS if not exclude_env_alias else None)
        if tradeid_value is None:
            tradeid_value=load_arg_from_jgt_env("trade_id")
        if tradeid_value is None:
            tradeid_value=load_arg_from_jgt_env("TradeID")
    
    if tradeid_value is not None:
        required=False
        
    parser.add_argument('-'+TRADEID_ARGNAME_ALIAS,'--'+TRADEID_ARGNAME, metavar="TradeID", required=required,
                        help='The trade identifier.',
                        default=tradeid_value)
    return parser


def add_account_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True,required=False)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    account_value=load_arg_default_from_settings(ACCOUNT_ARGNAME,None) if load_from_settings else None
    parser.add_argument('-'+ACCOUNT_ARGNAME, metavar="ACCOUNT",
                        help='An account which you want to use in sample.',default=account_value,required=required)
    return parser


def str_to_datetime(date_str):
    formats = ['%m.%d.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d', '%Y-%m-%d']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def valid_datetime(check_future: bool):
    def _valid_datetime(str_datetime: str):
        date_format = '%m.%d.%Y %H:%M:%S'
        try:
            result = datetime.strptime(str_datetime, date_format).replace(
                tzinfo=timezone.utc)
            if check_future and result > datetime.utcnow().replace(tzinfo=timezone.utc):
                msg = "'{0}' is in the future".format(str_datetime)
                raise argparse.ArgumentTypeError(msg)
            return result
        except ValueError:
            now = datetime.now()
            msg = "The date '{0}' is invalid. The valid data format is '{1}'. Example: '{2}'".format(
                str_datetime, date_format, now.strftime(date_format))
            raise argparse.ArgumentTypeError(msg)
    return _valid_datetime

def add_tlid_date_to_argumments(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    #--ttlid which transform into to_dt
    tlid_dateto_value=load_arg_default_from_settings(TLID_DATETO_ARGNAME,None,TLID_DATETO_ARGNAME_ALIAS) if load_from_settings else None
    parser.add_argument('-'+TLID_DATETO_ARGNAME_ALIAS,'--'+TLID_DATETO_ARGNAME, metavar="TLID",
                        help='The last dateto in TLID format',
                        default=tlid_dateto_value)
    return parser

def add_tlid_date_V2_arguments(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    group1 = parser.add_argument_group('Group 1 (TLID Range)')
    g1x=group1.add_mutually_exclusive_group()
    g1x.add_argument('-'+TLID_RANGE_ARGNAME_ALIAS,'--'+TLID_RANGE_ARGNAME_ALIAS, '--'+TLID_RANGE_ARGNAME, type=str, required=False, dest=TLID_RANGE_ARG_DEST,
                        help=TLID_RANGE_HELP_STRING)
    g2x=g1x.add_mutually_exclusive_group()
    
    raise Exception("Not implemented - Complicated")
    
    #group1.
    #dt_range_group=parser.add_mutually_exclusive_group()
    #dt_range_group.add_argument('-r', '--range', type=str, required=False, dest='tlidrange',
    #                    help='TLID range in the format YYMMDDHHMM_YYMMDDHHMM.')
    # Second group of arguments
    group2 = parser.add_argument_group('Group 2 (Dates)')
    group2.add_argument('-s', '--datefrom', metavar='"m.d.Y H:M:S"',
                        help='Date/time from which you want to receive historical prices.',
                        type=valid_datetime(True),required=False)
    group2.add_argument('-e', '--dateto', metavar='"m.d.Y H:M:S"',
                        help='Datetime until which you want to receive historical prices.',
                        type=valid_datetime(False),required=False)
    
    # Exclusivity between the two groups
    group1_xor_group2 = parser.add_mutually_exclusive_group()
    group1_xor_group2.add_argument('-r', '--range', dest='tlidrange', action='store_true')
    
    group2x=group1_xor_group2.add_mutually_exclusive_group()
    group2x.add_argument('-s', '--datefrom', dest='tlidrange', action='store_false')
    group2x.add_argument('-e', '--dateto', dest='tlidrange', action='store_false')
    
    
    return parser


def add_tlid_range_argument(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    #print("Tlid range active")
    group_range=_get_group_by_title(parser,ARG_GROUP_RANGE_TITLE,ARG_GROUP_RANGE_DESCRIPTION)
    tlid_value=load_arg_default_from_settings(TLID_RANGE_ARGNAME,None,TLID_RANGE_ARGNAME_ALIAS) if load_from_settings else None
    group_range.add_argument('-'+TLID_RANGE_ARGNAME_ALIAS, '--'+TLID_RANGE_ARGNAME_ALIAS,'--'+TLID_RANGE_ARGNAME, type=str, required=False, dest=TLID_RANGE_ARG_DEST,
                        help=TLID_RANGE_HELP_STRING)
    return parser

def add_date_arguments(parser: argparse.ArgumentParser=None, date_from: bool = True, date_to: bool = True,load_from_settings=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    group_range=_get_group_by_title(parser,ARG_GROUP_RANGE_TITLE,ARG_GROUP_RANGE_DESCRIPTION)
    
    if date_from:
        date_from_value=load_arg_default_from_settings(DATEFROM_ARGNAME,None,DATEFROM_ARGNAME_ALIAS) if load_from_settings else None
        group_range.add_argument('-'+DATEFROM_ARGNAME_ALIAS,'--'+DATEFROM_ARGNAME,
                            metavar="\"m.d.Y H:M:S\"",
                            help='Date/time from which you want to receive\
                                      historical prices. If you leave this argument as it \
                                      is, it will mean from last trading day. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True),
                            default=date_from_value
                            )
    if date_to:
        date_to_value=load_arg_default_from_settings(DATETO_ARGNAME,None,DATETO_ARGNAME_ALIAS) if load_from_settings else None
        group_range.add_argument('-'+DATETO_ARGNAME_ALIAS,'--'+DATETO_ARGNAME,
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      historical prices. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(False),
                            default=date_to_value
        )
    return parser


def add_report_date_arguments(parser: argparse.ArgumentParser=None, date_from: bool = True, date_to: bool = True):
    global default_parser
    if parser is None:
        parser=default_parser
    group_range=_get_group_by_title(parser,ARG_GROUP_RANGE_TITLE,ARG_GROUP_RANGE_DESCRIPTION)
    if date_from:
        group_range.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime from which you want to receive\
                                      combo account statement report. If you leave this argument as it \
                                      is, it will mean from last month. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        group_range.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      combo account statement report. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(True)
        )
    return parser


def add_max_bars_arguments(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    group_bars=_get_group_by_title(parser,ARG_GROUP_BARS_TITLE,ARG_GROUP_BARS_DESCRIPTION)
    print("DEPRECATION: Use: add_bars_amount_V2_arguments intead of add_max_bars_arguments and add_use_full_argument")
    group_bars.add_argument('-'+QUOTES_COUNT_ARGNAME_ALIAS,'--'+QUOTES_COUNT_ARGNAME,
                        metavar="MAX",
                        default=-1,
                        type=int,
                        help='Max number of bars. 0 - Not limited')
    
    return parser

def add_bars_amount_V2_arguments(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    #help='Specify the number of bars to download or use the full number of bars available from the store.'
    bars_group=_get_group_by_title(parser,ARG_GROUP_BARS_TITLE,ARG_GROUP_BARS_DESCRIPTION)
    #g=parser.add_argument_group('Bars Amount', 'Specify the number of bars to download or use the full number of bars available from the store.')
    bars_exclusive_subgroup=bars_group.add_mutually_exclusive_group()
    
    quotescount_value=load_arg_default_from_settings(QUOTES_COUNT_ARGNAME,-1,QUOTES_COUNT_ARGNAME_ALIAS) if load_from_settings else -1
    bars_exclusive_subgroup.add_argument('-'+QUOTES_COUNT_ARGNAME_ALIAS,'--'+QUOTES_COUNT_ARGNAME,
                        metavar="MAX",
                        default=quotescount_value,
                        type=int,
                        help='Max number of bars. 0 - Not limited')
    g_full_notfull=bars_exclusive_subgroup.add_mutually_exclusive_group()
    use_full_value=load_arg_default_from_settings(FULL_FLAG_ARGNAME,False,FULL_FLAG_ARGNAME_ALIAS) if load_from_settings else False
    g_full_notfull.add_argument('-'+FULL_FLAG_ARGNAME_ALIAS,'--'+FULL_FLAG_ARGNAME,
                        action='store_true',
                        help='Output/Input uses the full store. ',
                        default=use_full_value)
    g_full_notfull.add_argument('-'+NOT_FULL_FLAG_ARGNAME_ALIAS,'--'+NOT_FULL_FLAG_ARGNAME,
                        action='store_true',
                        help='Output/Input uses NOT the full store. ',
                        default=not use_full_value)
    return parser


def add_output_argument(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    """
    Adds an output argument to the given argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.

    Returns:
        parser (argparse.ArgumentParser): The argument parser with the output argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser

    output_value=load_arg_default_from_settings(OUTPUT_ARGNAME,None,OUTPUT_ARGNAME_ALIAS) if load_from_settings else None
    parser.add_argument('-'+OUTPUT_ARGNAME_ALIAS,'--'+OUTPUT_ARGNAME,
                        help='Output PATH. ',
                        default=output_value)
    
    return parser

def add_input_file_argument(parser: argparse.ArgumentParser=None,load_from_settings=True,add_f_alias=False)->argparse.ArgumentParser:
    """
    Adds an input file argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the input file argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with the input file argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    
    input_file_value=load_arg_default_from_settings(INPUT_FILE_ARGNAME,None,INPUT_FILE_ARGNAME_ALIAS) if load_from_settings else None
    if add_f_alias:parser.add_argument('-f','-'+INPUT_FILE_ARGNAME_ALIAS,'--'+INPUT_FILE_ARGNAME,
                        help='Input file PATH. ',
                        default=input_file_value)
    else:
        parser.add_argument('-'+INPUT_FILE_ARGNAME_ALIAS,'--'+INPUT_FILE_ARGNAME,
                        help='Input file PATH. ',
                        default=input_file_value)
    
    return parser

def add_compressed_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    """
    Adds an compressed argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    group_output=_get_group_by_title(parser,ARG_GROUP_OUTPUT_TITLE,ARG_GROUP_OUTPUT_DESCRIPTION)
    group_output.add_argument('-z','--compress',
                        action='store_true',
                        help='Compress the output. If specified, it will also activate the output flag.')
    return parser


def add_use_full_argument(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    """
    Adds a use full argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the read full argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    
    #print("DEPRECATION: Use: add_bars_amount_V2_arguments")
    full_notfull_group = parser.add_mutually_exclusive_group()
    use_full_value=load_arg_default_from_settings(FULL_FLAG_ARGNAME,False,FULL_FLAG_ARGNAME_ALIAS) if load_from_settings else False
    full_notfull_group.add_argument('-'+FULL_FLAG_ARGNAME_ALIAS,'--'+FULL_FLAG_ARGNAME,
                        action='store_true',
                        help='Output/Input uses the full store. ',
                        default=use_full_value)
    full_notfull_group.add_argument('-'+NOT_FULL_FLAG_ARGNAME_ALIAS,'--'+NOT_FULL_FLAG_ARGNAME,
                        action='store_true',
                        help='Output/Input uses NOT the full store. ',
                        default=not use_full_value)
 
    return parser

def add_use_fresh_argument(parser: argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
    """
    Adds a use fresh argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the use fresh argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    bars_group=_get_group_by_title(parser,ARG_GROUP_BARS_TITLE,ARG_GROUP_BARS_DESCRIPTION)
    
    fresh_old_group=bars_group.add_mutually_exclusive_group()
    use_fresh_value=load_arg_default_from_settings(FRESH_FLAG_ARGNAME,False,FRESH_FLAG_ARGNAME_ALIAS) if load_from_settings else False
    fresh_old_group.add_argument('-'+FRESH_FLAG_ARGNAME_ALIAS,'--'+FRESH_FLAG_ARGNAME,
                        action='store_true',
                        help='Freshening the storage with latest market. ',
                        default=use_fresh_value)
    fresh_old_group.add_argument('-'+NOT_FRESH_FLAG_ARGNAME_ALIAS,'--'+NOT_FRESH_FLAG_ARGNAME,
                        action='store_true',
                        help='Output/Input wont be freshed from storage (weekend or tests). ',
                        default=not use_fresh_value)
 
    return parser


def add_keepbidask_argument(parser: argparse.ArgumentParser=None,load_default_from_settings=True,flag_default_value=True)->argparse.ArgumentParser:
    """
    Adds a keep Bid/Ask argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the keep bid/ask argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with the argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    
    cleanupGroup=_get_group_by_title(parser,ARG_GROUP_CLEANUP_TITLE,ARG_GROUP_CLEANUP_DESCRIPTION)
    group_kba=cleanupGroup.add_mutually_exclusive_group()
    
    default_value = load_arg_default_from_settings(KEEP_BID_ASK_FLAG_ARGNAME,flag_default_value,alias=KEEP_BID_ASK_FLAG_ARGNAME_ALIAS) if load_default_from_settings else flag_default_value
    #print("keepbidask  value:"+str(default_value))
    group_kba.add_argument('-'+KEEP_BID_ASK_FLAG_ARGNAME_ALIAS,'--'+KEEP_BID_ASK_FLAG_ARGNAME,
                        action='store_true',
                        help='Keep Bid/Ask in storage. ',
                        default=default_value)
    group_kba.add_argument('-'+REMOVE_BID_ASK_FLAG_ARGNAME_ALIAS,'--'+REMOVE_BID_ASK_FLAG_ARGNAME,
                        action='store_true',
                        help='Remove Bid/Ask in storage. ',
                        default=not default_value)
    return parser

def add_format_outputs_arguments(parser:argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
  global default_parser
  if parser is None:
    parser=default_parser
  
  out_group=_get_group_by_title(parser,"Outputs")
  json_flag_default_value=load_arg_default_from_settings(JSON_FLAG_ARGNAME,False,JSON_FLAG_ARGNAME_ALIAS) if load_from_settings else False
  f_exclusive=out_group.add_mutually_exclusive_group()
  f_exclusive.add_argument("-"+JSON_FLAG_ARGNAME_ALIAS, "--"+JSON_FLAG_ARGNAME_ALIAS, "--"+JSON_FLAG_ARGNAME, help="Output in JSON format", action="store_true",default=json_flag_default_value,dest=JSON_FLAG_ARGNAME)
  #Markdown
  
  markdown_flag_default_value=load_arg_default_from_settings(MD_FLAG_ARGNAME,False,MD_FLAG_ARGNAME_ALIAS) if load_from_settings else False
  f_exclusive.add_argument("-"+MD_FLAG_ARGNAME_ALIAS, "--"+MD_FLAG_ARGNAME, help="Output in Markdown format", action="store_true",default=markdown_flag_default_value)
  return parser

def add_patterns_arguments(parser:argparse.ArgumentParser=None,load_from_settings=True,required=True,from_jgt_env=False)->argparse.ArgumentParser:
  global default_parser
  if parser is None:
    parser=default_parser
  
  
  pn_group=_get_group_by_title(parser,PN_GROUP_NAME)

  clh_default_value=load_arg_default_from_settings(PN_COLUMN_LIST_ARGNAME,None,PN_COLUMN_LIST_ARGNAME_ALIAS) if load_from_settings else None
  pn_group.add_argument("-"+PN_COLUMN_LIST_ARGNAME_ALIAS, "--"+PN_COLUMN_LIST_ARGNAME, nargs='+', help="List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao", default=clh_default_value)
  

  
  pn_default_value=load_arg_default_from_settings(PN_ARGNAME,None,PN_ARGNAME_ALIAS,from_jgt_env=from_jgt_env) if load_from_settings or from_jgt_env else None
  if pn_default_value is not None:
      required=False
      
  pn_group.add_argument("-"+PN_ARGNAME_ALIAS, "--"+PN_ARGNAME, help="Pattern Name",default=pn_default_value,required=required)
  
  pn_group.add_argument("-"+PN_LIST_FLAG_ARGNAME_ALIAS, "--"+PN_LIST_FLAG_ARGNAME, help="List Patterns", action="store_true")
  
  #Add the format outputs
  parser=add_format_outputs_arguments(parser,load_from_settings)
  return parser



def add_selected_columns_arguments(parser:argparse.ArgumentParser=None,load_from_settings=True)->argparse.ArgumentParser:
  global default_parser
  if parser is None:
    parser=default_parser
  
  
  sc_group=_get_group_by_title(parser,SELECTED_COLUMNS_GROUP_NAME)

  sc_default_value=load_arg_default_from_settings(SELECTED_COLUMNS_ARGNAME,None,SELECTED_COLUMNS_ARGNAME_ALIAS) if load_from_settings else None
  
  sc_group.add_argument("-"+SELECTED_COLUMNS_ARGNAME_ALIAS, "--"+SELECTED_COLUMNS_ARGNAME, nargs='+', help=SELECTED_COLUMNS_HELP, default=sc_default_value)

  return parser










import jgtclirqdata


def add_jgtclirqdata_arguments(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    group_pattern=parser.add_argument_group('RQ Pattern', 'RQ Pattern to use.  Future practice to create request patterns to load into the args later.')
    
    group_pattern.add_argument('-pdsrq','--pds_rq_base',
                        action='store_true',
                        help='Use PDS_RQ JSON_BASE')
    #PDS_RQ JSON_NORMAL
    group_pattern.add_argument('-pdsrqn','--pds_rq_normal',
                        action='store_true',
                        help='Use PDS_RQ JSON_NORMAL')
    #PDS_RQ JSON_NORMAL_FRESH
    group_pattern.add_argument('-pdsrqnf','--pds_rq_normal_fresh',
                        action='store_true',
                        help='Use PDS_RQ JSON_NORMAL_FRESH')
    #PDS_RQ JSON_FULL
    group_pattern.add_argument('-pdsrqf','--pds_rq_full',
                        action='store_true',
                        help='Use PDS_RQ JSON_FULL')
    #PDS_RQ JSON_FULL_FRESH
    group_pattern.add_argument('-pdsrqff','--pds_rq_full_fresh',
                        action='store_true',
                        help='Use PDS_RQ JSON_FULL_FRESH')
    #IDS_RQ JSON_BASE
    group_pattern.add_argument('-idsrq','--ids_rq_base',
                        action='store_true',
                        help='Use IDS_RQ JSON_BASE')
    
    group_pattern.add_argument('-cdsrq','--cds_rq_normal',
                        action='store_true',
                        help='Use CDS_RQ JSON_NORMAL')
    
    group_pattern.add_argument('-cdsrqf','--cds_rq_full',
                        action='store_true',
                        help='Use CDS_RQ JSON_FULL')
    #CDS_RQ JSON_FULL_FRESH
    group_pattern.add_argument('-cdsrqff','--cds_rq_full_fresh',
                        action='store_true',
                        help='Use CDS_RQ JSON_FULL_FRESH')
    #CDS_RQ JSON_NORM_FRESH
    group_pattern.add_argument('-cdsrqnf','--cds_rq_norm_fresh',
                        action='store_true',
                        help='Use CDS_RQ JSON_NORM_FRESH')
    
    return parser

#post add_jgtclirqdata_arguments
def __jgtclirqdata_post_parse():
    global args
    __check_if_parsed()
    _jgtclirqdata_to_load=[jgtclirqdata.PDS_RQ_BASE]
    try:
        if hasattr(args, 'pds_rq_base') and args.pds_rq_base:
            _jgtclirqdata_to_load.append(jgtclirqdata.PDS_RQ_BASE)
        if hasattr(args, 'ids_rq_base') and args.ids_rq_base:
            _jgtclirqdata_to_load.append(jgtclirqdata.IDS_RQ_BASE)
        if hasattr(args, 'cds_rq_normal') and args.cds_rq_normal:
            _jgtclirqdata_to_load.append(jgtclirqdata.CDS_RQ_NORMAL)
        if hasattr(args, 'cds_rq_full') and args.cds_rq_full:
            _jgtclirqdata_to_load.append(jgtclirqdata.CDS_RQ_FULL)
        if hasattr(args, 'cds_rq_full_fresh') and args.cds_rq_full_fresh:
            _jgtclirqdata_to_load.append(jgtclirqdata.CDS_RQ_FULL_FRESH)
        if hasattr(args, 'cds_rq_norm_fresh') and args.cds_rq_norm_fresh:
            _jgtclirqdata_to_load.append(jgtclirqdata.CDS_RQ_NORM_FRESH)
        if hasattr(args, 'pds_rq_normal') and args.pds_rq_normal:
            _jgtclirqdata_to_load.append(jgtclirqdata.PDS_RQ_NORMAL)
        if hasattr(args, 'pds_rq_normal_fresh') and args.pds_rq_normal_fresh:
            _jgtclirqdata_to_load.append(jgtclirqdata.PDS_RQ_NORMAL_FRESH)
        if hasattr(args, 'pds_rq_full') and args.pds_rq_full:
            _jgtclirqdata_to_load.append(jgtclirqdata.PDS_RQ_FULL)
        if hasattr(args, 'pds_rq_full_fresh') and args.pds_rq_full_fresh:
            _jgtclirqdata_to_load.append(jgtclirqdata.PDS_RQ_FULL_FRESH)
            
    except:
        pass
    #for each pattern we have, load their key/value into the args
    for pattern in _jgtclirqdata_to_load:
        try:
            #print(pattern)
            json_obj = json.loads(pattern)
            for key in json_obj:
                setattr(args, key, json_obj[key])
        except:
            pass
    return args


#Load a json content from the argument --json
def add_load_json_file_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    output_group=_get_group_by_title(parser,ARG_GROUP_OUTPUT_TITLE,ARG_GROUP_OUTPUT_DESCRIPTION)
    output_group.add_argument('-jsonf','--json_file',
                        help='JSON filepath content to be loaded.')
    
    return parser


def __json_post_parse():
    global args
    __check_if_parsed()
    
    try:
        #Create args from the json_file
        if hasattr(args, 'json_file') and args.json_file is not None:
            filepath = args.json_file
            #raise exception if file does not exist
            if not os.path.exists(filepath):
                raise Exception("File does not exist."+filepath)
            with open(filepath, 'r') as f:
                try:
                    json_obj = json.load(f)
                    for key in json_obj:
                        #print("key:"+key, " value:"+str(json_obj[key]))
                        setattr(args, key, json_obj[key])
                except:
                    pass
    except:
        pass
    return args


def add_exit_if_error(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-xe','--exitonerror',
                        action='store_true',
                        help='Exit on error rather than trying to keep looking')
    return parser

def add_dropna_volume_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    global default_parser
    if parser is None:
        parser=default_parser
    
    cleanupGroup=_get_group_by_title(parser,ARG_GROUP_CLEANUP_TITLE,ARG_GROUP_CLEANUP_DESCRIPTION)
    
    dv_group=cleanupGroup.add_mutually_exclusive_group()
    
    dv_group.add_argument('-'+DROPNA_VOLUME_FLAG_ARGNAME_ALIAS,'--'+DROPNA_VOLUME_FLAG_ARGNAME,
                        action='store_true',
                        help='Drop rows with NaN (or 0) in volume column.  (note.Montly chart does not dropna volume)')
    
    dv_group.add_argument("-"+DONT_DROPNA_VOLUME_FLAG_ARGNAME_ALIAS,"--"+DONT_DROPNA_VOLUME_FLAG_ARGNAME, help="Do not dropna volume", action="store_true")
    
    return parser



def __dropna_volume__post_parse():
    try:
        dropna_volume_flag = _do_we_dropna_volume(args)
        setattr(args, 'dropna_volume',dropna_volume_flag)
        #dont_dropna_volume
        setattr(args, 'dont_dropna_volume',not dropna_volume_flag)
        
    except:
        pass
    return args

def __quiet__post_parse():
    try:
        if not hasattr(args, 'quiet') and (hasattr(args, 'verbose') and args.verbose==0):
            #add quiet to list
           #print("Quiet mode activated in parser")
           setattr(args, 'quiet', True)
        else:
            setattr(args, 'quiet', False)
    except:
        pass
    return args


def _get_iterable_timeframes_from_args()->List[str]:
    global args
    __check_if_parsed()
    if hasattr(args, 'timeframe') and \
        hasattr(args, 'tflag')   and \
            getattr(args, "tflag"):
        return getattr(args, 'timeframes')
    else: #Return just one timeframe
        return [getattr(args, 'timeframe')]


def _get_iterable_instruments_from_args()->List[str]:
    global args
    __check_if_parsed()
    if hasattr(args, 'instrument') and \
        hasattr(args, 'iflag')   and \
            getattr(args, "iflag"):
        return getattr(args, 'instruments')
    else: #Return just one instrument
        return [getattr(args, 'instrument')]

from jgtconstants import TIMEFRAMES_DEFAULT_STRING,INSTRUMENT_ALL_STRING
from jgtconstants import TIMEFRAMES_ALL, TIMEFRAMES_DEFAULT


def get_timeframes(default_timeframes: List[str] = None, envvar="T") -> List[str]:
    global args
    if args.timeframe and not args.tflag:
        return [args.timeframe]
    elif args.tflag:
        return args.timeframes
    else:
        return os.getenv(envvar, TIMEFRAMES_DEFAULT_STRING).split(",") if default_timeframes is None else default_timeframes if isinstance(default_timeframes, list) else default_timeframes.split(",")

def get_instruments(default_instruments: List[str] = None, envvar="I") -> List[str]:
    global args
    if args.instrument and not args.iflag:
        return [args.instrument]
    elif args.iflag:
        return args.instruments
    else:
        return os.getenv(envvar, INSTRUMENT_ALL_STRING).split(",") if default_instruments is None else default_instruments if isinstance(default_instruments, list) else default_instruments.split(",")
    



def __timeframes_post_parse()->argparse.Namespace:
    global args,settings
    __check_if_parsed()
    
    _timeframes=None
    
    setattr(args, 'tflag',False)
    if hasattr(args, 'timeframe') and getattr(args, "timeframe") is not None  and ","  in getattr(args, "timeframe"):
        setattr(args, 'tflag',True)
        _timeframes=getattr(args, "timeframe").split(",")
    
    elif hasattr(args, "timeframes"):
        _timeframes=getattr(args, "timeframes")
    else:
        try:
            if settings["timeframes"]:
                _timeframes =settings["timeframes"]
        except:
            pass
            
            
    if _timeframes is not None and not isinstance(_timeframes, list) :
        _timeframes=parse_timeframes_helper(_timeframes)


    #if we have coma in the string
    if _timeframes is None:
        _timeframes = os.getenv("T",TIMEFRAMES_DEFAULT_STRING)
    
    if  "," in _timeframes:
        _timeframes=parse_timeframes_helper(_timeframes)
    
    
    setattr(args, 'timeframes',_timeframes)

    return args



def parse_timeframes_helper(timeframes):
    if timeframes in TIMEFRAMES_ALL:
        return [timeframes]
    
    if timeframes == "default":
        __timeframes = TIMEFRAMES_DEFAULT
    if  timeframes == "all" :
        __timeframes = TIMEFRAMES_ALL
    
    if timeframes == "default" or timeframes == "all" :
        try:
            _timeframes = os.getenv("T",__timeframes).split(",")
        except:
            _timeframes = None
    else:
        try:
            _timeframes = timeframes.split(",")
        except:
            _timeframes = None
    return _timeframes



from jgtconstants import INSTRUMENTS_DEFAULT,INSTRUMENT_ALL

def __instruments_post_parse()->argparse.Namespace:
    global args,settings
    __check_if_parsed()
    
    _instruments=None
    # if not hasattr(args, 'instrument') or args.instrument is None:
    #     return args
    
    setattr(args, 'iflag',False)
    if hasattr(args, 'instrument') and getattr(args, "instrument") is not None and "," in getattr(args, "instrument"):
        setattr(args, 'iflag',True)
        _instruments=getattr(args, "instrument")
    else:
        try:
            if settings["instruments"]:
                _instruments =settings["instruments"]
        except:
            pass
            
            
    if _instruments is not None and not isinstance(_instruments, list) :
        _instruments=parse_instruments_helper(_instruments)


    if _instruments is None :
        _instruments = os.getenv("I",None)
            
    setattr(args, 'instruments',_instruments)

    return args


def parse_instruments_helper(instruments):

   
    if instruments == "default":
        __instruments = INSTRUMENTS_DEFAULT
    if instruments == "all" :
        __instruments=INSTRUMENT_ALL
    
    if instruments == "default" or instruments == "all" :
        try:
            _instruments = os.getenv("I",None).split(",")
        except:
            _instruments = None
    else:
        try:
            _instruments = instruments.split(",")
        except:
            _instruments = None
    return _instruments

def __crop_last_dt__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    if hasattr(args, 'crop_last_dt'):
        if args.crop_last_dt is not None:
            setattr(args, 'crop_last_dt', args.crop_last_dt)
    else:
        setattr(args, 'crop_last_dt', None)
    return args
#tlid_dateto
def __tlid_dateto__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    if hasattr(args, TLID_DATETO_ARGNAME):
        if getattr(args, TLID_DATETO_ARGNAME) is not None:
            try:
                
                dt_object=tlid.to_date(getattr(args, TLID_DATETO_ARGNAME))
                setattr(args, TLID_DATETO_ARGNAME,dt_object )
            except:
                raise Exception("Invalid TLID DateTo format.  Use YYMMDDHHMM")
    else:
        setattr(args, 'crop_last_dt', None)
    return args
#@STCIssue We want this to Default to True and would be flagged to false by rm_bid_ask
def __keep_bid_ask__post_parse(keep_bid_ask_argname = 'keepbidask',rm_bid_ask_argname = 'rmbidask')->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        keep_bid_ask_value=True        
        
        if hasattr(args, rm_bid_ask_argname) or hasattr(args,'rm_bid_ask'):
            if hasattr(args, rm_bid_ask_argname) and args.rmbidask:
                keep_bid_ask_value=False
            if hasattr(args, 'rm_bid_ask') and args.rm_bid_ask:
                keep_bid_ask_value=False
        
        setattr(args, keep_bid_ask_argname,keep_bid_ask_value)
        setattr(args, 'keep_bid_ask',keep_bid_ask_value) # Future refactoring will be called just that.
        setattr(args, rm_bid_ask_argname,not keep_bid_ask_value)
    except:
        pass
    return args
    
def __verbose__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, 'verbose'):
            setattr(args, 'verbose',0)
    except:
        pass
    return args

def __quotescount__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, QUOTES_COUNT_ARGNAME):
            setattr(args, QUOTES_COUNT_ARGNAME,-1)
    except:
        pass
    return args

def __balligator_flag__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, BALLIGATOR_FLAG_ARGNAME):
            setattr(args, BALLIGATOR_FLAG_ARGNAME,False)
            
        if hasattr(args, BALLIGATOR_FLAG_ARGNAME) and args.timeframe=="M1":
            #print("We dont do balligator for M1")
            setattr(args, BALLIGATOR_FLAG_ARGNAME,False)
    except:
        pass
    return args

def __talligator_flag__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, TALLIGATOR_FLAG_ARGNAME):
            setattr(args, TALLIGATOR_FLAG_ARGNAME,False)
            
        if hasattr(args, TALLIGATOR_FLAG_ARGNAME) and args.timeframe=="M1":
            #print("We dont do talligator for M1")
            setattr(args, TALLIGATOR_FLAG_ARGNAME,False)
        
        if hasattr(args, TALLIGATOR_FLAG_ARGNAME) and args.timeframe=="W1":
            #print("We dont do talligator for W1")
            setattr(args, TALLIGATOR_FLAG_ARGNAME,False)
    except:
        pass
    return args


_NO_MFI_FOR_M1_flag=False
def __mfi_flag__post_parse()->argparse.Namespace:
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, MFI_FLAG_ARGNAME):
            setattr(args, MFI_FLAG_ARGNAME,False)
        
        if _NO_MFI_FOR_M1_flag:
            if hasattr(args, MFI_FLAG_ARGNAME) and args.timeframe=="M1":
                #print("We dont do MFI for M1")
                setattr(args, MFI_FLAG_ARGNAME,False)
    except:
        pass
    return args


def __use_fresh__post_parse()->argparse.Namespace: 
    global args
    __check_if_parsed()
    try:
        if not hasattr(args, FRESH_FLAG_ARGNAME):
            setattr(args, FRESH_FLAG_ARGNAME,False)
        if hasattr(args, FRESH_FLAG_ARGNAME) and args.fresh:
            setattr(args, FRESH_FLAG_ARGNAME,True)
        else:
            if hasattr(args, NOT_FRESH_FLAG_ARGNAME) and args.notfresh:
                setattr(args, FRESH_FLAG_ARGNAME,False)
    except:
        pass
    return args

def __check_if_parsed():
    if args is None or args==[]:
        raise Exception("args is not set.  Run parse_args() first before calling this function.  Most likely, the CLI must be updated to do parser.parse_args() first instead of doing it in the main (REFACTORING Responsabilities)")

def _post_parse_dependent_arguments_rules()->argparse.Namespace:
    global args
    __check_if_parsed()
    
    #args=_load_settings_from_args() #@STCIssue - THis has to load before we do any other argparsing, like preloading the settings.
    
    args=__quiet__post_parse()
    
    try:
        if hasattr(args,"instrument") and args.instrument and isinstance(args.instrument, str):
            setattr(args, 'instrument', fn2i(args.instrument) )
    except:
        pass
    try:
        if hasattr(args,"timeframe") and args.timeframe and isinstance(args.timeframe, str):
            setattr(args, 'timeframe', fn2t(args.timeframe) )
    except:
        pass
    
    # OTHER DEPENDENT RULES

    args=__dropna_volume__post_parse()
    
    args=__keep_bid_ask__post_parse()
    
    args=__timeframes_post_parse()
    args=__instruments_post_parse()
    
    args=__crop_last_dt__post_parse()
    args=__tlid_dateto__post_parse()
    args=__verbose__post_parse()
    args=__quotescount__post_parse()
    args=__balligator_flag__post_parse()
    args=__talligator_flag__post_parse()
    args=__mfi_flag__post_parse()
    args=__use_fresh__post_parse()
    args=__json_post_parse()   
    args=__jgtclirqdata_post_parse()
    args=_demo_flag()
    
    try:
        if hasattr(args,"instrument") and args.instrument and isinstance(args.instrument, str):
            setattr(args, 'instrument', fn2i(args.instrument) )
    except:
        pass
    
    try:
        if hasattr(args,"timeframe") and args.timeframe and isinstance(args.timeframe, str):
            setattr(args, 'timeframe', fn2t(args.timeframe) )
    except:
        pass

    return args

    
def _demo_flag():
    global args
    if hasattr(args, 'demo') and args.demo:
        setattr(args, 'connection', 'Demo')
        setattr(args, 'demo', True)
        setattr(args, 'real', False)
    else:
        setattr(args, 'connection', 'Real')
        setattr(args, 'real', True)
        setattr(args, 'demo', False)
    return args

def parse_args(parser: argparse.ArgumentParser=None)->argparse.Namespace:
    global default_parser,args,settings
    if parser is None:
        parser=default_parser
    args= parser.parse_args()
    try:
        #set a key jgtcommon_settings in the args to store settings
        setattr(args, 'jgtcommon_settings', get_settings())
    except:
        pass
    
    
    args=_post_parse_dependent_arguments_rules()
    return args

def _do_we_dropna_volume(_args=None):
    global args
    if _args is None:
        _args=args
    dropna_volume_value = _args.dropna_volume or not _args.dont_dropna_volume
    if args.timeframe == "M1" and dropna_volume_value:
        #print("We dont dropna volume for M1")
        return False # We dont drop for Monthly
    return dropna_volume_value

def add_viewpath_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
    """
    Adds an view path argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the viewpath argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with the argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    output_group=_get_group_by_title(parser,ARG_GROUP_OUTPUT_TITLE,ARG_GROUP_OUTPUT_DESCRIPTION)
    output_group.add_argument('-vp','--viewpath',
                        action='store_true',
                        dest='viewpath',
                        help='flag to just view the path of files from arguments -i -t.')
    return parser


# def add_quiet_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:
#     parser.add_argument('-q','--quiet',
#                         action='store_true',
#                         help='Suppress all output. If specified, no output will be printed to the console.')
#     return parser

def add_verbose_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    
    group_verbosity=_get_group_by_title(parser,ARG_GROUP_VERBOSITY_TITLE,ARG_GROUP_VERBOSITY_DESCRIPTION)
    
    group_verbosity.add_argument('-v', '--verbose',
                        type=int,
                        default=0,
                        help='Set the verbosity level. 0 = quiet, 1 = normal, 2 = verbose, 3 = very verbose, etc.')
    return parser

def add_cds_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-cds','--cds',
                        action='store_true',
                        default=False,
                        help='Action the creation of CDS')
    return parser

def add_ids_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-ids','--ids',
                        action='store_true',
                        default=False,
                        help='Action the creation of IDS')
    return parser

def add_ids_mfi_argument(parser: argparse.ArgumentParser=None,load_default_from_settings=True,flag_default_value=True)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    default_value = load_arg_default_from_settings(MFI_FLAG_ARGNAME,flag_default_value,alias=MFI_FLAG_ARGNAME_ALIAS) if load_default_from_settings else flag_default_value
    #settings.get(MFI_FLAG_ARGNAME,flag_default_value) if settings else flag_default_value
    
    group_indicators=_get_group_by_title(parser,ARG_GROUP_INDICATOR_TITLE,ARG_GROUP_INDICATOR_DESCRIPTION)
    mfi_exclusive_subgroup=group_indicators.add_mutually_exclusive_group()
    mfi_exclusive_subgroup.add_argument(
        "-"+MFI_FLAG_ARGNAME_ALIAS,
        "--"+MFI_FLAG_ARGNAME,
        action="store_true",
        default=default_value,
        help="Enable the Market Facilitation Index indicator.",
    )
    mfi_exclusive_subgroup.add_argument(
        "-"+NO_MFI_FLAG_ARGNAME_ALIAS,
        "--"+NO_MFI_FLAG_ARGNAME,  
        action="store_true",
        default=not default_value,
        help="Disable the Market Facilitation Index indicator.",
    )  
    return parser

def add_ids_gator_oscillator_argument(parser: argparse.ArgumentParser=None,load_default_from_settings=True,flag_default_value=False)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    group_indicators=_get_group_by_title(parser,ARG_GROUP_INDICATOR_TITLE,ARG_GROUP_INDICATOR_DESCRIPTION)
    
    default_value = load_arg_default_from_settings(GATOR_OSCILLATOR_FLAG_ARGNAME,flag_default_value,alias=GATOR_OSCILLATOR_FLAG_ARGNAME_ALIAS) if load_default_from_settings else flag_default_value
    
    group_indicators.add_argument(
        "-"+GATOR_OSCILLATOR_FLAG_ARGNAME_ALIAS,
        "--"+GATOR_OSCILLATOR_FLAG_ARGNAME,
        action="store_true",
        help="Enable the Gator Oscillator indicator.",
        default=default_value
    )
    return parser

from jgtcliconstants import  (LARGEST_FRACTAL_PERIOD_ARGNAME,
                                LARGEST_FRACTAL_PERIOD_ARGNAME_ALIAS, SETTING_ARGNAME, SETTING_ARGNAME_ALIAS,)
def add_ids_fractal_largest_period_argument(parser: argparse.ArgumentParser=None,load_default_from_settings=True,default_value=89)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    group_indicators=_get_group_by_title(parser,ARG_GROUP_INDICATOR_TITLE,ARG_GROUP_INDICATOR_DESCRIPTION)
    
    default_value = load_arg_default_from_settings(LARGEST_FRACTAL_PERIOD_ARGNAME,default_value,alias=LARGEST_FRACTAL_PERIOD_ARGNAME_ALIAS) if load_default_from_settings else default_value
    
    group_indicators.add_argument(
        "-"+LARGEST_FRACTAL_PERIOD_ARGNAME_ALIAS,
        "--"+LARGEST_FRACTAL_PERIOD_ARGNAME,
        type=int,
        default=default_value,
        help=f"The largest fractal period. ({default_value})",
    )
    return parser



from jgtconstants import BJAW_PERIODS,BTEETH_PERIODS,BLIPS_PERIODS
from jgtcliconstants import  (BALLIGATOR_PERIOD_JAWS_ARGNAME,
                              BALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS,
                              BALLIGATOR_PERIOD_TEETH_ARGNAME,
                              BALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS,
                              BALLIGATOR_PERIOD_LIPS_ARGNAME,
                              BALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS,)
def add_ids_balligator_argument(parser: argparse.ArgumentParser=None,add_periods_arg=True,load_default_from_settings=True,flag_default_value=False,period_jaws_default = BJAW_PERIODS,period_teeth_default=BTEETH_PERIODS,period_lips_default=BLIPS_PERIODS)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    
    flag_default_value=load_arg_default_from_settings(BALLIGATOR_FLAG_ARGNAME,flag_default_value,alias=BALLIGATOR_FLAG_ARGNAME_ALIAS) if load_default_from_settings else flag_default_value
    
    group_indicators=_get_group_by_title(parser,ARG_GROUP_INDICATOR_TITLE,ARG_GROUP_INDICATOR_DESCRIPTION)
    group_indicators.add_argument(
        "-"+BALLIGATOR_FLAG_ARGNAME_ALIAS,
        "--"+BALLIGATOR_FLAG_ARGNAME,
        action="store_true",
        help="Enable the Big Alligator indicator.",
        default=flag_default_value
    )
    
    if add_periods_arg:
        balligator_period_jaws_default=load_arg_default_from_settings(BALLIGATOR_PERIOD_JAWS_ARGNAME,period_jaws_default,alias=BALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+BALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS,
            "--"+BALLIGATOR_PERIOD_JAWS_ARGNAME,
            type=int,
            default=balligator_period_jaws_default,
            help="The period of the Big Alligator jaws.",
        )
        balligator_period_teeth_default=load_arg_default_from_settings(BALLIGATOR_PERIOD_TEETH_ARGNAME,period_teeth_default,alias=BALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+BALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS,
            "--"+BALLIGATOR_PERIOD_TEETH_ARGNAME,
            type=int,
            default=balligator_period_teeth_default,
            help="The period of the Big Alligator teeth.",
        )
        balligator_period_lips_default=load_arg_default_from_settings(BALLIGATOR_PERIOD_LIPS_ARGNAME,period_lips_default,alias=BALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+BALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS,
            "--"+BALLIGATOR_PERIOD_LIPS_ARGNAME,
            type=int,
            default=balligator_period_lips_default,
            help="The period of the Big Alligator lips.",
        )
    return parser

from jgtconstants import TJAW_PERIODS,TTEETH_PERIODS,TLIPS_PERIODS
from jgtcliconstants import  (TALLIGATOR_PERIOD_JAWS_ARGNAME,
                              TALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS,
                              TALLIGATOR_PERIOD_TEETH_ARGNAME,
                              TALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS,
                              TALLIGATOR_PERIOD_LIPS_ARGNAME,
                              TALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS,)
def add_ids_talligator_argument(parser: argparse.ArgumentParser=None,add_periods_arg=True,load_default_from_settings=True,flag_default_value=False,period_jaws_default = TJAW_PERIODS,period_teeth_default=TTEETH_PERIODS,period_lips_default=TLIPS_PERIODS)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    
    flag_default_value=load_arg_default_from_settings(TALLIGATOR_FLAG_ARGNAME,flag_default_value,alias=TALLIGATOR_FLAG_ARGNAME_ALIAS) if load_default_from_settings else flag_default_value
    
    group_indicators=_get_group_by_title(parser,ARG_GROUP_INDICATOR_TITLE,ARG_GROUP_INDICATOR_DESCRIPTION)
    group_indicators.add_argument(
        "-"+TALLIGATOR_FLAG_ARGNAME_ALIAS,
        "--"+TALLIGATOR_FLAG_ARGNAME,
        action="store_true",
        help="Enable the Tide Alligator indicator.",
        default=flag_default_value
    )
    
    if add_periods_arg:
        talligator_period_jaws_default=load_arg_default_from_settings(TALLIGATOR_PERIOD_JAWS_ARGNAME,period_jaws_default,alias=TALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+TALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS,
            "--"+TALLIGATOR_PERIOD_JAWS_ARGNAME,
            type=int,
            default=talligator_period_jaws_default,
            help="The period of the Tide Alligator jaws.",
        )
        talligator_period_teeth_default=load_arg_default_from_settings(TALLIGATOR_PERIOD_TEETH_ARGNAME,period_teeth_default,alias=TALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+TALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS,
            "--"+TALLIGATOR_PERIOD_TEETH_ARGNAME,
            type=int,
            default=talligator_period_teeth_default,
            help="The period of the Tide Alligator teeth.",
        )
        talligator_period_lips_default=load_arg_default_from_settings(TALLIGATOR_PERIOD_LIPS_ARGNAME,period_lips_default,alias=TALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS)
        
        group_indicators.add_argument(
            "-"+TALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS,
            "--"+TALLIGATOR_PERIOD_LIPS_ARGNAME,
            type=int,
            default=talligator_period_lips_default,
            help="The period of the Tide Alligator lips.",
        )
    return parser

def add_ads_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser
    interaction_group=_get_group_by_title(parser,ARG_GROUP_INTERACTION_TITLE,ARG_GROUP_INTERACTION_DESCRIPTION)
    interaction_group.add_argument('-ads','--ads',
                        action='store_true',
                        default=False,
                        help='Action the creation of ADS and show the chart')
    return parser

def add_iprop_init_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-iprop','--iprop',
                        action='store_true',
                        default=False,
                        help='Toggle the downloads of all instrument properties ')
    return parser

def add_debug_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    group_verbosity=_get_group_by_title(parser,ARG_GROUP_VERBOSITY_TITLE,ARG_GROUP_VERBOSITY_DESCRIPTION)
    group_verbosity.add_argument('-debug','--debug',
                        action='store_true',
                        default=False,
                        help='Toggle debug ')
    return parser

def add_pdsserver_argument(parser: argparse.ArgumentParser=None)->argparse.ArgumentParser:

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-server','--server',
                        action='store_true',
                        default=False,
                        help='Run the server ')
    return parser


def print_exception(exception: Exception):
    #logging.error("Exception: {0}\n{1}".format(exception, traceback.format_exc()))
    print("Exception: {0}\n{1}".format(exception, traceback.format_exc()))






def diff_month(year: int, month: int, date2: datetime):
    return (year - date2.year) * 12 + month - date2.month



def export_env_if_any(config):
    # if has a key : "keep_bid_ask" and if yes and set to "true", export an env variable "JGT_KEEP_BID_ASK" to "1"
    if 'keep_bid_ask' in config and config['keep_bid_ask'] == True:
        os.environ['JGT_KEEP_BID_ASK'] = '1'

_JGT_CONFIG_JSON_SECRET=None

def readconfig(json_config_str=None,config_file = 'config.json',export_env=False,config_file_path_env_name='JGT_CONFIG_PATH',config_values_env_name='JGT_CONFIG',force_read_json=False,demo=False,use_demo_json_config=False):
    global _JGT_CONFIG_JSON_SECRET
    
    try:
        home_dir = os.path.expanduser("~")
    except:
        home_dir=os.environ["HOME"]
    if home_dir=="":
        home_dir=os.environ["HOME"]
        
    #demo_config are assumed to be $HOME/.jgt/config_demo.json
    if demo and use_demo_json_config:
        config_file = os.path.join(home_dir, '.jgt/config_demo.json')
        #check if exist, advise and raise exception if not
        if not os.path.exists(config_file):
            print("Configuration not found. create : {config_file} or we will try to use the _demo in the usual config.json")
            config=readconfig(force_read_json=True)
            _set_demo_credential(config,demo)
            return config
            #raise Exception(f"Configuration not found. create : {config_file})")
 
    #force_read_json are assumed to be $HOME/.jgt/config.json
    if force_read_json:
        config_file = os.path.join(home_dir, '.jgt/config.json')
        #check if exist, advise and raise exception if not
        if not os.path.exists(config_file):
            raise Exception(f"Configuration not found. create : {config_file})")
        #load and return config
        with open(config_file, 'r') as f:
            config = json.load(f)
            if export_env:
                export_env_if_any(config)
            _set_demo_credential(config,demo)
            return config
            
    
    #print argument values to debug
    _DEBUG_240619=False
    if _DEBUG_240619:
        print("json_config_str:",json_config_str)
        print("config_file:",config_file)
        print("export_env:",export_env)
        print("config_file_path_env_name:",config_file_path_env_name)
        print("config_values_env_name:",config_values_env_name)
    
    # Try reading config file from current directory

    if json_config_str is not None:
        config = json.loads(json_config_str)
        _JGT_CONFIG_JSON_SECRET=json_config_str
        if export_env:
            export_env_if_any(config)
        _set_demo_credential(config,demo)
        return config
    
    
    if _JGT_CONFIG_JSON_SECRET is not None:
        config = json.loads(_JGT_CONFIG_JSON_SECRET)
        if export_env:
            export_env_if_any(config)
        _set_demo_credential(config,demo)
        return config
    
    config = None

    # if file does not exist try set the path to the file in the HOME
    if not os.path.exists(config_file):
        config_file = os.path.join(home_dir, config_file)
        
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            if export_env:
                export_env_if_any(config)
            _set_demo_credential(config,demo)
            return config
    else:

        config_file = os.path.join(home_dir, config_file)
        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            # If config file still not found, try reading from environment variable
            config_json_str = os.getenv('JGT_CONFIG_JSON_SECRET')
            if config_json_str:
                config = json.loads(config_json_str)
                if export_env:
                    export_env_if_any(config)
                _set_demo_credential(config,demo)
                return config


    # Now you can use the config dictionary in your application

    # if file dont exist, try loading from env var JGT_CONFIG
    if not os.path.exists(config_file):
        config_json_str = os.getenv(config_values_env_name)
        
        if config_json_str:
            config = json.loads(config_json_str)
            if export_env:
                export_env_if_any(config)
            #return config
        else:
            # if not found, try loading from env var JGT_CONFIG_PATH
            config_file = os.getenv(config_file_path_env_name)
            if config_file:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if export_env:
                        export_env_if_any(config)
                    #return config
           # else:
               
    # Read config file
    if config is None:
        #print("config_file:",config_file)
        if config_file is not None and os.path.exists(config_file) :
            with open(config_file, 'r') as file:
                config = json.load(file)
        
    if config is None:
        #Last attempt to read
        try:
            another_config = "config.json"
            if not os.path.exists(another_config):
                another_config = os.path.join(os.path.expanduser('~'), '.jgt', 'config.json')
                
            if not os.path.exists(another_config):
                another_config = "/etc/jgt/config.json"
            with open(another_config, 'r') as file:
                config = json.load(file)
        except:
            pass
        # try:
        #     home_config_path_try2 = os.path.join(os.path.expanduser('~'), '.jgt', 'config.json')
        #     if not os.path.exists(another_config):
        #         another_config = "/etc/jgt/config.json"
        #     with open(another_config, 'r') as file:
        #         config = json.load(file)
        # except:
        #     pass
        if config is None:
            try:
                with open("/home/jgi/.jgt/config.json", 'r') as file:
                    config = json.load(file)
            except:
                pass
        if config is None:
            try:                                                                                  
                with open("/etc/jgt/config.json", 'r') as file:                             
                    config = json.load(file)
            except:
                pass
                
        if config is None:    
            raise Exception(f"Configuration not found. Please provide a config file or set the JGT_CONFIG environment variable to the JSON config string. (config_file={config_file})")
    
    if export_env:
        export_env_if_any(config)
    _set_demo_credential(config,demo)
    return config

def _set_demo_credential(config,demo=False):
    if demo:
        config["user_id"]=config["user_id_demo"]
        config["password"]=config["password_demo"]
        config["account"]=config["account_demo"]
        config["connection"]="Demo"


def read_fx_str_from_config(demo=False)->tuple[str,str,str,str,str]:
    config = readconfig(demo=demo)
    if config["connection"]=="Real" and demo: #Make sure we have our demo credentials
        _set_demo_credential(config,True)
    str_user_id=config['user_id']
    str_password=config['password']
    str_url=config['url']
    str_connection="Real" if not demo else "Demo"
    str_account=config['account']
    return str_user_id,str_password,str_url,str_connection,str_account



def is_market_open(current_time=None,exit_cli_if_closed=False,market_closed_callback=None):
    if current_time is None:
        current_time = datetime.utcnow()

    # Define market open and close times
    market_open_time = time(21, 0)  # 21:00 UTC
    market_close_time = time(21, 15)  # 21:15 UTC

    # Get the current day of the week (0=Monday, 6=Sunday)
    current_day = current_time.weekday()

    current_time_utc = current_time.time()
    # Check if the market is open
    if current_day == 6:  # Sunday
        if current_time_utc >= market_open_time:
            return True
    elif current_day == 4:  # Friday
        if current_time_utc < market_close_time:
            return True
    elif 0 <= current_day < 4:  # Monday to Thursday
        return True
    if market_closed_callback is not None:
        market_closed_callback()
    if exit_cli_if_closed:
        from jgterrorcodes import MARKET_CLOSED_EXIT_ERROR_CODE
        print("Market is closed.")
        sys.exit(MARKET_CLOSED_EXIT_ERROR_CODE)
    return False

def dt_from_last_week_as_datetime():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    return last_week

def dt_from_last_week_as_string_fxformat():
    last_week = dt_from_last_week_as_datetime()
    _str=last_week.strftime('%m.%d.%Y')
    return _str + " 00:00:00"
