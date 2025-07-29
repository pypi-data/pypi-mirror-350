import os
import re
from datetime import datetime, timedelta

import tlid
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


def get_dt_format_pattern(end_datetime):
  # List of possible datetime formats with corresponding regex patterns
  formats = [
    ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}$"),
    ("%y-%m-%d", r"\d{2}-\d{2}-\d{2}$"),
    ("%Y-%m-%d %H:%M", r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"),
    ("%y-%m-%d %H:%M", r"\d{2}-\d{2}-\d{2} \d{2}:\d{2}$"),
  ]
  dt_pattern = "%y-%m-%d"  # default

  # Try to match the end_datetime string with each pattern
  for date_format, pattern in formats:
    if re.match(pattern, end_datetime):
      dt_pattern = date_format
      break
  else:
    raise ValueError(f"Invalid date format in end_datetime: {end_datetime}")

  return dt_pattern

def calculate_start_datetime(end_datetime, timeframe, periods):
  # Check if end_datetime is in tlid format
  #date_format = "%Y-%m-%d" if len(end_datetime.split('-')[0]) == 4 else "%y-%m-%d"
  date_format = get_dt_format_pattern(end_datetime)
  
  #print("date_format: ",date_format)
  # Parse end_datetime string into datetime object
  end_datetime = datetime.strptime(end_datetime, date_format)
  
  
  # If the year is less than 100, add 2000 to it to get the correct century
  if end_datetime.year < 100:
      end_datetime = end_datetime.replace(year=end_datetime.year + 2000)
  #print(end_datetime)
  
  # Check if timeframe is in hours
  if timeframe.startswith('H'):
    # Convert timeframe from hours to minutes
    timeframe_minutes = int(timeframe[1:]) * 60
  elif timeframe.startswith('D'):
    # Convert timeframe from days to minutes
    timeframe_minutes = int(timeframe[1:]) * 24 * 60
  elif timeframe.startswith('W'):
    # Convert timeframe from weeks to minutes
    timeframe_minutes = int(timeframe[1:]) * 7 * 24 * 60
  elif timeframe.startswith('M'):
    # Convert timeframe from months to minutes
    # Assume an average of 30 days per month
    timeframe_minutes = int(timeframe[1:]) * 30 * 24 * 60
  elif timeframe.startswith('m'):
    # Convert timeframe from minutes
    timeframe_minutes = int(timeframe[1:])
  else:
    # Assume timeframe is already in minutes
    timeframe_minutes = int(timeframe)
  
  # Convert timeframe from minutes to seconds
  timeframe_seconds = timeframe_minutes * 60
  # Calculate total seconds for all periods
  total_seconds = timeframe_seconds * periods
  # Calculate start datetime
  start_datetime = end_datetime - timedelta(seconds=total_seconds)
  
  return start_datetime


def calculate_tlid_range(end_datetime, timeframe, periods):
  
  # Calculate start datetime
  start_datetime = calculate_start_datetime(end_datetime, timeframe, periods)
  
  dt_pattern = get_dt_format_pattern(end_datetime)
  start_datetime_formatted = start_datetime.strftime(dt_pattern)
  
  # Format start and end datetime to tlid format
  start_tlid = tlid.fromdtstr(start_datetime_formatted)
  end_tlid = tlid.fromdtstr(end_datetime)
  #print("LEnght of enddate:" , len(end_datetime))
  #print("dt_pattern: ",dt_pattern)
  
  # Return tlid range
  return f"{start_tlid}_{end_tlid}"




def calculate_quote_counts_tf(month_amount):
    # The base data
    M1 = month_amount
    W1 = M1 * 4 
    D1 = 22 * M1
    H8 = D1 * 3 
    H6 = D1 * 4 
    H4 = D1 * 6 
    H3 = D1 * 8 
    H2 = D1 * 12
    H1 = D1 * 24
    m30 = H1 * 2 
    m15 = H1 * 4 
    m5 = H1 * 12 
    m1 = H1 * 60

    # Create a dictionary with the calculated data
    data = {
        "M1": M1,
        "W1": W1,
        "D1": D1,
        "H8": H8,
        "H6": H6,
        "H4": H4,
        "H3": H3,
        "H2": H2,
        "H1": H1,
        "m30": m30,
        "m15": m15,
        "m5": m5,
        "m1": m1
    }

    return data



def get_nb_minutes_by_tf(tf): # previously getMinByTF(tf):
    """
    Returns the number of minutes in the given timeframe string.

    Args:
    tf (str): timeframe string, one of 'm1', 'mi1', 'min1', 'm5', 'm15', 'm30', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H8', 'D1', 'W1', 'M1'

    Returns:
    int: number of minutes in the given timeframe string
    """
    if tf == "m1" or tf == "mi1" or tf == "min1":
        return 1
    if tf == "m5":
        return 5
    if tf == "m15":
        return 15
    if tf == "m30":
        return 30
    if tf == "H1":
        return 60
    if tf == "H2":
        return 120
    if tf == "H3":
        return 180
    if tf == "H4":
        return 240
    if tf == "H5":
        return 300
    if tf == "H6":
        return 360
    if tf == "H8":
        return 480
    if tf == "D1":
        return 1440
    if tf == "W1":
        return 10080
    if tf == "M1":
        return 302400



def get_higher_tf(timeframe,default_timeframes="M1,W1,D1,H4,H1,m15,m5",quiet=True):
  if default_timeframes=="T":# try read the os var "T"
     default_timeframes=os.getenv("T","M1,W1,D1,H4,H1,m15,m5")
     if not quiet:
        print("default timeframes read from env: ",default_timeframes)

  #return None if timeframe is M1
  if timeframe == "M1":
    return None    
  # Default timeframes
  timeframes = default_timeframes.split(',')
  
  # Override non default 
  if timeframe == "H6" and "H6" not in timeframes:
    return "D1"
  if timeframe == "H3" and "H3" not in timeframes:
    if "H8" not in timeframes:
       return "D1"
    return "H8"
  if timeframe == "H2" and "H2" not in timeframes:
    return "H4"
  if timeframe == "m30" and "m30" not in timeframes:
    if "H1" not in timeframes:
       return "H4"
    return "H1"
  
  # Get the index of the supplied timeframe
  try:
    tf_index = timeframes.index(timeframe)
  except ValueError:
    return None
  
  # Get the higher timeframe
  higher_tf = timeframes[tf_index - 1] if tf_index > 0 else None
  
  return higher_tf


def get_higher_tf_by_level(timeframe, level=1,default_timeframes = "M1,W1,D1,H4,H1,m15,m5",quiet=True):
  """
  Recursively calculates the higher time frame based on the given timeframe and level.

  Parameters:
  timeframe (str): The current timeframe.
  level (int): The number of levels to go higher in timeframes. Default is 1 (the level upper).
  timeframes (str): The list of timeframes to consider. Default is "M1,W1,D1,H4,H1,m15,m5".  Use "T" to read from the environment variable "T".
  quiet (bool): If True, suppresses the print statements. Default is True.

  Returns:
  str: The higher timeframe based on the given time frame and level. Expect None if there is no level.
  """
  htf = get_higher_tf(timeframe,default_timeframes,quiet)
  if level > 1:
    htf = get_higher_tf_by_level(htf, level - 1,default_timeframes,quiet)
  return htf



def get_higher_tf_array(t,default_timeframes = "M1,W1,D1,H4,H1,m15,m5",sort_reverse=True,quiet=True,max_level = 5):
  # for level from 0 to 3, run jpov.get_higher_tf_by_level(t,level)
  arr=[t]  
  for level in range(0,max_level):
    tf = get_higher_tf_by_level(t,level,default_timeframes)
    if tf is not None:
      arr.append(tf)
      if not quiet:
        print(tf)
  #remove duplicate if any
  
  arr = list(set(arr))
  #order them by default_timeframes
  arr.sort(key=lambda x: default_timeframes.index(x), reverse=sort_reverse)
  return arr

def get_higher_tf_array1(t):
  # for level from 0 to 3, run jpov.get_higher_tf_by_level(t,level)
  arr=[t]
  for level in range(0,4):
    tf = get_higher_tf_by_level(t,level)
    if tf is not None:
      arr.append(tf)
      #print(tf)
  #remove duplicate if any
  
  arr = list(set(arr))
  return arr


def i2fn(i):
  """
  Converts an input instrument string to a filename compatible string.
  """
  return i.replace("/", "-")

def fn2i(ifn):
  """
  Converts a filename string to an instrument compatible string.
  """
  return ifn.replace("-", "/")

def fn2t(t):
  """
  Converts an input timeframe filename to a timeframe compatible string. 
  """
  t_fix=t if t != "mi1" else t.replace("mi1","m1")
  t_fix=t_fix if t_fix != "min1" else t_fix.replace("min1","m1")
  
  return t_fix

def t2fn(t):
  """
  Converts an input timeframe string to a filename compatible string.
  """
  t_fix=t if t != "m1" else t.replace("m1","mi1")
  return t_fix

def topovfn(i,t,separator="_"):
  """
  Returns the filename for the given instrument and timeframe.
  """
  return f"{i2fn(i)}{separator}{t2fn(t)}"

def fn2pov(fn,separator="_")->tuple:
  """
  Converts a filename string to a pov compatible string.
  """
  arr=fn.split(separator)
  i:str=fn2i(arr[0])
  t:str=fn2t(arr[1])
  return i,t
  