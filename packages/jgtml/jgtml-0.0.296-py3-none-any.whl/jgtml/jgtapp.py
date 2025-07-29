import argparse
import json
import os
import subprocess
import sys
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtutils import jgtcommon
from jgtutils.jgtcliconstants import (CLI_FXADDORDER_PROG_NAME,CLI_FXMVSTOP_PROG_NAME,CLI_FXRMORDER_PROG_NAME,CLI_FXRMTRADE_PROG_NAME,CLI_FXTR_PROG_NAME,PDSCLI_PROG_NAME)

from jgtutils.jgtconstants import (LIPS,TEETH,JAW)
from jgtutils.jgtconstants import FDB,HIGH,LOW,CLOSE

from jgtpy.jgtpyconstants import (IDSCLI_PROG_NAME,CDSCLI_PROG_NAME,ADSCLI_PROG_NAME,MKSCLI_PROG_NAME,JGTCLI_PROG_NAME)

from jgtutils.FXTransact import FXTransactWrapper,FXTransactDataHelper as ftdh,FXTrades,FXTrade



from jgtpy.JGTIDS import _ids_add_fdb_column_logics_v2
from jgtpy import jgtapyhelper as th

#from jgtpy.JGTIDSSvc import get_ids
#from jgtpy.JGTIDSRequest import JGTIDSRequest

from SOHelper import get_bar_at_index,get_last_two_bars

from mlcliconstants import (MLFCLI_PROG_NAME,TTFCLI_PROG_NAME,PNCLI_PROG_NAME,MXCLI_PROG_NAME)

TFW_PROG_NAME = "tfw"

def w(timeframe,script_to_run=None,exit_on_timeframe=False):
  """Wrapper to run a bash script when a timeframe update is detected.
  
  (It is a wrapper of the command: tfw)
  
  usage: tfw [-h] [-ls SETTINGS] -t TIMEFRAME [-X | -S [SCRIPT_TO_RUN ...] | -C
           [CLI_TO_RUN ...] | -F FUNCTION] [-M MESSAGE] [-I IN_MESSAGE] [-N]
           [-v VERBOSE]

  JGT WTF CLI helper  
  
  options:
  -h, --help            show this help message and exit
  -ls SETTINGS, --settings SETTINGS
                        Load settings from a specific settings file (overrides default
                        settings (/etc/jgt/settings.json and HOME/.jgt/settings.json
                        and .jgt/settings.json)).
  -t TIMEFRAME, --timeframe TIMEFRAME
                        Timeframe
  -X, --exit            Exit the program when the timeframe is reached.
  -S [SCRIPT_TO_RUN ...], -B [SCRIPT_TO_RUN ...], --script-to-run [SCRIPT_TO_RUN ...]
                        Script to run when the timeframe is reached. (.jgt/tfw.sh).
  -C [CLI_TO_RUN ...], --cli-to-run [CLI_TO_RUN ...]
                        CLI to run when the timeframe is reached. (python -m
                        jgtutils.cli_test_cronrun_helper)
  -F FUNCTION, --function FUNCTION
                        Function to run when the timeframe is reached.
  -M MESSAGE, --message MESSAGE
                        Message to display when the timeframe is reached.
  -I IN_MESSAGE, --in-message IN_MESSAGE
                        Message to display when the timeframe wait starts.
  -N, --no-output       Do not output anything.
  """
  if script_to_run:
    subprocess.run([TFW_PROG_NAME, '-t', timeframe,'-N', '-B', script_to_run], check=True)
  elif exit_on_timeframe:
    subprocess.run([TFW_PROG_NAME, '-t', timeframe,'-N', '-X'], check=True)
    #print("Timeframe reached in W")
    #wait for it to exit
  else:
    subprocess.run([TFW_PROG_NAME, '-t', timeframe,'-N'], check=True)



def fxaddorder( instrument, lots, rate, buysell, stop, demo=False,flag_pips=False):
  """Add an entry order to the market.
  
  Used when an entry signal is detected.
  
  Args:
    instrument (str): Instrument to trade
    lots (str): Number of lots to trade
    rate (str): Entry rate
    buysell (str): Buy or Sell
    stop (str): Stop rate
    demo (bool, optional): Use the demo account. Defaults to False.
    flag_pips (bool, optional): Use pips as the unit for the stop rate (rather than specifying a specific price for the stop rate (useful when an instrument requires a minimal amount of pips for the entry order (example: SPX500))). Defaults to False.
  """
  pips_arg = '--pips' if flag_pips else ''
  demo_arg = '--demo' if demo else '--real'
  subprocess.run([CLI_FXADDORDER_PROG_NAME, '-i', instrument, '-n', lots, '-r', rate, '-d', buysell, '-x',stop,pips_arg , demo_arg], check=True)

def _get_order_data_fresh(orderid, demo=False):
    #Case  where the order is still in the orders and has not became a trade yet
    fxtr(orderid=orderid,demo=demo)
    fx_file_path = os.path.join("data","jgt", f"fxtransact_{orderid}.json")
    if os.path.exists(fx_file_path):
      with open(fx_file_path, "r") as f:
        fxdata = json.load(f)
      for o in fxdata.get("orders", []):
          if o.get("order_id") == orderid:
              return o
    #Case where we did not find the instrument because it might have became a trade
    fxtr(demo=demo) 
    # We will find the instrument under the property 'contingent_order_id' in the orders or in 'open_order_id' in the trades
    fx_file_path = os.path.join("data","jgt", "fxtransact.json")
    if os.path.exists(fx_file_path):
        with open(fx_file_path, "r") as f:
            fxdata = json.load(f)
        for t in fxdata.get("trades", []):
            if t.get("open_order_id") == orderid:
                return t
        for o in fxdata.get("orders", []):
            if o.get("order_id") == orderid:
                return o
        for o in fxdata.get("orders", []):
            if o.get("contingent_order_id") == orderid:
                return o
    return None

def _get_order_data(orderid, demo=False):
    fx_file_path = os.path.join("data","jgt", f"fxtransact_{orderid}.json")
    if os.path.exists(fx_file_path):
      with open(fx_file_path, "r") as f:
          fxdata = json.load(f)
      for o in fxdata.get("orders", []):
          if o.get("order_id") == orderid:
              return o
    return _get_order_data_fresh(orderid, demo)

def order_became_a_trade(orderid, demo=False):
    o=_get_order_data(orderid, demo)
    if o:
        #if o has a property 'open_order_id' == orderid, it is a trade
        if hasattr(o,"open_order_id") and o["open_order_id"]==orderid:
            return True
          
    return False

def _get_instrument_from_orderid(orderid, demo=False):
    # First, it is possible that we already have that file : ./data/jgt/fxaddorder_170492374.json   
    #Case  where the order is still in the orders and has not became a trade yet
    o=_get_order_data(orderid, demo)
    if o:
      return o.get("instrument")
    raise ValueError(f"No matching order found for {orderid}.")

def _get_buysell_from_orderid(orderid, demo=False):
  #get the buysell from the orderid
  #fxtr -id 68782480 --demo
  #get the buysell from the orderid
  o=_get_order_data(orderid, demo)
  if o:
    return o.get("buy_sell")
  raise ValueError(f"No matching order found for {orderid}.")

def _get_stop_rate_from_orderid(orderid, demo=False):
  #get the stop rate from the orderid
  #fxtr -id 68782480 --demo
  #get the stop rate from the orderid
  o=_get_order_data(orderid, demo)
  if o:
    return o.get("stop")
  raise ValueError(f"No matching order found for {orderid}.")


def entryvalidate(orderid,timeframe, demo=False): #@STCIssue At a Higher Level, ya we run this but we should have a better design and a STATE for the CAMPAIGN (entering, trading, exiting)
  """Validate that an entry order is still valid and remove it if not.
  
  Used when the timeframe of the entry order is updated to validate that the order is still valid.
  """
  demo_arg = '--demo' if demo else '--real'
  instrument=_get_instrument_from_orderid(orderid, demo)
  bs=_get_buysell_from_orderid(orderid, demo)
  stop_rate=_get_stop_rate_from_orderid(orderid,demo)#@STCIssue What happens from here when it became a trade ???? How do we know it became a trade ?? - STATE for the CAMPAIGN (entering, trading, exiting)
  became_a_trade=order_became_a_trade(orderid, demo)
  if became_a_trade:
    print("The order became a trade, we are not validating it anymore")
    return
  df = _get_ids_updated(instrument, timeframe)
  cb=get_bar_at_index(df,-1)
  clow=cb[LOW]
  cclose=cb[CLOSE]
  chigh=cb[HIGH]
  if bs=="B" and (cclose<stop_rate or clow<stop_rate):
    print("The stop rate has hit")
    fxrmorder(orderid, demo=demo)
  else:
    if bs=="S" and (cclose>stop_rate or chigh>stop_rate):
      print("The stop rate has hit")
      fxrmorder(orderid, demo=demo)
  
  
def fxrmorder(orderid, demo=False):
  """Remove an existing entry order.
  
  Used in case an order has become invalid (e.g. stop rate hit).
  """
  demo_arg = '--demo' if demo else '--real'
  subprocess.run([CLI_FXRMORDER_PROG_NAME, '-id', orderid, demo_arg], check=True)

def fxrmtrade(tradeid, demo=False):
  """Remove/Close an existing trade.
  
  Might be used by other function to close a trade in certain condition where the stop was hit or the trade is not valid anymore but still open.
  """
  demo_arg = '--demo' if demo else '--real'
  subprocess.run([CLI_FXRMTRADE_PROG_NAME, '-tid', tradeid, demo_arg], check=True)

def fxtr(tradeid=None,orderid=None, demo=False,save_flag=True):
  """Get trade details / update local trade data.
  
  (Wrapper for the command: fxtr)
  """
  save_arg = '-save' if save_flag else ''
  demo_arg = '--demo' if demo else '--real'
  if tradeid:
    subprocess.run([CLI_FXTR_PROG_NAME, '-tid', tradeid, demo_arg, save_arg], check=True)
  elif orderid:
    subprocess.run([CLI_FXTR_PROG_NAME, '-id', orderid, demo_arg, save_arg], check=True)
  else:
    subprocess.run([CLI_FXTR_PROG_NAME, demo_arg, save_arg], check=True)
  msg = "File saved."
  print_jsonl_message(msg,extra_dict={"trade_id":tradeid,"order_id":orderid },scope="jgtapp::fxtr")

def fxmvstop(tradeid,stop,flag_pips=False, demo=False,args=None):
  """Move stop for a trade"""
  pips_arg = '--pips' if flag_pips else ''
  demo_arg = '--demo' if demo else '--real'
  cli_args = [CLI_FXMVSTOP_PROG_NAME, '-tid', tradeid, '-x', stop, demo_arg]
  if pips_arg != '':
    cli_args.append(pips_arg)
  try:
    subprocess.run(cli_args, check=True)
  except subprocess.CalledProcessError as e:
    print(f"Error moving stop: {e}")
    from jgtutils.jgterrorcodes import (
      TRADE_STOP_CHANGING_EXIT_ERROR_CODE,
      TRADE_STOP_NOT_CHANGED_EXIT_ERROR_CODE,
      TRADE_STOP_INVALID_EXIT_ERROR_CODE)
    #@STCGoal Handle the error codes and ways to recover
    #@STCIssue pass the error code to the caller context.  ex. fxmvstop is ran directly from the CLI, the error code should be passed by exiting the process with the error code, else if used by fxmvstopgator, the error code should be passed to the caller context in a raised exception.
    #look at the args command to guess the context

def ids(instrument, timeframe,use_full=False,use_fresh=True):
  """Refresh the IDS data (indicator Data Service)."""
  use_fresh_arg = '-old' if not use_fresh else '--fresh'
  use_full_arg = '--full' if use_full else '-new'
  subprocess.run([IDSCLI_PROG_NAME, '-i', instrument, '-t', timeframe, use_full_arg, use_fresh_arg], check=True)

"""
fxmvstopgator -tid 68773276  --demo -i AUD/NZD -t H4 --lips
"""
#@STCGoal RM Order if Stop was Hit





#@STCGoal Move EXIT Stop On FDB Signal
fxmvstopfdb_epilog = "Move the stop to the FDB signal. If the stop is already hit, close the trade if --close is passed.  Considering we could add --lips to move the stop to the lips if no FDB signal is found #@STCIssue It would requires to detect if previously the stop was moved to an FDB signal (as we dont want to move it again back in the lips if we are still in an FDB signal)"

MOVED_TO_FDB_FLAG_NAME = "moved_to_fdb"
def fxmvstopfdb(i,t,tradeid,demo=False,close=False,lips=False,teeth=False,jaw=False,not_if_stop_closer=True):
  """Move stop to the FDB signal. 
  
  ENhance the exit to use the FDB signal (probably a better exit that using the lips).  Is used in the case that we are at the ending phase of a trading campaign.  """
  demo_arg="--demo" if demo else "--real"
  if close:
    print("Closing the trade if the stop of fdbsignal is already hit")
    raise NotImplementedError("Closing the trade if the stop of fdbsignal is already hit")
  
  
  
  
  #Update the local datafor the trade
  ## we expect : fxtransact_68782480.json
  #fxtr(tradeid=tradeid,demo=demo)
  
  trade_data = _get_trade_data(tradeid, demo)
  #just make sure we have the same instrument
  if i == "_": # use the instrument from the trade data 
    i = trade_data["instrument"]
  if not trade_data["instrument"]==i:
    print(f"Trade data instrument {trade_data['instrument']} is different from the passed instrument {i}")
    from jgtutils.jgterrorcodes import INSTRUMENT_NOT_VALID_EXIT_ERROR_CODE
    sys.exit(INSTRUMENT_NOT_VALID_EXIT_ERROR_CODE)
  

  #fuck=fxtrades[tradeid]
  #get the trade data
  #print(fxdata)
  #trade_data=ftdh.load_fxtrade_from_fxtransact(fxdata,tradeid)
  #trade_data2=fxdata.get_trade(tradeid)
  direction=trade_data["buy_sell"]
  original_stop=trade_data["stop"]
  msg = "Detected trade direction."
  print_jsonl_message(msg,extra_dict={"direction":direction,"original_stop":original_stop})
  # print(trade_data)
  #@STCIssue Why do I want that info on the Trade ??
  
    
  skip_generating_ids=False
  #if SKIP_IDS defined in os env, skip
  if os.getenv("SKIP_IDS"):
    skip_generating_ids=True
    
  if skip_generating_ids:
    print("Skipping generating IDS (JUST READING  IT FOR DEV)")
  

  dfc = _get_ids_updated(i, t)
  lcb=get_bar_at_index(dfc,-2)
  lcbfdb = lcb[FDB]
  lcbhigh=lcb[HIGH]
  lcblow=lcb[LOW]
  cb=get_bar_at_index(dfc,-1)
  clow=cb[LOW]
  cclose=cb[CLOSE]
  chigh=cb[HIGH]
  
  is_sell_fdb=lcbfdb<0
  is_buy_fdb=lcbfdb>0
  stop_price=None
  if direction=="B" and is_sell_fdb:
    stop_price=lcblow
  else:
    if direction=="S" and is_buy_fdb:
      stop_price=lcbhigh
      
  
  if stop_price:
    msg_ = f"We change the Stop for:{stop_price} from : {original_stop}"
    print(msg_)
    #@q Does our Current Bar Broke the FDB Signal ??
    #@STCIssue If close is True, we should close the trade if the stop is already hit
    stop_has_hit=False
    if direction=="B" and cclose>stop_price:
      stop_has_hit=True
    else: 
      if direction=="S" and cclose<stop_price:
        stop_has_hit=True
    msg=f"Stop has hit" if stop_has_hit else "Stop has not hit"
    print(msg)
    
    if stop_has_hit:
      msg = "The stop has hit the FDB signal, we are closing the trade"
      print_jsonl_message(msg,scope="fxmvstopfdb")
      _close_trade_cmd=f"jgtapp fxrmtrade -tid {tradeid} {demo_arg}"
      msg = f"Executing:{_close_trade_cmd}"
      print_jsonl_message(msg)
      fxrmtrade(tradeid,demo=demo)
      #print("Done")
    else:
      print("We are moving the stop to the FDB signal")
      fxmvstop(tradeid,stop_price,demo=demo)
      #write a flag so we know we moved to an FDB Signal
      flag_object={MOVED_TO_FDB_FLAG_NAME:True}
      flag_file_path = __get_fdb_moved_flag_filename(tradeid)
      with open(flag_file_path,"w"):
        json.dump(flag_object)
  
      
  else:
    #msg = "We dont have a signal, Shall we fall in set the stop to the lips ??"
    #print_jsonl_message(msg,scope="fxmvstopfdb")
    if lips or teeth or jaw:
      
      flag_moved_to_fdb=_check_flag_fdb_moved(tradeid)
      
      if flag_moved_to_fdb:
        msg = "We already moved to an FDB signal, we are not moving the stop back to the lips."
        print_jsonl_message(msg,scope="fxmvstopfdb",extra_dict={"trade_id":tradeid, "goal":"Know we had an FDB signal.  Could that be invalidated by the current bar broking the other side of our FDB Signal, therefore we would come back to the probably --lips"})
      else:
          
        line_arg="lips" if lips else "teeth" if teeth else "jaw"
        fxmvstopgator_cmd = f"jgtapp fxmvstopgator -i {i} -t {t} -tid {tradeid} --{line_arg} {demo_arg}"
        #print("We are running something like this:",fxmvstopgator_cmd)
        msg = f"Moving stop to {line_arg}"
        print_jsonl_message(msg,extra_dict={"trade_id":tradeid,"instrument":i,"timeframe":t, "line":line_arg})
        skip_update = False
        fxmvstopgator(i,t,tradeid,lips=lips,teeth=teeth,jaw=jaw,demo=demo,skip_trade_data_update=skip_update)
    else:
      msg = "No --lips, --teeth or --jaw passed, we are not moving the stop"
      print_jsonl_message(msg)

def _get_trade_data(tradeid, demo,fresh=True):
    fxtr(demo=demo,tradeid=tradeid)
    expected_fn=f"fxtransact_{tradeid}.json"

    from jgtutils.jgtfxhelper import mkfn_cfxdata_filepath
    expected_path=mkfn_cfxdata_filepath(expected_fn)
    #expected_path=os.path.join("data","jgt",expected_fn)
    #x=FXTrade.from_id(tradeid)
    #expected_path=ftdh.load_fxtransact_from_file(expected_fn)
    if not os.path.exists(expected_path):
      fresh=True
      print(f"File {expected_path} does not exist - fxtr will be ran")
    else:
      fresh=False # We have the file, we dont need to run fxtr
    
    if fresh:
      # fxtr(tradeid=tradeid,demo=demo)
      fxtr(demo=demo)
    #return
    msg = "Reading the trade data from the file:"
    print_jsonl_message(msg,extra_dict={"trade_id":tradeid,"demo":demo, "expected_fn":expected_path},scope="jgtapp")
    fxdata=ftdh.load_fxtransact_from_file(expected_path)
    trade_data:FXTrade=None
    trades:FXTrades=fxdata.trades
    #return None if no trades in the list
    for trade in trades.trades:
    #print(trade)
      if str(trade["trade_id"])==str(tradeid):
        trade_data=trade
        break
    return trade_data

def _check_flag_fdb_moved(tradeid):
    flag_file_path = __get_fdb_moved_flag_filename(tradeid)
    flag_moved_to_fdb=False
    if os.path.exists(flag_file_path):
        #Load it and check if we moved to an FDB signal is set to true
      with open(flag_file_path,"r") as f:
        flag_object=json.load(f)
        if MOVED_TO_FDB_FLAG_NAME in flag_object:
          flag_moved_to_fdb=flag_object[MOVED_TO_FDB_FLAG_NAME]
    return flag_moved_to_fdb

def __get_fdb_moved_flag_filename(tradeid):
    return f".jgt/fdb_moved_flag_{tradeid}.json"
    
  
  
  

def _get_ids_updated(i, t,skip_generating=False):
    try:
      if not skip_generating:
        ids(i,t,use_fresh=True,use_full=False)
    except:
      print("IDS failed")
  #read the last bar from the IDS csv
    df=th.read_ids(i,t)
    dfc=_ids_add_fdb_column_logics_v2(df)
    return dfc
    
  
def print_jsonl_message(msg,extra_dict:dict=None,scope=None):
  o={}
  o["message"]=msg
  if extra_dict:
      o.update(extra_dict)
  if scope:
    o["scope"]=scope
  print(json.dumps(o))

def fxmvstopgator(i,t,tradeid,lips=True,teeth=False,jaw=False,demo=False,skip_trade_data_update=False,loop_action=False):
  

  trade_data=_get_trade_data(tradeid, demo,fresh=not skip_trade_data_update)
  if trade_data is None or trade_data=={}:
    msg = f"Trade data not found for tradeid {tradeid}"
    print_jsonl_message(msg)
    from jgtutils.jgterrorcodes import TRADE_NOT_FOUND_EXIT_ERROR_CODE
    sys.exit(TRADE_NOT_FOUND_EXIT_ERROR_CODE)
    
  if i == "_": # use the instrument from the trade data
    i = trade_data["instrument"]
  
  #First update the IDS
  df = _get_ids_updated(i, t)
  #get the last bar
  current_bar=get_bar_at_index(df,-1)
  choosen_line="_"
  #get the stop from choosen indicator line (by flag)
  if not teeth and not jaw:
    lips=True # DEFAULT
  if lips:
    stop=str(current_bar[LIPS])
    choosen_line="lips"
  elif teeth:
    stop=str(current_bar[TEETH])
    choosen_line="teeth"
  elif jaw:
    stop=str(current_bar[JAW])
    choosen_line="jaw"
  else:
    raise ValueError("No indicator line selected")
  msg = f"Made Gator line stop."
  print_jsonl_message(msg,extra_dict={"stop":stop,"line":choosen_line},scope="fxmvstopgator")
  #Then move the stop
  fxmvstop(tradeid,stop,demo=demo)
  if loop_action:
    print("{\"message\":\"Loop action run the fxmvstopgator active\"}")
    sleep(60) # We will wait at least 60 seconds before running the loop action, we already changed the stop
    sleep(1)
    w(t,exit_on_timeframe=True)
    #recursive call
    fxmvstopgator(i,t,tradeid,lips=lips,teeth=teeth,jaw=jaw,demo=demo,loop_action=True,skip_trade_data_update=skip_trade_data_update)

def tide(instrument, timeframe, buysell):
  raise DeprecationWarning("tide is deprecated. ")
  #subprocess.run(['tide', instrument, timeframe, buysell])

def pds(instrument, timeframe,use_full=True):
  use_full_arg = '--full' if use_full else ''
  subprocess.run([PDSCLI_PROG_NAME, '-i', instrument, '-t', timeframe, use_full_arg], check=True)

def cds(instrument, timeframe, use_fresh=False,use_full=True):
  use_full_arg = '--full' if use_full else ''
  old_or_fresh = '-old' if not use_fresh else '--fresh'
  subprocess.run([CDSCLI_PROG_NAME, '-i', instrument, '-t', timeframe,use_full_arg, old_or_fresh], check=True)

def ads(instrument, timeframe, use_fresh=False,tc=True,pov=False):
  old_or_fresh = '-old' if not use_fresh else '--fresh'
  ads_cli_args = [ADSCLI_PROG_NAME, '-i', instrument, '-t', timeframe, old_or_fresh]
  if tc and not pov:
    ads_cli_args.append('-sf')
    ads_cli_args.append('tc')
  elif pov:
    ads_cli_args.append('-sf')
    ads_cli_args.append('cp')
  subprocess.run(ads_cli_args, check=True)

def ocds(instrument, timeframe,use_full=True):
  use_full_arg = '--full' if use_full else ''
  subprocess.run([JGTCLI_PROG_NAME, '-i', instrument, '-t', timeframe, use_full_arg, '-old'], check=True)

  
def ttf(instrument, timeframe,pn="ttf",use_fresh=False,use_full=True):
  use_full_arg = '--full' if use_full else ''
  use_fresh_arg = '-old' if not use_fresh else '--fresh'
  
  ttf_args = [TTFCLI_PROG_NAME, '-i', instrument, '-t', timeframe, use_full_arg, use_fresh_arg, '-pn', pn]
  print("TTF is being ran by jgtapp with args: ", ttf_args)
  subprocess.run(ttf_args, check=True)


def mlf(instrument, timeframe,pn="ttf",total_lagging_periods=5,use_fresh=False,use_full=True):
  use_full_arg = '--full' if use_full else ''
  use_fresh_arg = '-old' if not use_fresh else '--fresh'
  mlf_args = [MLFCLI_PROG_NAME, '-i', instrument, '-t', timeframe, use_full_arg, use_fresh_arg, '-pn', pn,'--total_lagging_periods',total_lagging_periods]
  subprocess.run(mlf_args, check=True)

  

def mx(instrument, timeframe, use_fresh=False):
  old_or_fresh = '-old' if not use_fresh else '--fresh'
  subprocess.run([MXCLI_PROG_NAME, '-i', instrument, '-t', timeframe, old_or_fresh], check=True)

def ttfmxwf(instrument, use_fresh=False):
  for t in ["M1", "W1", "D1", "H4"]:
    print(f"Processing {instrument} for timeframe {t}")
    print("  CDS....")
    cds(instrument, t, use_fresh)
    if t != "M1":
      print("  TTF....")
      ttf(instrument, t)
    if t != "M1" and t != "W1":
      print("  MX....")
      mx(instrument, t)
      
def ttfwf(instrument, use_fresh=False):
  
  _settings = jgtcommon.get_settings()
  #ttf2run
  if hasattr(_settings, 'ttf2run'):
    ttf2run=_settings.ttf2run
  else:
    from jgtml.mlconstants import TTF2RUN_DEFAULT
    ttf2run=TTF2RUN_DEFAULT
  for pn in ttf2run:
      
    for t in ["M1", "W1", "D1", "H4"]:
      print(f"Processing {instrument} for timeframe {t}")
      print("  CDS....")
      cds(instrument, t, use_fresh)
      if t != "M1":
        print("  TTF....")
        ttf(instrument, t,pn=pn)

def _add_common_arguments(parser,from_jgt_env=True,required_instrument=True,required_timeframe=True,fresh=True,fresh_from_settings=True,full_from_settings=False):
  parser=jgtcommon.add_instrument_standalone_argument(parser,from_jgt_env=from_jgt_env,required=required_instrument)
  parser=jgtcommon.add_timeframe_standalone_argument(parser,from_jgt_env=from_jgt_env,required=required_timeframe)
  parser=jgtcommon.add_use_fresh_argument(parser,load_from_settings=fresh_from_settings)
  parser=jgtcommon.add_use_full_argument(parser,load_from_settings=full_from_settings)
  parser=jgtcommon.add_verbose_argument(parser,load_from_settings=True)
  parser=jgtcommon.add_demo_flag_argument(parser,load_default_from_settings=True,from_jgt_env=from_jgt_env)
  
  return parser
def _add_ordering_arguments(parser,from_jgt_env=True):
  parser=jgtcommon.add_orderid_arguments(parser,from_jgt_env=from_jgt_env)
  return parser

def main():
  cli_help_description = "CLI equivalent of bash functions"
  parser = jgtcommon.new_parser(cli_help_description,"JGTApp Wrapper/runner - run various ","jgtapp",add_exiting_quietly_flag=True)#argparse.ArgumentParser(description=cli_help_description)
  subparsers = parser.add_subparsers(dest='command')
  
  #fxaddorder
  parser_fxaddorder = subparsers.add_parser('fxaddorder', help='Add an order',aliases=['add'])
  add_get_bash_autocomplete_argument(parser_fxaddorder)
  parser_fxaddorder.add_argument('-i','--instrument', help='Instrument')
  parser_fxaddorder.add_argument('-n','--lots', help='Lots')
  parser_fxaddorder.add_argument('-r','--rate', help='Rate')
  parser_fxaddorder.add_argument('-d','--buysell', help='Buy or Sell')
  parser_fxaddorder.add_argument('-x','--stop', help='Stop')
  parser_fxaddorder.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxaddorder.add_argument('--real', action='store_true', help='Use the real account',default=True)
  parser_fxaddorder.add_argument('--pips', action='store_true', help='Use pips')
  
  #fxrmorder
  parser_fxrmorder = subparsers.add_parser('fxrmorder', help='Remove an order',aliases=['rm'])
  parser_fxrmorder.add_argument('-id','--orderid', help='Order ID')
  parser_fxrmorder.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxrmorder.add_argument('--real', action='store_true', help='Use the real account',default=True)
  
  #entryvalidate
  parser_entryvalidate = subparsers.add_parser('entryvalidate', help='Remove an order if it became invalid (e.g. stop rate hit')
  parser_entryvalidate.add_argument('-id','--orderid', help='Order ID')
  parser_entryvalidate.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_entryvalidate.add_argument('--real', action='store_true', help='Use the real account',default=True)
  
  #fxrmtrade
  parser_fxrmtrade = subparsers.add_parser('fxrmtrade', help='Remove a trade',aliases=['rmtrade','close'])
  parser_fxrmtrade.add_argument('-tid','--tradeid', help='Trade ID')
  parser_fxrmtrade.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxrmtrade.add_argument('--real', action='store_true', help='Use the real account',default=True)
    
  #fxtr
  parser_fxtr = subparsers.add_parser('fxtr', help='Get trade details')
  parser_fxtr.add_argument('-tid','--tradeid', help='Trade ID')
  parser_fxtr.add_argument('-id','--orderid', help='Order ID')
  parser_fxtr.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxtr.add_argument('--real', action='store_true', help='Use the real account',default=True)
  parser_fxtr.add_argument('--nosave', action='store_true', help='Dont Save the trade details')
  
  #fxmvstop
  parser_fxmvstop = subparsers.add_parser('fxmvstop', help='Move stop',aliases=['mvstop','mv'])
  parser_fxmvstop.add_argument('-tid','--tradeid', help='Trade ID')
  parser_fxmvstop.add_argument('-x','--stop', help='Stop')
  parser_fxmvstop.add_argument('--pips', action='store_true', help='Use pips')
  parser_fxmvstop.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxmvstop.add_argument('--real', action='store_true', help='Use the real account',default=True)
  
  #ids
  parser_ids = subparsers.add_parser('ids', help='Refresh the IDS')
  parser_ids.add_argument('-i','--instrument', help='Instrument')
  parser_ids.add_argument('-t','--timeframe', help='Timeframe')
  parser_ids.add_argument('--full', action='store_true', help='Use the full data')
  parser_ids.add_argument('--fresh', action='store_true', help='Use the fresh data')
  
  #fxmvstopgator
  parser_fxmvstopgator = subparsers.add_parser('fxmvstopgator', help='Move stop using gator',aliases=['gator'])
  parser_fxmvstopgator.add_argument('-i','--instrument', help='Instrument',default="_",required=False)
  parser_fxmvstopgator.add_argument('-t','--timeframe', help='Timeframe')
  parser_fxmvstopgator.add_argument('-tid','--tradeid', help='Trade ID')
  parser_fxmvstopgator.add_argument('--lips', action='store_true', help='Use lips')
  parser_fxmvstopgator.add_argument('--teeth', action='store_true', help='Use teeth')
  parser_fxmvstopgator.add_argument('--jaw', action='store_true', help='Use jaw')
  parser_fxmvstopgator.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxmvstopgator.add_argument('--real', action='store_true', help='Use the real account',default=True)
  parser_fxmvstopgator.add_argument('-W','--loop_action', help='Loop action', action='store_true')
  
  #fxmvstopfdb
  
  parser_fxmvstopfdb = subparsers.add_parser('fxmvstopfdb', help='Move stop using fdb',epilog=fxmvstopfdb_epilog,aliases=['fdb'])
  parser_fxmvstopfdb.add_argument('-i','--instrument', help='Instrument',default="_",required=False)
  parser_fxmvstopfdb.add_argument('-t','--timeframe', help='Timeframe')
  parser_fxmvstopfdb.add_argument('-tid','--tradeid', help='Trade ID')
  parser_fxmvstopfdb.add_argument('--demo', action='store_true', help='Use the demo account')
  parser_fxmvstopfdb.add_argument('--real', action='store_true', help='Use the real account',default=True)
  #close the trade if the stop of fdbsignal is already hit
  parser_fxmvstopfdb.add_argument('--close', action='store_true', help='Close the trade if the stop of fdbsignal is already hit')
  parser_fxmvstopfdb.add_argument('--lips', action='store_true', help='Use lips (if no FDB signal is found, the lips will be used)')
  parser_fxmvstopfdb.add_argument('--teeth', action='store_true', help='Use teeth. If no FDB signal is found, the teeth will be used')
  parser_fxmvstopfdb.add_argument('--jaw', action='store_true', help='Use jaw (if no FDB signal is found, the jaw will be used)')
  

  parser_tidealligator = subparsers.add_parser('tide', help='Run the pto tidealligator')
  parser_tidealligator.add_argument('-i','--instrument', help='Instrument')
  parser_tidealligator.add_argument('-t','--timeframe', help='Timeframe')
  parser_tidealligator.add_argument('buysell', help='Buy or Sell')

  parser_prep_pds_01 = subparsers.add_parser('pds', help='Refresh the PDS full for an instrument and timeframe')
  parser_prep_pds_01.add_argument('-i','--instrument', help='Instrument')
  parser_prep_pds_01.add_argument('-t','--timeframe', help='Timeframe')
  parser_prep_pds_01.add_argument('--full', action='store_true', help='Use the full data')

  parser_prep_cds_05 = subparsers.add_parser('cds', help='Refresh the CDS')
  parser_prep_cds_05.add_argument('-i','--instrument', help='Instrument')
  parser_prep_cds_05.add_argument('-t','--timeframe', help='Timeframe')
  #--fresh flag to use the fresh data
  parser_prep_cds_05.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')
  parser_prep_cds_05.add_argument('--full', action='store_true', help='Use the full data')
  
  parser_prep_ads_06 = subparsers.add_parser('ads', help='Refresh the ADS charts')
  parser_prep_ads_06.add_argument('-i','--instrument', help='Instrument')
  parser_prep_ads_06.add_argument('-t','--timeframe', help='Timeframe')
  #--fresh flag to use the fresh data
  parser_prep_ads_06.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')
  #-pov, --save_figure_as_pov_name
  parser_prep_ads_06.add_argument('-pov','--save_figure_as_pov_name', action='store_true', help='Save the figure as pov name. Default is in ./charts/T.png')
  
  
  parser_prep_cds_06_old = subparsers.add_parser('ocds', help='Refresh the CDS from old PDS')
  parser_prep_cds_06_old.add_argument('-i','--instrument', help='Instrument')
  parser_prep_cds_06_old.add_argument('-t','--timeframe', help='Timeframe')
  parser_prep_cds_06_old.add_argument('--full', action='store_true', help='Use the full data')
  
  #tfw
  parser_tfw_cron = subparsers.add_parser('w', help='Refresh wait for timeframe')
  parser_tfw_cron.add_argument('-t','--timeframe', help='Timeframe')
  parser_tfw_cron.add_argument("-B", "--script-to-run", help="Script to run when the timeframe is reached. (.jgt/tfw.sh). ")
  parser_tfw_cron.add_argument("-X", "--exit", action="store_true", help="Exit the program when the timeframe is reached.")
  
  
  parser_prep_ttf_10 = subparsers.add_parser('ttf', help='Refresh the TTF for an instrument and timeframe')
  parser_prep_ttf_10.add_argument('-i','--instrument', help='Instrument symbol')
  parser_prep_ttf_10.add_argument('-t','--timeframe', help='Timeframe')
  parser_prep_ttf_10.add_argument('-pn','--patternname', help='Pattern Name')
  parser_prep_ttf_10.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')
  parser_prep_ttf_10.add_argument('--full', action='store_true', help='Use the full data')


  
  parser_prep_mlf_22 = subparsers.add_parser('mlf', help='Refresh the MLF for an instrument and timeframe')
  parser_prep_mlf_22.add_argument('-i','--instrument', help='Instrument symbol')
  parser_prep_mlf_22.add_argument('-t','--timeframe', help='Timeframe')
  parser_prep_mlf_22.add_argument('-pn','--patternname', help='Pattern Name')
  parser_prep_mlf_22.add_argument('-tlp','--total_lagging_periods', help='Total Lagging Periods')
  parser_prep_mlf_22.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')
  parser_prep_mlf_22.add_argument('--full', action='store_true', help='Use the full data')
  
  
  #ttfmxwf
  parser_post_ttfmxwf_14 = subparsers.add_parser('ttfmxwf', help='Refresh the TTF, MX and CDS for an instrument')
  parser_post_ttfmxwf_14.add_argument('-i','--instrument', help='Instrument symbol')
  parser_post_ttfmxwf_14.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')

  parser_post_mx_15 = subparsers.add_parser('mx', help='Refresh the MX (using the TTF) for an instrument and timeframe')
  parser_post_mx_15.add_argument('-i','--instrument', help='Instrument symbol')
  parser_post_mx_15.add_argument('-t','--timeframe', help='Timeframe')

  parser_wf_ttf_prep_19 = subparsers.add_parser('ttfwf', help='Refresh TTF preparation for an instrument')
  parser_wf_ttf_prep_19.add_argument('-i','--instrument', help='Instrument symbol')
  parser_wf_ttf_prep_19.add_argument('-new','--fresh', action='store_true', help='Use the fresh data')
  parser_wf_ttf_prep_19.add_argument('--full', action='store_true', help='Use the full data')

  #An --autocomplete for bash
  # This argument --autocomplete is used to generate the bash autocomplete script
  ## We should not see it in the help
  add_get_bash_autocomplete_argument(parser)
  
  
  args = parser.parse_args()
  
  if args.get_bash_autocomplete:
      command_list = "fxaddorder fxrmorder entryalidate fxrmtrade fxtr fxmvstop ids fxmvstopgator fxmvstopfdb"
      array_commands = command_list.split(" ")
      #print(args.get_bash_autocomplete)
      if args.get_bash_autocomplete and args.get_bash_autocomplete in array_commands:
        current_command = args.get_bash_autocomplete
        print(current_command)
        #get subparser of the current command
        subparser = subparsers.choices[current_command]
        #printits help 
        subparser.print_help()
      else:
        print(command_list)#Generating bash autocomplete script...")
      
      #print(args.get_bash_autocomplete)
      
     
      exit()
      
  #if no arguments are passed, print help
  if not vars(args).get('command'):
    parser.print_help()
    parser.exit()
  
  
  
  if args.command == 'tide':
    tide(args.instrument, args.timeframe, args.buysell)
  elif args.command == 'fxaddorder' or args.command == 'add':
    fxaddorder(args.instrument, args.lots, args.rate, args.buysell, args.stop, args.demo,args.pips)
  elif args.command == 'fxrmorder' or args.command == 'rm':
    fxrmorder(args.orderid, args.demo)
  elif args.command == 'entryvalidate': #@STCIssue Does that needs to Get the instrument from the OrderID ?
    entryvalidate(args.orderid, args.demo)
  elif args.command == 'fxrmtrade' or args.command == 'rmtrade' or args.command == 'close':
    fxrmtrade(args.tradeid, args.demo)
  elif args.command == 'fxtr':
    fxtr(args.tradeid,args.orderid,args.demo,not args.nosave)
  elif args.command  in ['fxmvstop','mvstop','mv']:
    fxmvstop(args.tradeid, args.stop, args.pips, args.demo)
  elif args.command == 'ids':
    ids(args.instrument, args.timeframe,args.full,args.fresh)
  elif args.command == 'fxmvstopgator' or args.command == 'gator':
    lips_value = True if not args.lips and not args.teeth and not args.jaw else False
    fxmvstopgator(args.instrument, args.timeframe, args.tradeid, lips_value,args.teeth,args.jaw,args.demo,loop_action=args.loop_action)
  elif args.command == 'fxmvstopfdb' or args.command == 'fdb':
    fxmvstopfdb(args.instrument, args.timeframe, args.tradeid, args.demo,args.close,args.lips,args.teeth,args.jaw)
  elif args.command == 'w':
    w(args.timeframe,args.script_to_run,args.exit)
  elif args.command == 'pds':
    pds(args.instrument, args.timeframe,)
  elif args.command == 'cds':
    cds(args.instrument, args.timeframe, args.fresh,args.full)
  elif args.command == 'ads':
    use_pov_name = args.save_figure_as_pov_name if args.save_figure_as_pov_name else False
    tc_flag = False if use_pov_name else True
    
    ads(args.instrument, args.timeframe, args.fresh,pov=use_pov_name,tc=tc_flag)
  elif args.command == 'ocds':
    ocds(args.instrument, args.timeframe)
  elif args.command == 'ttf':
    ttf(args.instrument, args.timeframe,args.patternname,args.columns_list_from_higher_tf,args.fresh,args.full)
  elif args.command == 'mlf':
    mlf(args.instrument, args.timeframe,args.patternname,args.total_lagging_periods,args.fresh,args.full)
  elif args.command == 'ttfmxwf':
    ttfmxwf(args.instrument, args.fresh)
  elif args.command == 'mx':
    mx(args.instrument, args.timeframe)
  elif args.command == 'ttfwf':
    ttfwf(args.instrument, args.fresh,args.full)

def add_get_bash_autocomplete_argument(parser):
    parser.add_argument('--get-bash-autocomplete','--get-autocomplete','--autocomplete',help=argparse.SUPPRESS,nargs='?',const=True,action='store',dest='get_bash_autocomplete')

if __name__ == "__main__":
  main()
