

import os

OFFERS_CSV_DATA="""18,CAD/JPY
1010,SPX500
2020,WHEATF
3008,2USNote
3,GBP/USD
36,EUR/NOK
14,EUR/AUD
3004,5USNote
17,AUD/JPY
32,EUR/SEK
21,GBP/NZD
2003,SOYF
1035,EUSTX50
1002,ESP35
89,NZD/CHF
96,EUR/HUF
1013,US30
3011,FED30D
4,USD/CHF
22,GBP/AUD
13,GBP/CHF
1001,AUS200
15,EUR/CAD
90,CAD/CHF
1012,UK100
4001,XAU/USD
3005,10USNote
39,AUD/CHF
91,NZD/CAD
2,USD/JPY
30,USD/SEK
5,EUR/CHF
38,USD/MXN
83,USD/TRY
3010,Schatz
1008,NAS100
97,USD/HUF
1,EUR/USD
20,GBP/CAD
16,AUD/CAD
1060,US2000
1004,GER30
12,CHF/JPY
50,USD/HKD
37,USD/NOK
2001,USOil
1058,USDOLLAR
1007,JPN225
98,TRY/JPY
71,ZAR/JPY
9,EUR/GBP
47,USD/ZAR
105,USD/CNH
4002,XAG/USD
2021,CORNF
6,AUD/USD
11,GBP/JPY
1003,FRA40
3001,Bund
2015,NGAS
2002,UKOil
8,NZD/USD
1005,HKG33
3012,EURIBOR3M
19,NZD/JPY
40,EUR/NZD
28,AUD/NZD
3014,SONIA3M
3009,Bobl
1016,Copper
87,EUR/TRY
7,USD/CAD
10,EUR/JPY"""

def offer_id_to_instrument(offer_id):
    for line in OFFERS_CSV_DATA.split("\n"):
        if line.startswith(str(offer_id) + ","):
            return line.split(",")[1]
    return None

def instrument_to_offer_id(symbol):
    for line in OFFERS_CSV_DATA.split("\n"):
        if line.split(",")[1] == symbol:
            return int(line.split(",")[0])
    return None

def offers_to_dict():
    dict = {}
    for line in OFFERS_CSV_DATA.split("\n"):
        dict[int(line.split(",")[0])] = line.split(",")[1]
    return dict

def instruments_to_dict():
    dict={}
    for line in OFFERS_CSV_DATA.split("\n"):
        dict[line.split(",")[1]] = int(line.split(",")[0])
    return dict


from jgtos import ensure_directory_exists, fix_path_ext, mkfn_cdata_filepath
from jgtcliconstants import JGT_FXDATA_NS,JGT_HOOK_NS
from jgtos import get_data_path
def mkfn_cfxdata_filepath(fn,use_local=True,ext=None):
    #.replace(f".{ext}.{ext}",f".{ext}")
    if use_local:
        fpath = mkfn_cdata_filepath( fn)

    else :
        fx_dir_path=get_data_path(JGT_FXDATA_NS)
        fpath = os.path.join(fx_dir_path,fn)
    if ext is not None:
        fpath = fix_path_ext(ext, fpath)
    cleaned_filepath = fpath.replace("_.",".")
    #ensure_directory_exists(cleaned_filepath)
    return cleaned_filepath



def is_entry_stop_valid(entry_rate,stop_rate,bs):
    """
    Entry Rate and Stop Rate validation
    
    """
    if bs=="S":
        if entry_rate<stop_rate:
            return True
        else:
            return False
    elif bs=="B":
        if entry_rate>stop_rate:
            return True
        else:
            return False