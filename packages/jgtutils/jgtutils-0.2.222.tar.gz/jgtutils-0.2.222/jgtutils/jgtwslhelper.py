import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtutils.jgtcliconstants import (PDSCLI_PROG_NAME,TLID_RANGE_ARGNAME_ALIAS,FULL_FLAG_ARGNAME,QUOTES_COUNT_ARGNAME_ALIAS,KEEP_BID_ASK_FLAG_ARGNAME_ALIAS)

import platform

import jgtos


def pwsd_wsl_run_command1(bash_command_to_run):
    powershell_command = 'wsl.exe bash -c \'' + bash_command_to_run + '\''
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")





def run_bash_command_by_platform(bash_cmd):
    try:
        if platform.system() == "Windows":
            shell = os.environ.get('COMSPEC', 'cmd.exe')
            if 'powershell' in shell.lower():
                # The interpreter is PowerShell            
                return subprocess.run(bash_cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
            else:
                # The interpreter is cmd.exe
                return wsl_run_bash_on_cmd(bash_cmd)
        else:
            # The system is Linux
            return subprocess.run(bash_cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    except Exception as e:
        print(f"An error occurred running {PDSCLI_PROG_NAME}: {str(e)}")
        print(f"   bash_cmd: {bash_cmd}")
        raise e
        #return None
    
def wsl_run_bash_on_cmd(bash_cmd):   
    
    powershell_command = 'wsl.exe bash -c \'' + bash_cmd + '\''
    result = subprocess.run(
        ["pwsh.exe", "-Command", powershell_command], stdout=subprocess.PIPE, shell=True
    )
    return result.stdout.decode("utf-8")



def run(bash_command):
    return run_bash_command_by_platform(bash_command)




def resolve_cli_path(cli_path=""):
    if cli_path == "" or cli_path is None or cli_path == 0 or cli_path == '0':
        cli_path = os.path.join(os.getenv('HOME'), '.local', 'bin', PDSCLI_PROG_NAME)
    if not os.path.exists(cli_path):
        cli_path = PDSCLI_PROG_NAME    
    
    return cli_path #@STCIssue Should install : pip install --user jgtfxcon    (if not found)

def jgtfxcli_wsl(instrument:str, timeframe:str, quote_count:int,cli_path="", verbose_level=0,use_full=False,keep_bid_ask=False):

    
    bash_command_to_run=_mkbash_cmd_string_jgtfxcli_range(instrument, timeframe,cli_path=cli_path, verbose_level=verbose_level,quote_count=quote_count,use_full=use_full,keep_bid_ask=keep_bid_ask)
    
    return run_bash_command_by_platform(bash_command_to_run)


def _mkbash_cmd_string_jgtfxcli_range(instrument:str, timeframe:str,tlid_range=None,cli_path="", verbose_level=0,quote_count=420,use_full=False,keep_bid_ask=False):

    base_args = mk_base_args(instrument, timeframe, cli_path, verbose_level, keep_bid_ask)
    
    if tlid_range is not None and tlid_range != "":
        bash_command_to_run = f"{base_args} -{TLID_RANGE_ARGNAME_ALIAS} \"{tlid_range}\""
    else:
        if use_full:
            bash_command_to_run = f"{base_args} --{FULL_FLAG_ARGNAME}"
        else:
            quote_args = ""
            if quote_count > 0:
                quote_args = f" -{QUOTES_COUNT_ARGNAME_ALIAS} {quote_count}"
            bash_command_to_run = f"{base_args}{quote_args}"
        
    
    return bash_command_to_run

def mk_base_args(instrument, timeframe, cli_path, verbose_level, keep_bid_ask):
    cli_path=resolve_cli_path(cli_path)
    bidask_arg = ""
    
    if keep_bid_ask:
        bidask_arg = f" -{KEEP_BID_ASK_FLAG_ARGNAME_ALIAS}"
    
    base_args=f"{cli_path} -i \"{instrument}\" -t \"{timeframe}\"{bidask_arg} -v {verbose_level}"
    return base_args

def jgtfxcli_wsl_range(instrument:str, timeframe:str, quote_count:int,tlid_range=None,cli_path="", verbose_level=0,use_full=False,keep_bid_ask=False):
    bash_command_to_run = _mkbash_cmd_string_jgtfxcli_range(instrument, timeframe,tlid_range,cli_path, verbose_level,quote_count,use_full=use_full,keep_bid_ask=keep_bid_ask)
    return run_bash_command_by_platform(bash_command_to_run)

def jgtfxcli(instrument:str, timeframe:str, quote_count:int,cli_path="", verbose_level=0,use_full=False):
    return jgtfxcli_wsl(instrument,timeframe,quote_count,cli_path,verbose_level,use_full=use_full)

def getPH(instrument:str, timeframe:str, quote_count:int,tlid_range=None, verbose_level=0,use_full=False,keep_bid_ask=False):
    return jgtfxcli_wsl_range(instrument, timeframe, quote_count,tlid_range,"", verbose_level,use_full=use_full,keep_bid_ask=keep_bid_ask)

def wsl_cd(directory):
    # Define the command to be executed
    command = ["wsl.exe", "cd", directory]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Print the error (if any)
    if result.stderr:
        return result.stderr.decode("utf-8")
    else:
        # Print the output
        return result.stdout.decode("utf-8")
        

def cd(tpath):
    wsl_cd(tpath)

def execute_wsl_command_v1_with_cd(directory, command_to_execute):
    # Define the command to be executed
    command = ["wsl.exe", "cd", directory, "&&", command_to_execute]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode("utf-8"))

    # Print the error (if any)
    if result.stderr:
        print("Error:", result.stderr.decode("utf-8"))


minimum_quote_count = 335

# Define the dividers for each timeframe
timeframe_dividers = {
    "m1": 0.0166,
    "mi1": 0.0166,
    "m5": 0.8,
    "m15": 0.25,
    "m30": 0.5,
    "H1": 1,
    "H2": 2,
    "H3": 3,
    "H4": 4,
    "H5": 5,
    "H6": 6,
    "H8": 8,
    "D1": 24,
    "W1": 110,
    "M1": 400
}

#@STCIssue Locks us to H1, should be interactive and receive an input from the user, lower TF
def get_timeframe_dividers(base_tf="H1"):
    return timeframe_dividers[base_tf]
