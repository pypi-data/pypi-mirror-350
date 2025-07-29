from jgtconstants import *


def get_constant_col_type_by_name(colname:str):
    """
    Get the type of the column based on the column name.
    
    Parameters:
    colname (str): The column name to get the type for.
    
    Returns:
    str: The type of the column based on the column name.
    
    """
    
    """
    AOAZ_TYPE=int
AOBZ_TYPE=int
ZLC_TYPE=int
MFI_SIGNAL_TYPE = int
MFI_SQUAT_TYPE = int
MFI_GREEN_TYPE = int
MFI_FADE_TYPE = int
MFI_FAKE_TYPE = int
ZLCB_TYPE=int
ZLCS_TYPE=int
ZONE_SIGNAL_TYPE= int
SZ_TYPE=int
BZ_TYPE=int
SS_TYPE=int
SB_TYPE=int
PRICE_PEAK_ABOVE_TYPE = int
AO_PEAK_ABOVE_TYPE = int
PRICE_PEAK_BELLOW_TYPE = int
AO_PEAK_BELLOW_TYPE = int
FDB_TARGET_TYPE = float
VECTOR_AO_FDB_COUNT_TYPE = int
VECTOR_AO_FDBS_COUNT_TYPE = int
VECTOR_AO_FDBB_COUNT_TYPE= int
    """
    if colname == AOAZ:
        return AOAZ_TYPE
    elif colname == AOBZ:
        return AOBZ_TYPE
    elif colname == ZLC:
        return ZLC_TYPE
    elif colname == MFI_SIGNAL:
        return MFI_SIGNAL_TYPE
    elif colname == MFI_SQUAT:
        return MFI_SQUAT_TYPE
    elif colname == MFI_GREEN:
        return MFI_GREEN_TYPE
    elif colname == MFI_FADE:
        return MFI_FADE_TYPE
    elif colname == MFI_FAKE:
        return MFI_FAKE_TYPE
    elif colname == ZLCB:
        return ZLCB_TYPE
    elif colname == ZLCS:
        return ZLCS_TYPE
    elif colname == ZONE_SIGNAL:
        return ZONE_SIGNAL_TYPE
    elif colname == SZ:
        return SZ_TYPE
    elif colname == BZ:
        return BZ_TYPE
    elif colname == SS:
        return SS_TYPE
    elif colname == SB:
        return SB_TYPE
    elif colname == PRICE_PEAK_ABOVE:
        return PRICE_PEAK_ABOVE_TYPE
    elif colname == AO_PEAK_ABOVE:
        return AO_PEAK_ABOVE_TYPE
    elif colname == PRICE_PEAK_BELLOW:
        return PRICE_PEAK_BELLOW_TYPE
    elif colname == AO_PEAK_BELLOW:
        return AO_PEAK_BELLOW_TYPE
    elif colname == FDB_TARGET:
        return FDB_TARGET_TYPE
    elif colname == VECTOR_AO_FDB_COUNT:
        return VECTOR_AO_FDB_COUNT_TYPE
    elif colname == VECTOR_AO_FDBS_COUNT:
        return VECTOR_AO_FDBS_COUNT_TYPE
    elif colname == VECTOR_AO_FDBB_COUNT:
        return VECTOR_AO_FDBB_COUNT_TYPE
    elif colname == ACB:
        return ACB_TYPE
    elif colname == ACS:
        return ACS_TYPE
    else:
        return None
      


def get_dtype_definitions():
    """
    Get the dictionary of column names and their types.
    
    Returns:
    dict: The dictionary of column names and their types.
    
    """
    dtype_definitions = {
        AOAZ: AOAZ_TYPE,
        AOBZ: AOBZ_TYPE,
        ZLC: ZLC_TYPE,
        MFI_SIGNAL: MFI_SIGNAL_TYPE,
        MFI_SQUAT: MFI_SQUAT_TYPE,
        MFI_GREEN: MFI_GREEN_TYPE,
        MFI_FADE: MFI_FADE_TYPE,
        MFI_FAKE: MFI_FAKE_TYPE,
        ZLCB: ZLCB_TYPE,
        ZLCS: ZLCS_TYPE,
        ZONE_SIGNAL: ZONE_SIGNAL_TYPE,
        SZ: SZ_TYPE,
        BZ: BZ_TYPE,
        SS: SS_TYPE,
        SB: SB_TYPE,
        PRICE_PEAK_ABOVE: PRICE_PEAK_ABOVE_TYPE,
        AO_PEAK_ABOVE: AO_PEAK_ABOVE_TYPE,
        PRICE_PEAK_BELLOW: PRICE_PEAK_BELLOW_TYPE,
        AO_PEAK_BELLOW: AO_PEAK_BELLOW_TYPE,
        FDB_TARGET: FDB_TARGET_TYPE,
        VECTOR_AO_FDB_COUNT: VECTOR_AO_FDB_COUNT_TYPE,
        VECTOR_AO_FDBS_COUNT: VECTOR_AO_FDBS_COUNT_TYPE,
        VECTOR_AO_FDBB_COUNT: VECTOR_AO_FDBB_COUNT_TYPE,
        ACB: ACB_TYPE,ACS: ACS_TYPE
    }
    return dtype_definitions
  
DTYPE_DEFINITIONS=get_dtype_definitions()