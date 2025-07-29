# %%

import os
import json
import sys
import shutil
import signal
import atexit
from contextlib import contextmanager

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
from datetime import datetime,timedelta
import tlid
from xhelper import count_bars_before_zero_line_cross
from SOHelper import get_bar_at_index,get_last_two_bars

from jgtutils.coltypehelper import DTYPE_DEFINITIONS
from jgtutils.jgtconstants import ZONE_SIGNAL,MFI_FADE,MFI_SQUAT
#@STCGoal Standardize the Signal Columns
from mlconstants import (
  NORMAL_MOUTH_IS_OPEN_COLNAME,
  CURRENT_BAR_IS_OUT_OF_NORMAL_MOUTH_COLNAME,
  CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME,
  BIG_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_LIPS_COLNAME,
  MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME,
  CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME,
  TIDE_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_LIPS_COLNAME,
  MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME
)

# Global variables for cleanup
_cleanup_handlers = []
_temp_files = []

def register_cleanup(handler):
    """Register a cleanup handler to be called on exit"""
    _cleanup_handlers.append(handler)

def register_temp_file(filepath):
    """Register a temporary file to be cleaned up on exit"""
    _temp_files.append(filepath)

@contextmanager
def safe_file_operation(filepath, mode='r'):
    """Safely handle file operations with proper cleanup"""
    try:
        with open(filepath, mode) as f:
            yield f
    except Exception as e:
        print(f"Error operating on file {filepath}: {e}")
        raise

def cleanup():
    """Execute all registered cleanup handlers and remove temp files"""
    for handler in _cleanup_handlers:
        try:
            handler()
        except Exception as e:
            print(f"Error in cleanup handler: {e}")
    
    for filepath in _temp_files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error removing temp file {filepath}: {e}")

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\nReceived interrupt signal. Cleaning up...")
    cleanup()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Register cleanup on exit
atexit.register(cleanup)

# Validity of cache
def is_timeframe_cached_valid(df, timeframe:str,use_utc=True,quiet=True):
  """
  Checks if the cached data is still valid for the given timeframe.

  Args:
    df: The cached DataFrame.
    timeframe: The timeframe to check.

  Returns:
    True if the cache is valid, False otherwise.
  """
  try:
    
    # Get the last bar's timestamp.
    if "Date" in df.columns:
      last_bar_timestamp = df.iloc[-1]["Date"]
    else:
      last_bar_timestamp = df.index[-1]
    
    # Ensure the timestamp is in UTC if required
      if use_utc:
        last_bar_timestamp = pd.to_datetime(last_bar_timestamp, utc=True)
        now = datetime.utcnow().replace(tzinfo=pd.Timestamp.utcnow().tzinfo)
      else:
        last_bar_timestamp = pd.to_datetime(last_bar_timestamp)
        now = datetime.now()
    #quiet=False
    if not quiet:
      print(f"DEBUG::UTC::last_bar_timestamp:{last_bar_timestamp} now:{now}")
    # Calculate the valid range for the timeframe.
    if timeframe == "m1":
      valid_range = pd.Timedelta(minutes=1)
    elif timeframe == "m5":
      valid_range = pd.Timedelta(minutes=5)
    elif timeframe == "m15":
      valid_range = pd.Timedelta(minutes=15)
    elif timeframe == "m30":
      valid_range = pd.Timedelta(minutes=30)
    elif timeframe == "H1":
      valid_range = pd.Timedelta(hours=1)
    elif timeframe == "H2":
      # Calculate the next expiration time for H2 timeframe
      next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
      while next_expiration <= now:
        next_expiration += timedelta(hours=2)
      is_within_expiration = now < next_expiration
      return is_within_expiration
    elif timeframe == "H3":
      next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
      while next_expiration <= now:
        next_expiration += timedelta(hours=3)
      is_within_expiration = now < next_expiration
      return is_within_expiration
    elif timeframe == "H4":
      # Calculate the next expiration time for H4 timeframe
      next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
      while next_expiration <= now:
        next_expiration += timedelta(hours=4)
      is_within_expiration = now < next_expiration
      return is_within_expiration
    elif timeframe == "H6":
      next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
      while next_expiration <= now:
        next_expiration += timedelta(hours=6)
      is_within_expiration = now < next_expiration
      return is_within_expiration
    elif timeframe == "H8":
      next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
      while next_expiration <= now:
        next_expiration += timedelta(hours=8)
      is_within_expiration = now < next_expiration
      return is_within_expiration
    elif timeframe == "D1":
      valid_range = pd.Timedelta(days=1)
    elif timeframe == "W1":
      valid_range = pd.Timedelta(days=7)
    elif timeframe == "M1":
      valid_range = pd.Timedelta(days=30)
    else:
      raise ValueError("Invalid timeframe.")
    if not quiet:
      print("DEBUG::valid_range:",valid_range)
    # Check if the last bar's timestamp is within the valid range.
    return last_bar_timestamp + valid_range > now
  except Exception as e:
    if not quiet:print(f"Cache invalid {timeframe}")
    return False


# %% [markdown]
# # --@STCGoal Proto Scan FDB Signal Analysis
# 

# %%
from jgtpy import JGTCDSSvc as svc

from jgtutils.jgtconstants import LOW,HIGH,FDB

import JGTBalanceAnalyzer as ba
import pandas as pd

# %% [markdown]

# # CDS Data gets added ctx bar Ctx gator
#use_cache=True
cds_cache_file_suffix = "_cds_cache"
jgt_cache_root_dir="/srv/lib/jgt/cache"
no_cache=False
#look if writable, able to create otherwise use $HOME/.cache/jgt/cache


# %%
def _make_cached_filepath(i, t,subdir="fdb_scanners",ext="csv",suffix=""):
  ifn=i.replace("/","-")
  fn = f"{ifn}_{t}{suffix}.{ext}"
  #make sure the subdir exists
  cache_dir_fullpath=os.path.join(jgt_cache_root_dir,subdir)
  os.makedirs(cache_dir_fullpath,exist_ok=True)
  fpath=os.path.join(cache_dir_fullpath,fn)
  return fpath.replace("..", ".")

def generate_fresh_and_cache(_i,_t,_quotescount=300,cache_filepath=None):
    """Generate fresh data and cache it with proper error handling"""
    global cds_cache_file_suffix
    if cache_filepath is None:
        cache_filepath = _make_cached_filepath(_i, _t,suffix=cds_cache_file_suffix)
    
    try:
        dfsrc:pd.DataFrame=svc.get(_i,_t,quotescount=_quotescount)
        with safe_file_operation(cache_filepath, 'w') as f:
            dfsrc.to_csv(f)
        return dfsrc
    except Exception as e:
        print(f"Error generating fresh data for {_i} {_t}: {e}")
        if os.path.exists(cache_filepath):
            try:
                os.remove(cache_filepath)
            except:
                pass
        raise

def get_jgt_cache_root_dir():
    env_val = os.environ.get("JGT_CACHE")
    if env_val:
        # Always join subdirs relative to this, so ensure it's absolute and normalized
        return os.path.abspath(os.path.expanduser(env_val))
    return os.path.join(os.path.expanduser("~"), ".cache/jgt")

jgt_cache_root_dir = get_jgt_cache_root_dir()
os.makedirs(jgt_cache_root_dir, exist_ok=True)  # 🧠 Ensure the cache root exists before any subdirectory is created.

def _ini_cache():
  global cds_cache_file_suffix
  global jgt_cache_root_dir
  if not os.access(jgt_cache_root_dir, os.W_OK):
    home_cache = os.path.join(os.path.expanduser("~"), ".cache/jgt")
    if jgt_cache_root_dir != home_cache:
      jgt_cache_root_dir = home_cache
      try:
        os.makedirs(jgt_cache_root_dir, exist_ok=True)
      except:
        raise Exception("Unable to create cache dir")
      if not os.access(jgt_cache_root_dir, os.W_OK):
        raise Exception("Cache dir not writable")

from jgtutils import jgtcommon





instruments = "AUD/NZD,NZD/CAD,AUD/CAD,SPX500,EUR/USD,GBP/USD,XAU/USD,USD/CAD"
instruments = "AUD/NZD,NZD/CAD,AUD/CAD"
instruments = "SPX500,EUR/USD,GBP/USD,AUD/USD,XAU/USD,USD/CAD,AUS200,USD/JPY,EUR/CAD,AUD/CAD,NZD/CAD,AUD/NZD"
instruments="SPX500"
instruments = "SPX500,EUR/USD,GBP/USD,AUD/USD,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD,NZD/CAD,AUD/NZD,CAD/JPY"

timeframes = "H1,m15,m5,m1"
timeframes = "D1,H4,H1,m15,m5,m1"
timeframes = "D1,H4,H2,H1,m15,m5,m1"
timeframes = "H8,H6,H4,H3,H2,H1,m15,m5"
timeframes = "H8,H4,H1,m15,m5"
timeframes = "m15,m5,m1"
timeframes = "H4,H1,m15,m5"
timeframes = "M1,W1,D1,H4,H1,m15,m5"
timeframes = "D1,H4,H1,m15,m5"
timeframes = "m15,m5,m1"
timeframes = "H1,m15,m5"
timeframes = "D1,H4,H1,m15,m5"


all_timeframes_references = "M1,W1,D1,H4,H1"


def parse_args():
  parser=jgtcommon.new_parser("FDB Scanner","Scan market for FDB signals","fdbscan",add_exiting_quietly_flag=True)
  parser=jgtcommon.add_verbose_argument(parser) 
  parser=jgtcommon.add_instrument_standalone_argument(parser)
  parser=jgtcommon.add_timeframe_standalone_argument(parser)
  parser=jgtcommon.add_demo_flag_argument(parser)
  parser.add_argument("-nc","--no-cache",action="store_true",help="Do not use cache")
  
  args=jgtcommon.parse_args(parser)
  return args

def main():
  global cds_cache_file_suffix
  global jgt_cache_root_dir
  global instruments
  global timeframes
  global no_cache
  
  _ini_cache()
  args=parse_args()
  no_cache=args.no_cache
  
  #instruments=args.instruments if args.iflag else instruments if not args.instrument else [args.instrument]
  #timeframes=args.timeframes if args.tflag else timeframes if not args.timeframe else [args.timeframe]
  instruments=jgtcommon.get_instruments(instruments)
  timeframes=jgtcommon.get_timeframes(timeframes)
  
  demo_flag=args.demo
  
    
  quiet=args.quiet
  
  verbose_level=args.verbose
  # %%
  # i="SPX500"
  # i="NZD/CAD"
  # t="D1"
  quotescount=333
  lots=1

  md_df_tail_amount = 50
  outdir="output"
    
  contexes_all = {
      "tide": {"title": "Tide Alligator"},
      "big": {"title": "Big Alligator", "name": "big"},
      "normal": {"title": "Normal Alligator", "name": "normal"}
  }
  contexes = {
      "tide": {"title": "Tide Alligator"},
      "big": {"title": "Big Alligator", "name": "big"}
  }

  save_bars=False
  
  environment_var_name_instrument = "INSTRUMENTS"
  if environment_var_name_instrument in os.environ:
    instruments=os.getenv(environment_var_name_instrument).split(",")
    print("INSTRUMENTS loaded from environment")
  lots = int(os.getenv("LOTS",lots))
  if os.getenv("LOTS") is not None:
      print("LOTS loaded from environment")
  
  environment_var_name_timeframe = "TIMEFRAMES"
  if environment_var_name_timeframe in os.environ:
    timeframes = os.getenv(environment_var_name_timeframe).split(",")
    print("TIMEFRAMES loaded from environment")
  
  previous_tlid_id = tlid.get_seconds()

  all_signals={}
  all_signals_filename=f"fdb_signals_out__{tlid.get_day()}.json"
  all_signals_dirpath=os.path.join(os.getcwd(),"data","jgt","signals")
  os.makedirs(all_signals_dirpath,exist_ok=True)
  all_signals_filepath=os.path.join(all_signals_dirpath,all_signals_filename)
  #all_signals_filepath=_make_cached_filepath("fdb_signals_",tlid.get_day(),suffix="_all_signals",ext="json",subdir="signals")
  sh_script_savedir=os.path.join(os.getcwd(),"rjgt")
  os.makedirs(sh_script_savedir,exist_ok=True)
  all_signals_filepath_bash_name=all_signals_filename.replace(".json",".sh")
  all_signals_filepath_bash=os.path.join(sh_script_savedir,all_signals_filepath_bash_name)
  
  if verbose_level>0:
    print("tail -f ",all_signals_filepath_bash)
  def _append_all_signals_filepath_bash(signal_savepath,sh_string):
    with open(all_signals_filepath_bash,"a") as f:
      f.write(sh_string)
      f.write("\n")
  _append_all_signals_filepath_bash(all_signals_filepath_bash,"# ---Scan started:"+ tlid.get_minutes())
  _append_all_signals_filepath_bash(all_signals_filepath_bash,"signals_out_json_file="+all_signals_filepath) 
  
  for i in instruments:
    zones={}
    squats={}
    fades={}
    b4zlc={}
    timeframes_to_parse = all_timeframes_references.split(",")
    #add timeframes that are not in scannable_tf
    expand_timeframe_list(timeframes_to_parse)
    #print(timeframes_to_parse)
    #exit(0)
    for t in timeframes_to_parse:
      if t == " " or t == "":
        continue
      
      cache_filepath = _make_cached_filepath(i, t,suffix=cds_cache_file_suffix)

      dfsrc:pd.DataFrame=None
      if no_cache:
        dfsrc:pd.DataFrame=generate_fresh_and_cache(i,t,quotescount)
      
      if dfsrc is None:
        try:
          dfsrc=pd.read_csv(cache_filepath,index_col=0,parse_dates=True,dtype=DTYPE_DEFINITIONS)
        except:
          dfsrc:pd.DataFrame=generate_fresh_and_cache(i,t,quotescount,cache_filepath)
    
        if not is_timeframe_cached_valid(dfsrc, t):
          if verbose_level>2:print("Cache invalid for ",t)
          dfsrc=generate_fresh_and_cache(i,t,quotescount)
      
      signal_bar,current_bar= get_last_two_bars(dfsrc)

      
      b4zlc[t]=count_bars_before_zero_line_cross(dfsrc)
      czone=signal_bar[ZONE_SIGNAL]
      zones[t]=czone
      cmfifade=signal_bar[MFI_FADE]
      cmfiquat=signal_bar[MFI_SQUAT]
      fades[t]=cmfifade
      squats[t]=cmfiquat
      
      #Break here if the timeframe is not in the original timeframes
      if t not in timeframes:
        #print("Skipping ",t, " We just loaded it for data")
        continue
      scanning_info_header = f"a=Scanning;i={i};t={t};vtlid="
      output_string = scanning_info_header #if verbose_level>0 else ""
      
      validation_timestamp = dfsrc.index[-1]
      from jgtutils.jgtos import tlid_dt_to_string
      tlid_timestamp_string = f"{tlid_dt_to_string(validation_timestamp)};"
      
      tlid_id = tlid.get_seconds()
      
      output_string += tlid_timestamp_string if tlid_timestamp_string != "" else tlid_id # if verbose_level>0 else ""


      
      while tlid_id == previous_tlid_id:
        tlid_id = tlid.get_seconds()
      
      
      
      def _get_htf_signal(timeframe):
        from jgtpy import JGTCDSSvc as csvc
        if timeframe != "M1":
          #outsig="htf_signals=\""
          outsig=""
          htf=csvc.get_higher_tf_by_level(timeframe,1)
          htf2=csvc.get_higher_tf_by_level(timeframe,2)
          #print("htf:",htf)
          
          #@STCIssue.Limitations::Expect values when you scan Higher Timeframes too
          if htf2 is not None:
            for _t in [htf2] if isinstance(htf2,str) else htf2:
              outsig=_update_htf_signal(outsig, _t,"2")
          if htf is not None:
            for _t in [htf] if isinstance(htf,str) else htf:
              outsig=_update_htf_signal(outsig, _t,"1")
          return outsig.strip() #+ "\""
        return None

      def _update_htf_signal(outsig, _t,tf_code="1",addzone=False,addfade=True,addb4zlc=True):
          if _t in zones:
            czone = f"sell" if zones[_t] < 0 else f"buy" if zones[_t] > 0 else f"gray"
            if addzone:outsig+=f"zone{tf_code}={czone};"
          if _t in fades:
            cfade = fades[_t]
            if addfade:outsig+=f"fade{tf_code}={cfade};"
          if _t in squats:
            csquat = squats[_t]
            outsig+=f"squat{tf_code}={csquat};"
          if _t in b4zlc:
            czlc = b4zlc[_t]
            if addb4zlc:outsig+=f"b4zlc{tf_code}={czlc};"
          return outsig
      
      #@STCGoal Get a Useful String on Higher Timeframes Signals
      htfsig_TMP=_get_htf_signal(t)
      tmpzone=""
      count_to=0
      count_max=len(zones)
      for k,v in zones.items():
        separator="-" if count_to<count_max-1 else ""
        zv="S" if v<0 else "B" if v>0 else "N"
        tmpzone+=f"{zv}{separator}"
        count_to+=1
      hzone="zone="+tmpzone
      htfsig_TMP+=hzone
      if verbose_level>0:
        output_string+=";" +htfsig_TMP if htfsig_TMP is not None else "htfsig=None"
      #output_string+=";"+hzone
      
      def _extra_scripting_output_callback(_i:str,_t:str,_signal_bar:pd.Series,_current_bar:pd.Series):
        _htfsig=_get_htf_signal(_i,_t,_signal_bar,_current_bar)
        if verbose_level>1:
          print(_htfsig," FROM CALLBACK passed to function create_fdb_entry_order")
        return _htfsig
        
        
      
      from SignalOrderingHelper import create_fdb_entry_order
      valid_gator_mouth_open_in_mouth=False
      valid_sig_out_mouth=True
      o,msg=create_fdb_entry_order(i,signal_bar,current_bar,
                               lots=lots,t=t,
                                          valid_gator_mouth_open_in_mouth=valid_gator_mouth_open_in_mouth,
                                          validate_signal_out_of_mouth=valid_sig_out_mouth,validation_timestamp=validation_timestamp,quiet=quiet,verbose_level=verbose_level,
                                          demo_flag=demo_flag)      
      if o is not None:
        sh=o["sh"]
        o["htfsig"]=htfsig_TMP
        sh=sh.replace("##__",htfsig_TMP)
        #output_string+="\n"
        #output_string+="\n----\n"
        output_string+="\n\n" if verbose_level==0 else ""
        output_string+=scanning_info_header if verbose_level==0 else ""
        #_found_signal_string = f" - Signal Found\n"
        #output_string+=_found_signal_string
        output_string+="\n" if verbose_level==0 else ""
        output_string+=msg
        # Write the signal to a file we can run
        ifn=i.replace("/","-")
        sh_file_per_i_tf_name=f"{ifn}_{t}_{o['tlid_id']}.sh"
        
        sh_file_fullpath=os.path.join(sh_script_savedir,sh_file_per_i_tf_name)
        with open(sh_file_fullpath,"w") as f:
          f.write(sh.replace("```sh","").replace("```",""))
        rel_sh_file_fullpath=os.path.relpath(sh_file_fullpath,os.getcwd())
        output_string+=f". {rel_sh_file_fullpath}"
        
        output_string+="\n" if verbose_level==0 else ""
        output_string+=sh
        
        
        print_output(output_string)
        from JGTOutputHelper import serialize_signal_to_json_file,serialize_signal_to_markdown_file_from_json_file
        signal_savepath=serialize_signal_to_json_file(i,t,o,signal_bar,current_bar)
        md_filepath=serialize_signal_to_markdown_file_from_json_file(signal_savepath)
        
        signal_key=f"{i}_{t}_{o['tlid_id']}"
        all_signals[signal_key]=o
        _append_all_signals_filepath_bash(all_signals_filepath_bash,sh)
      else:
        # if verbose_level==0:
        #   print(".",end="")
        if verbose_level>0:
          print_output(output_string)

      
      if save_bars:
          current_bar_fn=_make_cached_filepath(i,t,suffix="_currentbar")
          last_bar_completed_fn=_make_cached_filepath(i,t,suffix="_signalbar")
          current_bar.to_csv(current_bar_fn,index=True) 
          signal_bar.to_csv(last_bar_completed_fn,index=True) 
          
      previous_tlid_id = tlid_id
      
      
      process_balancing=False


      _future_filtering_by_big_tide_gator(md_df_tail_amount, outdir, contexes, i, t, dfsrc, process_balancing)
  
  #save all our signals
  
  with open(all_signals_filepath,"w") as f:
    json.dump(all_signals,f,indent=2)
  
  if verbose_level>0:
    print(f"Signals saved to {all_signals_filepath}")

def expand_timeframe_list(timeframes_to_parse):
    for t in timeframes:
      if "m5" in timeframes and "m15" not in timeframes_to_parse:
        timeframes_to_parse.append("m15")
      if "m1" in timeframes and "m5" not in timeframes_to_parse:
        timeframes_to_parse.append("m5")
        if "m15" not in timeframes_to_parse:
          timeframes_to_parse.append("m15")
      if t not in timeframes_to_parse:
        timeframes_to_parse.append(t)
      

def print_output(output_string):
    print(output_string.replace("\n\n","\n").replace(";;",";").replace("- ","").replace("-\n","\n"))
  

def _future_filtering_by_big_tide_gator(md_df_tail_amount, outdir, contexes, i, t, dfsrc, process_balancing):
    if process_balancing:
      r={}
      _df=None
      for bs in ["B","S"]:
        obs={}
        print("bs:",bs)
        for ctx_name,v in contexes.items():
          o={}
            #_df=dfsrc if o["df"] is None else o["df"] # Reused the new df
          if _df is None:
            _df=dfsrc
            #_df=dfsrc if _df is None else _df
          ocols=ba.generate_column_names_for_direction(ctx_name,bs)
          ctx_evaltitle =v["title"]
          o["ctx_evaltitle"]=ctx_evaltitle
          o["name"]=ctx_name
          print("k:",ctx_name," v:",ctx_evaltitle)
            #sig_ctx_mouth_is_open_and_in_ctx_lips
          df_filter=ba.filter_sig_ctx_mouth_is_open_and_in_ctx_lips(_df,bs,ctx_name)
          new_col="sig_ctx_mouth_is_open_and_in_ctx_lips"
          _df=ba.add_sig_ctx_mouth_is_open_and_in_ctx_lips(_df,bs,ctx_name,None)
            #add_sig_ctx_mouth_is_open_and_in_ctx_lips_sell
            #print(df.tail(2))
          o["df"]=_df
          o["df_filter"]=df_filter
          obs[ctx_name]=o
        r[bs]=obs
          
          #df_sig_is_in_ctx_teeth = filter_sig_is_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname) if bs=="S" else filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname)
          # df_sig_is_in_ctx_teeth = filter_sig_is_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname) if bs=="S" else filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname)
          
          
            


      os.makedirs(outdir,exist_ok=True)

      rb=r["B"]
      rs=r["S"]
      content=f"""
        """

      for ctx_name,v in contexes.items():
        ctx_evaltitle =v["title"]
        rb_ctx=rb[ctx_name]
        rs_ctx=rs[ctx_name]
        print("ctx_name:",ctx_name)
        rb_ctx_df=rb_ctx["df"]
        rs_ctx_df=rs_ctx["df"]
          #save
        df_outputfile = _make_cached_filepath(i,t,subdir=outdir,suffix=f"_bs")
        _df.to_csv(df_outputfile)
          
          #make some markdown output
        content=content+f"""
  # Total number of rows:
  {len(rb_ctx_df)}
  # {ctx_evaltitle} Buy
  {rb_ctx_df.tail(md_df_tail_amount).to_markdown()}
  ## Columns
  {rb_ctx_df.columns.to_list()}
  # {ctx_evaltitle} Sell
  {rs_ctx_df.tail(md_df_tail_amount).to_markdown()}
  ## Columns
  {rs_ctx_df.columns.to_list()}
          """

        #save
      md_output_filepath = _make_cached_filepath(i,t,subdir=outdir,suffix=f"_ctx",ext="md")
      with open(md_output_filepath,"w") as f:
          f.write(content)
          
          

def detect_green_dragon_breakout(instrument, timeframes):
    """
    Detect breakouts using the "Green Dragon Breakout" strategy.
    
    Args:
        instrument: Trading instrument symbol
        timeframes: List of timeframes to analyze
        
    Returns:
        Dictionary with breakout detection results
    """
    print(f"\n🔍 Detecting breakouts for {instrument} using Green Dragon Breakout")
    
    # Placeholder for breakout detection logic
    green_dragon_results = {
        "instrument": instrument,
        "timeframes": timeframes,
        "breakouts": []
    }
    
    # Implement the breakout detection logic here
    # For now, we'll just return an empty result
    return green_dragon_results

import shutil

def ensure_jgtfxcli_available():
    """
    🧠 Mia: Checks if 'jgtfxcli' is available in the system PATH before any invocation.
    🌸 Miette: If not found, gently guides the user to install it with a poetic nudge.
    """
    if shutil.which("jgtfxcli") is None:
        msg = (
            "\n🚨 jgtfxcli not found in your PATH!\n"
            "To restore the magic, please run: pip install -U jgtfxcon\n"
            "(This will install the CLI tool required for this script to sing in harmony.)\n"
        )
        print(msg)
        raise RuntimeError("jgtfxcli is missing. Please install it as above.")

# Example usage before any jgtfxcli invocation:
ensure_jgtfxcli_available()
# ...existing code...
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupted with CTRL+C, exiting gracefully.")
        sys.exit(0)
