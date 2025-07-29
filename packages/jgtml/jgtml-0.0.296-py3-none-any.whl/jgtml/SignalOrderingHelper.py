

import datetime
from typing import Callable, Optional
import tlid
from jgtutils import iprops
from jgtutils.jgtconstants import \
  HIGH,LOW,FDB,ASKHIGH,ASKLOW,BIDHIGH,BIDLOW,JAW,TEETH,LIPS,BJAW,BTEETH,BLIPS,DATE
import pandas as pd

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

from jgtutils.iprops import \
  get_pips


def calculate_entry_risk(i, bs, entry_rate, stop_rate, position_size, tick_shift=1, rounding_add=2, t=None,quiet=True,verbose_level=0):
    pips = get_pips(i)
    tick_size = pips / 10

    decimal_places = len(str(pips).split('.')[1]) + rounding_add if '.' in str(pips) else 1
    if bs == "B":
        entry_rate += tick_size * tick_shift
        stop_rate -= tick_size * tick_shift
    elif bs == "S":
        entry_rate -= tick_size * tick_shift
        stop_rate += tick_size * tick_shift

    entry_rate = round(entry_rate, decimal_places)
    stop_rate = round(stop_rate, decimal_places)

    risk_per_unit = abs(entry_rate - stop_rate)
    total_risk = risk_per_unit * position_size
    risk_in_pips = risk_per_unit / pips
    if verbose_level>2:print(f"pips:{pips}, risk/u:{risk_per_unit}, risk in pips:{risk_in_pips} for {i}")
    
    return total_risk,risk_per_unit, round(risk_in_pips,2)

def get_entry_stop_rate_ticked(i,bs,entry_rate,stop_rate,tick_shift=1,rouding_add = 2,t=None):
  pips=get_pips(i)
  tick_size=pips/10
  
  decimal_places = len(str(pips).split('.')[1]) + rouding_add if '.' in str(pips) else 1
  if bs=="B":
    entry_rate+=tick_size*tick_shift
    stop_rate-=tick_size*tick_shift
  else:
    if bs=="S":
      entry_rate-=tick_size*tick_shift
      stop_rate+=tick_size*tick_shift
  entry_rate = round(entry_rate, decimal_places)
  stop_rate = round(stop_rate, decimal_places)
  return entry_rate,stop_rate
  

def valid_gator(last_bar_completed,current_bar,bs):
  last_bar_mouth_is_open_and_price_is_out = is_mouth_open_and_bar_out_of_it(last_bar_completed,bs)
  cur_bar_mouth_is_open_and_price_is_out = is_mouth_open_and_bar_out_of_it(current_bar,bs)
  return \
    last_bar_mouth_is_open_and_price_is_out \
      and \
        cur_bar_mouth_is_open_and_price_is_out



def is_mouth_open_and_bar_out_of_it(bar,bs)->bool:
  is_bar_out_of_mouth_result = is_bar_out_of_mouth(bar,bs)
  is_mouth_open_result = is_mouth_open(bar,bs)
  return is_bar_out_of_mouth_result and is_mouth_open_result


def is_bar_out_of_mouth(bar,bs)->bool:
  mouth_open_reverse = is_mouth_open(bar,"B") if bs=="S" else is_mouth_open(bar,"S")
  if bs=="B":
    return bar[HIGH] < bar[LIPS] \
      and \
        not mouth_open_reverse
  if bs=="S":
    return bar[LOW] > bar[LIPS] \
      and \
        not mouth_open_reverse
  
def is_mouth_open(bar,bs)->bool:
  if bs=="B":
    return bar[LIPS] < bar[TEETH] and bar[TEETH] < bar[JAW] and bar[LIPS] < bar[JAW]
  if bs=="S":
    return bar[LIPS] > bar[TEETH] and bar[TEETH] > bar[JAW] and bar[LIPS] > bar[JAW]
  return False
  
def is_big_mouth_open(bar,bs)->bool:
  if bs=="B":
    return  bar[BLIPS] < bar[BTEETH] and bar[BTEETH] < bar[BJAW] and  bar[BLIPS] < bar[BJAW]
  if bs=="S":
    return  bar[BLIPS] > bar[BTEETH] and bar[BTEETH] > bar[BJAW]and  bar[BLIPS] > bar[BJAW]

def is_fdbsignal_crossed_t(bar,bs,tcol):
  if bs=="B":
    return bar[HIGH] < bar[tcol]
  if bs=="S":
    return bar[LOW] > bar[tcol]

def is_fdbsignal_in_big_mouth(bar,bs):
  return is_fdbsignal_crossed_t(bar,bs,BLIPS)
  
def is_fdbsignal_in_big_mouth_teeth(bar,bs):
  return is_fdbsignal_crossed_t(bar,bs,BLIPS)


def create_fdb_entry_order(i,signal_bar,current_bar,lots=1,tick_shift=2,quiet=True,valid_gator_mouth_open_in_mouth=False,validate_signal_out_of_mouth=True,t=None,validation_timestamp=None,verbose_level=0,demo_flag=True):
  #,_extra_scripting_output_callback: Optional[Callable[[str,str,pd.Series,pd.Series]]] = None):
  had_valid_signal=False
  is_signal_broken=True
  msg = ""
   
  # signal_bar=signal_bar.to_dict()
  # current_bar=current_bar.to_dict()
  tlid_id = tlid.get_seconds()
  
  fdb_sig = signal_bar[FDB]
  if fdb_sig==1:
    bs_string="Buy"
    askhigh = signal_bar[ASKHIGH]
    bidlow = signal_bar[BIDLOW]
    
    bs="B"
    entry_rate,stop_rate=get_entry_stop_rate_ticked(i,bs,askhigh,bidlow,tick_shift=tick_shift,t=t)

    had_valid_signal=True
    #check of the current_bar make the signal invalid by being out of range (means the entry_rate is already hit or it passed the stop_rate (making it invalid))
    cur_askhigh = current_bar[ASKHIGH]
    cur_bidlow = current_bar[BIDLOW]
    
    if cur_askhigh<=entry_rate and cur_bidlow>=stop_rate :
      is_signal_broken=False
    
      
    if  verbose_level>2:
      msg += f"cur_askhigh:{cur_askhigh} entry_rate:{entry_rate} cur_bidlow:{cur_bidlow} stop_rate:{stop_rate}\n"
      print(msg)
  
  
  if fdb_sig==-1:
    bs_string="Sell"
    #print(f"# Sell Signal on {i}")
    
    bidlow = signal_bar[BIDLOW]
    askhigh = signal_bar[ASKHIGH]
    
    entry_rate,stop_rate=get_entry_stop_rate_ticked(i,"S",bidlow,askhigh,tick_shift=tick_shift,t=t)

    bs="S"
    had_valid_signal=True
    
    cur_bidlow = current_bar[BIDLOW]
    cur_askhigh = current_bar[ASKHIGH]
    
    if cur_bidlow>=entry_rate and cur_askhigh<=stop_rate:
      is_signal_broken=False
    
    if verbose_level>2:
      msg += f"cur_bidlow:{cur_bidlow} entry_rate:{entry_rate} cur_askhigh:{cur_askhigh} stop_rate:{stop_rate}\n"
      #print(msg)
  
  if  is_signal_broken and had_valid_signal:
    if verbose_level>0:
      msg += f"## Signal Stop Broken the {bs_string} {i} {t} "
      #print(msg)
    return None,msg
  
  if not had_valid_signal:
    return None,msg
  
  is_valid_gator = valid_gator(signal_bar,current_bar,bs)
  if valid_gator_mouth_open_in_mouth \
    and \
      not is_valid_gator:
    if verbose_level>0:
      msg += f"## Invalid Gator {i} {t} valid_gator_mouth_open_in_mouth"
      #print(msg)
    return None,msg
  
  if validate_signal_out_of_mouth \
    and \
      not is_bar_out_of_mouth(current_bar,bs):
    if verbose_level>0:
      msg += f"## Invalid Gator {i} {t} not valid_sig_out_mouth"
      #print(msg)
    return None,msg
  #Get 'Date' or index of the signal bar
  
  validation_timestamp_str=validation_timestamp.strftime("%Y-%m-%d %H:%M") if validation_timestamp is not None else ""
  
  total_risk,risk_per_unit, risk_in_pips=calculate_entry_risk(i, bs, entry_rate, stop_rate, lots, tick_shift=tick_shift, t=t,quiet=quiet,verbose_level=verbose_level)
  
  #extra_scripting_output_str=_extra_scripting_output_callback(i,t,signal_bar,current_bar) if _extra_scripting_output_callback is not None else None
  extra_scripting_output_str="##__"
  
  output_script = generate_entry_order_script(lots, entry_rate, stop_rate, i, bs,tlid_id=tlid_id,t=t,validation_timestamp_str=validation_timestamp_str,demo_flag=demo_flag,total_risk=total_risk,risk_per_unit=risk_per_unit, risk_in_pips=risk_in_pips,extra_scripting_output=extra_scripting_output_str)
  o = build_order_result_object(lots, entry_rate, stop_rate, bs, tlid_id, output_script,i,t,total_risk=total_risk,risk_per_unit=risk_per_unit, risk_in_pips=risk_in_pips)
  msg=""
  return o,msg

def build_order_result_object(lots, entry_rate, stop_rate, buysell, tlid_id, output_script,i,t,total_risk=None,risk_per_unit=None, risk_in_pips=None):
    o={}
    o["sh"]=output_script
    o["entry"]=entry_rate
    o["stop"]=stop_rate
    o["bs"]=buysell
    o["lots"]=lots
    o["tlid_id"]=tlid_id
    o["i"]=i
    o["t"]=t
    o["total_risk"]=total_risk
    o["unit_risk"]=risk_per_unit
    o["pips_risk"]=risk_in_pips
    return o


def generate_entry_order_script(lots, entry_rate, stop_rate, instrument, buysell,tlid_id=None,t=None,validation_timestamp_str="",demo_flag=True,total_risk=None,risk_per_unit=None, risk_in_pips=None,extra_scripting_output=None):
    demo_arg="demo" if demo_flag else "real"
    demo_arg_opp="#demo_arg=\"--real\""  if demo_flag else "#demo_arg=\"--demo\""
    timeframe=t if t is not None else "_"
    #make a timestamp of now in UTC
    now_utc_string=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    bs_string="Buy" if buysell=="B" else "Sell"
    if tlid_id is None:
      tlid_id = tlid.get_seconds()
    # total_risk={total_risk}
    #risk_per_unit={risk_per_unit} #/per pip
    extra_scripting_output_str = extra_scripting_output if extra_scripting_output is not None else ""
    output_script=f"""
```sh

### --- COPY FROM HERE --- 
demo_arg="--{demo_arg}" {demo_arg_opp}
# FDB {bs_string} Entry {instrument} {timeframe} - bts/now:{validation_timestamp_str}/{now_utc_string}
risk_in_pips={risk_in_pips}
instrument="{instrument}";timeframe="{timeframe}";bs="{buysell}"
tlid_id={tlid_id};lots={lots}
entry_rate={entry_rate};stop_rate={stop_rate}
jgtnewsession $tlid_id $instrument $timeframe $entry_rate $stop_rate $bs $lots $demo_arg
{extra_scripting_output_str}
### ---- COPY TO HERE ---
```"""
    
    return output_script

def generate_entry_order_script_pto1(lots, entry_rate, stop_rate, instrument, buysell):
    output_script=f"""
```sh
entry_rate={entry_rate};stop_rate={stop_rate};instrument={instrument};buysell={buysell};lots={lots}
s=CreateEntryOrderPtoAddStop.py
python $s $real_fx_cli_base_args -lots $lots -r $entry_rate -d $buysell -i $instrument -stop $stop_rate  | tee __output.txt  && \
OrderID=$(cat __output.txt| grep -o 'OrderID=[0-9]*' | cut -d '=' -f2) && \
echo "OrderID: $OrderID"
```
"""
    
    return output_script


def get_iprop(i):
  return iprops.get_iprop(i)