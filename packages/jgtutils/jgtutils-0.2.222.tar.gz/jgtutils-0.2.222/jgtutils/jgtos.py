import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def ensure_directory_exists(filepath):
    #detect if the filepath is a directory or a file and if a file is supplied, create the directory where the file will be saved
    is_probably_a_filepath = filepath[-4] == "."
    if os.path.isfile(filepath) or is_probably_a_filepath:
        directory = os.path.dirname(filepath)
    else:
        directory = filepath
    #directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory

def create_filestore_path(
    instrument:str, 
    timeframe:str, 
    quiet=True, 
    compressed=False, 
    tlid_range:str=None,
    output_path:str=None,
    nsdir:str="pds",
    use_full=False
):
    # Define the file path based on the environment variable or local path
    if output_path is None:
        data_path = get_data_path(nsdir=nsdir,use_full=use_full)
    else: # get path from var in os
        data_path = os.path.join (output_path.replace("/"+nsdir,""),nsdir)
    
    if not quiet:
        print(data_path)

    ext = "csv"
    if compressed:
        ext = "csv.gz"

    fpath = mk_fullpath(instrument, timeframe, ext, data_path, tlid_range=tlid_range)

    if os.name == "nt":
        fpath = fpath.replace("/", "\\")
    return fpath

def fix_timeframed_path(timeframe, original_path):
    if timeframe=="m1":
        updated_path = original_path.replace("m1","mi1")
    else:
        updated_path = original_path
    return updated_path

def mk_fn(instrument:str, 
          timeframe:str, 
          ext:str="csv"):
    """Make a file name with instrument and timeframe

    Args:
        instrument (str): symbol
        timeframe (str): TF
        ext (str): ext name "csv"

    Returns:
        str: file name
    """
    _tf = timeframe
    _i = instrument.replace("/", "-")
    if timeframe == "m1":
        _tf = timeframe.replace("m1", "mi1")
    _fn = _i + "_" + _tf + "." + ext
    return _fn.replace("..", ".")


def mk_fn_range(instrument:str, 
                timeframe:str, 
                start: datetime.datetime, 
                end: datetime.datetime, 
                ext="csv"):
    _tf = timeframe
    _i = instrument.replace("/", "-")
    if timeframe == "m1":
        _tf = timeframe.replace("m1", "mi1") #differenciate with M1
    start_str = tlid_dt_to_string(start)
    end_str = tlid_dt_to_string(end)
    _fn = f"{_i}_{_tf}_{start_str}_{end_str}.{ext}"
    # _fn= _i + '_' + _tf + '.' + ext
    _fn = _fn.replace("..", ".")
    _fn = _fn.replace("/", "-")
    return _fn

import subprocess


def create_directory_with_sudo(path):
    # Construct the command
    command = f"sudo mkdir -p -m 777 {path}"

    # Execute the command
    subprocess.run(command, shell=True)



def mk_fullpath(instrument:str, 
                timeframe:str, 
                ext:str, 
                path:str, 
                tlid_range:str=None):
    #path dont exist, try to make that directory
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except:
            print("Error creating the directory : " + path)
            print("Executing:  sudo mkdir -m 777 -p " + path)
            #execute system command sudo mkdir -p -m 777 $path
            try:
                create_directory_with_sudo(path)
                print("Directory created : " + path)
            except:
                print("Error creating the directory : " + path)
                print("Please create the directory manually:  sudo mkdir -m 777 -p " + path)
            
            
    if tlid_range is None:
        fn = mk_fn(instrument, timeframe, ext)
    else:
        start_dt, end_dt = tlid_range_to_start_end_datetime(
            tlid_range=tlid_range
        )
        # print(str(start_dt),str(end_dt))
        fn = mk_fn_range(instrument, timeframe, start_dt, end_dt, ext)
    rpath = os.path.join(path, fn)
    if os.name == "nt":
        rpath = rpath.replace("/", "\\")
    # path + '/'+fn
    return rpath




def get_data_path(nsdir: str, 
                  range_level:int=6,
                  use_full=False):
    # Try to read the path from the JGTPY_DATA environment variable
    if use_full:
        default_data_full="/var/lib/jgt/full/data"
        data_path = os.environ.get('JGTPY_DATA_FULL',default_data_full)

        #create the directory if it does not exist
        try:
            os.makedirs(data_path, exist_ok=True)
        except:
            print("Error creating the directory : " + data_path)
            print("Please create the directory manually:  sudo mkdir -m 777 -p " + data_path)
            data_path = "/data/full"
            print("Using default directory : " + data_path)
            os.makedirs(data_path, exist_ok=True)


        if not os.path.exists(data_path):
            print("Once the directory is created, you can generate the PDS/CDS manually : " + data_path)
            
            
                
    else:
        default_data="/var/lib/jgt/data"
        data_path = os.environ.get('JGTPY_DATA',default_data)
        #create the directory if it does not exist 
        try:        
            os.makedirs(data_path, exist_ok=True)
        except:                      
            print("Error creating the directory : " + data_path)                                                                          
            print("Please create the directory manually:  sudo mkdir -m 777 -p " + data_path) 
            data_path = "/data" 
            print("Using default directory : " + data_path) 
            os.makedirs(data_path, exist_ok=True) 
        
    # If the variable is defined and the path exists, return it
    if data_path and os.path.exists(data_path):
        rpath = os.path.abspath(os.path.join(data_path, nsdir))
        return rpath

    # If the variable is not defined or the path does not exist, fall back to the current behavior
    # Start with the current working directory
    base_path = os.getcwd()

    # Try up to X range levels up to find the data directory
    for _ in range(range_level):
        data_path = os.path.join(base_path, 'data')
        if os.path.exists(data_path):
            # Check if the directory has write permissions
            if not os.access(data_path, os.W_OK):
                raise Exception(f"No write access to the directory: {data_path}")
            break
        # Go one level up for the next iteration
        base_path = os.path.abspath(os.path.join(base_path, '..'))
    else:
        # If the loop completes without finding the data directory, raise an exception
        raise Exception("Data directory not found. Please create a directory named 'data' in the current, parent directory (up to 3 levels), or set the JGTPY_DATA environment variable.")

    # Replace slashes with backslashes on Windows
    if os.name == "nt":
        data_path = data_path.replace("/", "\\")

    # Append the nsdir to the data path
    data_path = os.path.abspath(os.path.join(data_path, nsdir))

    return data_path


def get_pov_local_data_filename(instrument:str,timeframe:str,use_full=False,nsdir="pds",ext="csv"):
  root_dir=get_data_path(nsdir,use_full=use_full)
  
  local_fn_suffix = ext
  full_path=mk_fullpath(instrument, timeframe, local_fn_suffix, root_dir)
  return full_path


def tlid_range_to_start_end_datetime(tlid_range: str):
    #Support inputting just a Year
    if len(tlid_range) == 4 or len(tlid_range) == 2 :
        start_str = tlid_range + "0101" + "0000"
        end_str = tlid_range +  "1231" + "2359"
    else:
        #Normal support start_end
        try:
            start_str, end_str = tlid_range.split("_")
        except:
            print("TLID ERROR - make use you used a \"_\"")
            return None,None
    
    date_format_start = "%y%m%d%H%M"
    date_format_end = "%y%m%d%H%M"
    
    if len(start_str) == 4 or len(start_str) == 2:
        start_str = start_str + "0101" + "0000"
    if len(end_str) == 4 or len(end_str) == 2 :
        end_str = end_str + "1231" + "2359"
    
    if len(start_str) == 6:
        start_str = start_str + "0000"
    if len(end_str) == 6:
        end_str = end_str + "2359"
   
    if len(start_str) == 8:
        start_str = start_str + "0000"
    if len(end_str) == 8:
        end_str = end_str + "2359"
        
    if len(start_str) == 12:
        date_format_start = "%Y%m%d%H%M"
    if len(end_str) == 12:
        date_format_end = "%Y%m%d%H%M"
   
    #print(date_format_end)
    try:
        start_dt =  datetime.datetime.strptime(start_str, date_format_start)
        end_dt = datetime.datetime.strptime(end_str, date_format_end)
        return start_dt,end_dt
    except ValueError:
        return None

def tlid_range_to_jgtfxcon_start_end_str(tlid_range: str):
    date_format_fxcon = '%m.%d.%Y %H:%M:%S'
    start_dt,end_dt = tlid_range_to_start_end_datetime(tlid_range)
    #print(str(start_dt),str(end_dt))
    if start_dt is None or end_dt is None:
        return None,None
    else:
        return str(start_dt.strftime(date_format_fxcon)),str(end_dt.strftime(date_format_fxcon))

def tlid_dt_to_string(dt: datetime.datetime):
    return dt.strftime("%y%m%d%H%M")

def tlidmin_to_dt(tlid_str: str):
    date_format = "%y%m%d%H%M"
    try:
        tlid_dt =  datetime.datetime.strptime(tlid_str, date_format)
        return tlid_dt
    except ValueError:
        pass
    
    return None

from jgtcliconstants import JGT_DATA_DIR,JGT_DATA_SUBDIRDIR
def mkfn_cdata_filepath(fn,*args):
    cdata_jgt_dir = os.path.join(os.getcwd(),JGT_DATA_DIR,JGT_DATA_SUBDIRDIR,*args)
    os.makedirs(cdata_jgt_dir, exist_ok=True)
    cfilepath=os.path.join(cdata_jgt_dir,fn)
    return cfilepath

def fix_path_ext(ext, fpath,double_underscore=False):
    """
    Fixes the file path extension.

    Parameters:
    ext (str): The desired extension to replace the existing extension.
    fpath (str): The file path to be fixed.

    Returns:
    str: The fixed file path with the desired extension.
    """
    if ext is None: # get the ext from the fn
        ext = fpath.split(".")[-1]
        if ext == fpath:
            raise Exception(f"No extension found in the file path: {fpath}")
        #print(ext)

    #check if the ext is already in the fpath
    if not fpath.endswith(f".{ext}"):
        fpath = f"{fpath}.{ext}"
        
    return sanitize_filename(fn=fpath,ext=ext,double_underscore=double_underscore)#fpath.replace(f".{ext}.{ext}",f".{ext}")


def sanitize_filename( fn,ext=None,double_underscore=True):
    if ext is None: # get the ext from the fn
        ext = fn.split(".")[-1]
    _sanitized_filename = fn.replace("_.",".").replace(f".{ext}.{ext}",f".{ext}")
    if double_underscore:
        _sanitized_filename=_sanitized_filename.replace("__","_")
    return _sanitized_filename
