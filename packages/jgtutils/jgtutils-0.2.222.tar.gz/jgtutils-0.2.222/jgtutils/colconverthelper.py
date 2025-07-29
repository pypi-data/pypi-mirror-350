from jgtconstants import (MFI_FADE, MFI_FADE_ID, MFI_FADE_STR, MFI_FAKE,
                          MFI_FAKE_ID, MFI_FAKE_STR, MFI_GREEN, MFI_GREEN_ID,
                          MFI_GREEN_STR, MFI_SQUAT, MFI_SQUAT_ID,
                          MFI_SQUAT_STR)

from jgtutils.jgtconstants import MFI_SIGNAL as MFI_DEFAULT_COLNAME
from jgtutils.jgtconstants import ZONE_SIGNAL as ZONE_DEFAULT_COLNAME


def mfi_str_to_id(mfi_str:str)->int:
    if mfi_str == MFI_SQUAT_STR:
        return MFI_SQUAT_ID
    elif mfi_str == MFI_FAKE_STR:
        return MFI_FAKE_ID
    elif mfi_str == MFI_FADE_STR:
        return MFI_FADE_ID
    elif mfi_str == MFI_GREEN_STR:
        return MFI_GREEN_ID
    else:
        return 0

def mfi_signal_to_str(mfi_signal:int)->str:
    if mfi_signal == MFI_SQUAT:
        return MFI_SQUAT_STR
    elif mfi_signal == MFI_FAKE:
        return MFI_FAKE_STR
    elif mfi_signal == MFI_FADE:
        return MFI_FADE_STR
    elif mfi_signal == MFI_GREEN:
        return MFI_GREEN_STR
    else:
        return "0"

def get_mfi_features_column_list_by_timeframe(t:str,mfi_colname=""):
    """
    Get the list of columns that are MFI features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the MFI features columns for.
    mfi_colname (str): The name of the MFI column to use. Default is MFI_VAL (plan to upgrade to MFI_SIGNAL)
    
    Returns:
    list: The list of columns that are MFI features for the given timeframe and its related timeframes
    """
    if mfi_colname=="":
        mfi_colname=MFI_DEFAULT_COLNAME
    mfi_str_selected_columns = [mfi_colname+'_M1',mfi_colname+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      mfi_str_selected_columns.append(mfi_colname+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        mfi_str_selected_columns.append(mfi_colname+'_H4')
        
    if t=='m15' or t=='m5':
        mfi_str_selected_columns.append(mfi_colname+'_H1')
    
    if t=='m5':
        mfi_str_selected_columns.append(mfi_colname+'_m15')
        
    mfi_str_selected_columns.append(mfi_colname)
    return mfi_str_selected_columns



from jgtconstants import (ZONE_BUY_ID, ZONE_BUY_STR, ZONE_INT, ZONE_NEUTRAL_ID,
                          ZONE_NEUTRAL_STR, ZONE_SELL_ID, ZONE_SELL_STR)


def zone_str_to_id(zone_str:str)->int:
    if zone_str == ZONE_BUY_STR:
        return ZONE_BUY_ID
    elif zone_str == ZONE_SELL_STR:
        return ZONE_SELL_ID
    elif zone_str == ZONE_NEUTRAL_STR:
        return ZONE_NEUTRAL_ID
    else:
        return ZONE_NEUTRAL_ID

def zone_id_to_str(zone_id:int)->str:
    if zone_id == ZONE_BUY_ID:
        return ZONE_BUY_STR
    elif zone_id == ZONE_SELL_ID:
        return ZONE_SELL_STR
    elif zone_id == ZONE_NEUTRAL_ID:
        return ZONE_NEUTRAL_STR
    else:
        return ZONE_NEUTRAL_STR




#get_zone_columns_list
#get_mfi_features_column_list_by_timeframe
def get_zone_features_column_list_by_timeframe(t:str,zone_colname=""):
    """
    Get the list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the list of ZONE features for.
    zone_colname (str): The name of the ZONE column to use. If not provided, the default ZCOL is used. (Planning to use ZONE_SIGNAL)
    
    Returns:
    list: The list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    """
    if zone_colname=="":
        zone_colname=ZONE_DEFAULT_COLNAME
    
    zcol_ctx_selected_columns = [zone_colname+'_M1',zone_colname+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      zcol_ctx_selected_columns.append(zone_colname+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_H4')
        
    if t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_H1')
    
    if t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_m15')
        
    zcol_ctx_selected_columns.append(zone_colname)
    return zcol_ctx_selected_columns
  