
"""
Here we would have common data functions such as : write_patternname_columns_list and read_patternname_columns_list

Therefore: 
 * ttfcli would  
"""
import os
import pandas as pd
from mlutils import get_basedir,get_outfile_fullpath,get_list_of_files_in_ns
from mlconstants import PATTERN_NS, TTF_NOT_NEEDED_COLUMNS_LIST, default_columns_to_get_from_higher_tf,TTF_DTYPE_DEFINITION



settings:dict = {}

def load_settings(custom_path=None,args=None):
  global settings
  if args is not None:
    if hasattr(args,"jgtcommon_settings"):
      _settings=getattr(args,"jgtcommon_settings")
      settings.update(_settings)
  if settings is None or len(settings)==0:
    from jgtutils.jgtcommon import load_settings as jgtcommon_load_settings
    settings = jgtcommon_load_settings(custom_path)
  return settings

def get_settings():
  global settings
  if settings is None or len(settings)==0:
    settings=load_settings()
  return settings

if __name__ != "__main__": 
  load_settings()


#ttf


def get_ttf_outfile_fullpath(i,t,use_full=True,suffix="",ns="ttf",pn="ttf"):
  return get_outfile_fullpath(i,t,use_full,ns,pn=pn,suffix=suffix)


def write_patternname_columns_list(i,t,use_full=True,columns_list_from_higher_tf=None,pn="ttf",ns="ttf",suffix="_columns"):
  if columns_list_from_higher_tf is None:
    columns_list_from_higher_tf = default_columns_to_get_from_higher_tf
  output_filename=get_ttf_outfile_fullpath(i,t,use_full,suffix=suffix,pn=pn,ns=ns)
  with open(output_filename, 'w') as f:
    for item in columns_list_from_higher_tf:
      f.write("%s\n" % item)
  print(f"    Pattern:{pn} Output columns :'{output_filename}'")
  return output_filename

def read_patternname_columns_list(i,t,use_full=True,pn="ttf",ns="ttf",suffix="_columns")->list:
  output_filename=get_ttf_outfile_fullpath(i,t,use_full,suffix=suffix,pn=pn,ns=ns)
  #if not os.path.exists(output_filename), we would try to read from the pndata...
  flag_we_have_pattern_stored_specific_to_pov = os.path.exists(output_filename)
  #flag_we_have_pattern_stored_specific_to_pov=False # BYPASS FOR DEVELOPMENT
  if not flag_we_have_pattern_stored_specific_to_pov:
    raw_columns = pndata__read_new_pattern_columns_list(pn=pn)
    raise NotImplementedError("We Require to Add the Timeframe Columns to the Pattern")
    return raw_columns
  with open(output_filename, 'r') as f:
    columns_list_from_higher_tf = f.readlines()
  columns_list_from_higher_tf = [x.strip() for x in columns_list_from_higher_tf]
  return columns_list_from_higher_tf

def create_filebase_from_patternname(i,t,pn="ttf")->str:
  ifn=i.replace("/","-")
  output_filename = f"{ifn}_{t}_{pn}"
  return output_filename.replace("__","_").replace('"','')

def create_filensbase_from_patternname(i,t,pn="ttf",ns="ttf")->str:
  filebase=create_filebase_from_patternname(i,t,pn)
  return f"{ns}/{filebase}"


#@STCIssue Future Generic we would use for other patterns (ex.  targets/mx)
def read_pattern_raw(i, t,pn,ns, use_full=True)->pd.DataFrame:

  outfile_fullpath=get_outfile_fullpath(i,t,use_full,ns,pn=pn)
  df=pd.read_csv(outfile_fullpath, index_col=0,dtype=TTF_DTYPE_DEFINITION)
  return df


def read_ttf_pattern_raw(i, t, use_full=True,pn="ttf",ns="ttf")->pd.DataFrame:
  ttf_outfile_fullpath=get_ttf_outfile_fullpath(i,t,pn=pn,ns=ns,use_full=use_full)
  df=pd.read_csv(ttf_outfile_fullpath, index_col=0,dtype=TTF_DTYPE_DEFINITION)
  return df
  

def read_ttf_feature_columns_only_from_pattern(i, t, use_full=True,pn="ttf",ns="ttf"):
  df=read_ttf_pattern_raw(i, t, use_full=use_full,pn=pn,ns=ns)
  pattern_columns_list:list=read_patternname_columns_list(i,t,pn=pn,ns=ns)
  #keep only the columns from the list
  df=df[pattern_columns_list]
  return df


MLF_NS = "mlf"

def write_mlf_pattern_lagging_columns_list(i, t, use_full=True, pn="ttf", lagging_columns=None):
  print("WARN::write_mlf_pattern_lagging_columns_list::WILL BE DEPRECATED")
  write_patternname_columns_list(i,t,use_full,lagging_columns,pn=pn,ns=MLF_NS)

def read_mlf_pattern_lagging_columns_list(i, t, use_full=True, pn="ttf"):
  #@STCIssue UPGRADE TO USE THE PATTERNNAME / Settings - REPLACE by : pndata__read_new_pattern_columns_list_with_htf_and_lags_using_settings
  #lagging_columns=read_patternname_columns_list(i,t,use_full,pn=pn,ns=MLF_NS)
  lagging_columns=pndata__read_new_pattern_columns_list_with_htf_and_lags_using_settings(t,pn,lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_')
  return lagging_columns

def read_mlf_pattern_raw(i, t, use_full=True,pn="ttf"):
  df=read_ttf_pattern_raw(i, t, use_full=use_full,pn=pn,ns=MLF_NS)
  return df

def pto_read_pattern_columns_list_with_higher_tf(i, t, use_full=True, pn="ttf"):
  raise NotImplementedError("""
  #@STCGoal See : pndata__read_new_pattern_columns_list_with_htf
                            """)
#   columns_list_from_higher_tf = read_patternname_columns_list(i,t,use_full,pn=pn,ns="ttf")
#   return columns_list_from_higher_tf


def read_mlf_for_pattern(i, t, use_full=True,pn="ttf"):
  df=read_ttf_pattern_raw(i, t, use_full=use_full,pn=pn,ns=MLF_NS)
  return df

def read_mlf_feature_columns_only_from_pattern(i, t, use_full=True,pn="ttf"):
  df=read_mlf_for_pattern(i, t, use_full=use_full,pn=pn)
  lagging_columns_list:list=read_mlf_pattern_lagging_columns_list(i,t,pn=pn,use_full=use_full)
  #keep only the columns from the list
  df=df[lagging_columns_list]
  return df



def pndata__write_new_pattern_columns_list(columns_list_from_higher_tf, pn, suffix=""):
    if columns_list_from_higher_tf is None:
        raise ValueError("columns_list_from_higher_tf cannot be None")
    pattern_filename=get_outfile_fullpath("-","-",True,PATTERN_NS,pn=pn,suffix=suffix)
    with open(pattern_filename, 'w') as f:
        for item in columns_list_from_higher_tf:
            f.write("%s\n" % item)
    print(f"Pattern: {pn} Output columns: '{pattern_filename}'")
    return pattern_filename

def pndata__get_all_patterns_from_settings(args=None):
  global settings
  if settings is None or len(settings)==0:
    settings=load_settings(args=args)
  if "patterns" in settings:
    patterns_data = settings["patterns"]
    return patterns_data
  return {}

#get_list_of_files_in_ns
#@DeprecationWarning("Use of JGT Settings to Define patterns")
def pndata__get_all_patterns(use_full=True,output_type="object",args=None):
  list_of_files=get_list_of_files_in_ns(use_full,PATTERN_NS)
  #read all files in the directory and make a dictionary of the pattern names and their columns
  o={}
  for f in list_of_files:
    pn=f.split(".")[0]
    #print(f"Pattern: {pn}")
    columns_of_the_pattern=pndata__read_new_pattern_columns_list(pn=pn,args=args)
    #print(f"Columns: {columns_of_the_pattern}")
    p={"columns":columns_of_the_pattern}
    o[pn]=p
  
  patterns_in_settings=pndata__get_all_patterns_from_settings(args=args)
  o.update(patterns_in_settings)
  
  if output_type=="json":
    import json
    return json.dumps(o, indent=4)
  if output_type=="md":
    return _patterns_dictionary_to_markdown(o)
  return o

def _patterns_dictionary_to_markdown(patterns_dictionary):
    _out_string = "| Pattern | Columns |"
    _out_string += "\n"+ "| --- | --- |"
                
    for k,v in patterns_dictionary.items():
        _line = f"| {k} | "
        _columns_list = v['columns']
        _len_of_columns = len(_columns_list)
        for c in _columns_list:
            coma_if_not_last = "," if _columns_list.index(c) < _len_of_columns-1 else ""
            _line += f"{c}{coma_if_not_last}"
        _line += " |"
        #{v['columns']} |"
        _out_string += "\n"+_line
    return _out_string 


def pndata__read_new_pattern_columns_list(pn, suffix="",args=None)->list[str]:
    global settings
    if settings is None or len(settings)==0:
        settings=load_settings(args=args)

    
    pattern_filename=get_outfile_fullpath("-","-",True,PATTERN_NS,pn=pn,suffix=suffix)
    #Support reading from the args if not none
    if args is not None:
      if hasattr(args,"columns_list_from_higher_tf") and args.columns_list_from_higher_tf is not None:
        return args.columns_list_from_higher_tf
    
    if "patterns" in settings and pn in settings["patterns"]:
      patterns=settings["patterns"]
      if pn in patterns:
        pattern_columns_values = patterns[pn]["columns"]
        return pattern_columns_values
    
    if not os.path.exists(pattern_filename):
      raise FileNotFoundError(f"File {pattern_filename} does not exist.  Use -clh <col1 col2 ...> to create it.")
    
    with open(pattern_filename, 'r') as f:
        columns_list = [line.strip() for line in f]
    #print(f"Pattern: {pn} Read columns: {columns_list}")
    return columns_list

from jgtutils import jgtpov as jpov
def _ptottf__make_htf_created_columns_array(workset,t,columns_list_from_higher_tf):

  created_columns=[]
  for c in columns_list_from_higher_tf:
    for k in workset:
      if not c in created_columns: 
        created_columns.append(c)
      new_col_name = c+"_"+k
      if k != t:
        if not new_col_name in created_columns: 
          created_columns.append(new_col_name)
  return created_columns

def pndata__read_new_pattern_columns_list_with_htf(t:str,pn:str, suffix="",args=None):
  #Pattern and its columns without the Higher Timeframe features
  raw_pattern_column_list:list[str]=pndata__read_new_pattern_columns_list(pn=pn,suffix=suffix,args=args)
  povs = jpov.get_higher_tf_array(t)
  created_columns=_ptottf__make_htf_created_columns_array(povs,t,raw_pattern_column_list)
  return created_columns

def pndata__read_new_pattern_columns_list_with_htf_and_lags_using_settings(t,pn, lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_',args=None):
  columns_to_add_lags_to=pndata__read_new_pattern_columns_list_with_htf(t,pn,args=args)
  
  new_cols = _get_lagging_columns_list(columns_to_add_lags_to, lag_period=lag_period, total_lagging_periods=total_lagging_periods, out_lag_midfix_str=out_lag_midfix_str)
  
  extended_columns_list = columns_to_add_lags_to+new_cols
  return extended_columns_list


def _get_lagging_columns_list(columns_to_add_lags_to, lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_'):
    new_cols = []  # List to hold new lagging columns
    for col in columns_to_add_lags_to:
        for j in range(1, total_lagging_periods + 1):
            lag_col_name = _create_lag_column_name(out_lag_midfix_str, col, j)
            new_cols.append(lag_col_name)
    return new_cols
  
def _create_lag_column_name(out_lag_midfix_str, col, j):
    return f'{col}{out_lag_midfix_str}{j}'