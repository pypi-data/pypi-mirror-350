import json
import sys
def print_jsonl_message(msg,extra_dict:dict=None,scope=None,state:str=None,msg_key_name = "message",state_key_name = "state",scope_key = "scope",use_short=False):
    json_output = build_jsonl_message(msg,extra_dict,scope,state,msg_key_name,state_key_name,scope_key,use_short)
    print(json_output)

def build_jsonl_message(msg,extra_dict:dict=None,scope=None,state:str=None,msg_key_name = "message",state_key_name = "state",scope_key = "scope",use_short=False):
    o={}
    if use_short:
        msg_key_name="msg"
        state_key_name="s"
        scope_key="sc"
    o[msg_key_name]=msg
    if extra_dict:
        o.update(extra_dict)
    if scope:
        o[scope_key]=scope
    if state:        
        o[state_key_name]=state
    json_output = json.dumps(o)
    return json_output


_exit_message = None
_exit_handler = None

def signal_handler(sig, frame):
    global _exit_message, _exit_handler
    if _exit_message:
        print(_exit_message)
    if _exit_handler:
        #call it        
        msg=_exit_handler()
        print(msg)
    sys.exit(0)

def add_exiting_quietly(message:str=None,exit_handler=None):
    global _exit_message, _exit_handler
    if exit_handler:
        _exit_handler = exit_handler
    if message:
        _exit_message = message
    import signal
    signal.signal(signal.SIGINT, signal_handler)