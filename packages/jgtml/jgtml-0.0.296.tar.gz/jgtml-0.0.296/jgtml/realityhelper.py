import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtutils.jgtconstants import VOLUME,FDB_TARGET as TARGET
from mlconstants import ZONE_DEFAULT_COLNAME,MFI_DEFAULT_COLNAME

#from jgtpy import mfihelper,JGTCDSSvc as cdssvc
import anhelper as anh
import mxhelper
import mxconstants
import jtc
import pandas as pd


#@STCGoal We Have TTF Data with Lags for the pattern 'ttf_mfis_ao_2407a'
#@STCIssue How are created the TTF ?  How to create them with the lags and smaller Datasets (we dont need full)?

import ptottf 
#from jgtml import anhelper

from mfihelper2 import column_mfi_str_in_dataframe_to_id as _convert_mfi_columns_from_str_to_id

from zonehelper import wf_mk_zone_ready_dataset__240708 as _prep_zone_features_in_dataframe
#column_zone_str_in_dataframe_to_id as convert_zone_columns_from_str_to_id

from mxhelper import _add_lag_features_to_dataframe as _add_mfi_lagging_feature_to_ttfdf



def _load_ttf_data(i, t, use_full,force_refresh=False,quiet=True):
  if force_refresh:
    try:
      print("RH::loaddata::Upgrading/Refreshing the Depending Data before creating the TTF")
      ptottf._upgrade_ttf_depending_data(i, t, use_full=use_full, use_fresh=True,quiet=quiet)
      use_fresh=False
      #ptottf._upgrade_ttf_depending_data(i,t,use_full=use_full,use_fresh=True,quiet=quiet)
      ptottf.create_ttf_csv(i,t,use_full=use_full,use_fresh=use_fresh,quiet=quiet)
      force_refresh=False # We don't want to force refresh the next time
    except:
      print("ERROR::Failed to upgrade TTF depending data")
  return ptottf.read_ttf_csv(i, t, use_full=use_full,force_refresh=force_refresh)


#@STCIssue This should be Moved to mfihelper2.py
def __prep_mfi_2407a_features_in_dataframe(t, lag_period, total_lagging_periods, dropna, columns_to_keep, columns_to_drop, df):
    #df=_convert_mfi_columns_from_str_to_id(df,t, inplace=True)
  #add lags
    df=_add_mfi_lagging_feature_to_ttfdf(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,inplace=True)
    if dropna:
      df.dropna(inplace=True)
    if columns_to_keep:
      df=df[columns_to_keep]
    if columns_to_drop:
      for col in columns_to_drop:
        if col in df.columns:
          df.drop(columns=[col],inplace=True)
    return df


def _pto_get_dataset__with_mfi_ao__2407060929(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None,force_refresh=False,quiet=True):
  #Read Data
  df=_load_ttf_data(i, t, use_full,force_refresh=force_refresh,quiet=quiet)
  #Convert the MFI columns from str to id before we add lags
  df = __prep_mfi_2407a_features_in_dataframe(t, lag_period, total_lagging_periods, dropna, columns_to_keep, columns_to_drop, df)
    #df.drop(columns=columns_to_drop,inplace=True)
  #columns_to_add_lags_to = mxhelper.get_mfi_features_column_list_by_timeframe(t)
  #ttfdf=anhelper.add_lagging_columns(ttfdf, columns_to_add_lags_to)
  return df

def get_mlf_basedir(use_full,ns="mlf"):
    if use_full:
        bd=os.getenv("JGTPY_DATA_FULL")
        if bd is None:
            raise Exception("JGTPY_DATA_FULL environment variable is not set.")
    else:
        bd=os.getenv("JGTPY_DATA")
        if bd is None:
            raise Exception("JGTPY_DATA environment variable is not set.")
    fulldir=os.path.join(bd,ns)
    #mkdir -p fulldir
    os.makedirs(fulldir, exist_ok=True)
    return fulldir

def get_mlf_outfile_fullpath(i,t,use_full,suffix="",ns="mlf"):
    save_basedir=get_mlf_basedir(use_full,ns)
    ifn=i.replace("/","-")
    output_filename = f"{ifn}_{t}_{suffix}.csv"
    return os.path.join(save_basedir,output_filename.replace("__","_"))
  
def create_pattern_dataset__ttf_mfis_ao_2407a_pto_get_dataset_we_need_in_here__2407060929(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None,force_refresh=False,quiet=True):
  print("INFO::Requires experimentation with training, testing prediction to select from this what we need in reality to make the model work and predict reality of a signal.")
  df=_pto_get_dataset__with_mfi_ao__2407060929(i,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,dropna=dropna, use_full=use_full,columns_to_keep=columns_to_keep,columns_to_drop=columns_to_drop,force_refresh=force_refresh,quiet=quiet)
  output_filename=get_mlf_outfile_fullpath(i,t,use_full,"mfiao")
  try:
    df.to_csv(output_filename, index=True)
    print("INFO::MLF Saved to : ", output_filename)
  except:
    print("ERROR::Failed to save MLF to : ", output_filename)
  return df


def _read_adequate_pattern_dataset(i,t,use_full,pn,quiet=True,force_refresh=False):
  #@STCGoal Read ttf pattern
  from ptottf import read_ttf_csv
  df=read_ttf_csv(i, t, use_full=use_full,pn=pn,force_refresh=force_refresh)
  if not quiet:
    print(df.columns)
  return df
  #raise Exception("Not Implemented Yet::",patternname)

from mldatahelper import write_mlf_pattern_lagging_columns_list,read_patternname_columns_list
import mldatahelper as mldh
import anhelper

from mldatahelper import _get_lagging_columns_list

def generate_mlf_feature_pattern(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None,drop_bid_ask=False,force_refresh=False,quiet=True,pn="ttf",out_lag_midfix_str='_lag_',just_keep_lagging_columns=False,save_to_csv=True,args=None):
  #@STCGoal Pattern Name -> We have the Columns list serialized
  columns_list_from_higher_tf = mldh.pndata__read_new_pattern_columns_list_with_htf(t,pn,args=args)
  if not quiet:
    print("INFO::Columns List from Higher TF to prep laggings using MLF:",columns_list_from_higher_tf) #@STCGoal We Know which columns were in the TTF Pattern when created.
  #print("-------------------------------------------------","Not Implemented Yet::",patternname)
  
  
  df:pd.DataFrame=_read_adequate_pattern_dataset(i,t,use_full,pn,force_refresh=force_refresh)
  
  df=__clean_dataframe(df, columns_to_keep, columns_to_drop, drop_bid_ask,dropna)
  
  df=anhelper.add_lagging_columns(df, columns_list_from_higher_tf, lag_period, total_lagging_periods, out_lag_midfix_str)
  
  lagging_columns=mldh._get_lagging_columns_list(columns_list_from_higher_tf, lag_period, total_lagging_periods, out_lag_midfix_str)
  
  fixed_columns_to_keep=columns_list_from_higher_tf+lagging_columns
  #write_patternname_columns_list
  if just_keep_lagging_columns:
    df=df[fixed_columns_to_keep]
  
  #print(df.columns)
  if save_to_csv:      
    write_mlf_pattern_lagging_columns_list(i, t, use_full, pn, fixed_columns_to_keep)
    #save the mlf df to_csv
    output_filename=get_mlf_outfile_fullpath(i,t,use_full,pn)
    df.to_csv(output_filename, index=True)
    print("INFO::MLF Saved to : ", output_filename) 

  
  return df



def get_mfis_ao_zone_2407b_feature(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None,drop_bid_ask=False,force_refresh=False,quiet=True,zone_colname="",mfi_colname="",patternname="ttf"):
  print("WARN:::::: patternname is not IMPLEMENTED in MLF Now:",patternname)
  if zone_colname=="":
    zone_colname=ZONE_DEFAULT_COLNAME
  if mfi_colname=="":
    mfi_colname=MFI_DEFAULT_COLNAME
    
  df=_pto_get_dataset__with_mfi_ao__2407060929(i,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,dropna=dropna, use_full=use_full,columns_to_keep=columns_to_keep,columns_to_drop=columns_to_drop,force_refresh=force_refresh,quiet=quiet)
  
  df=_prep_zone_features_in_dataframe(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,inplace=True,zone_colname=zone_colname)
  
  __clean_dataframe(df, columns_to_keep, columns_to_drop, drop_bid_ask,dropna)
  
  output_filename=get_mlf_outfile_fullpath(i,t,use_full)
  try:
    df.to_csv(output_filename, index=True)
    print("INFO::MLF Saved to : ", output_filename)
  except:
    print("ERROR::Failed to save MLF to : ", output_filename)
  return df

from jgtutils.jgtconstants import BIDOPEN,BIDHIGH,BIDLOW,BIDCLOSE,ASKOPEN,ASKHIGH,ASKLOW,ASKCLOSE
def __clean_dataframe(df:pd.DataFrame, columns_to_keep=None, columns_to_drop=None, drop_bid_ask=False,dropna=True )->pd.DataFrame:
    """
    Common cleanup for the dataframe we are creating with various patterns
    
    """
    if dropna:
      df.dropna(inplace=True)
    if columns_to_keep:
      for col_name in columns_to_keep:
        if col_name not in df.columns:
          columns_to_keep.remove(col_name)
    if columns_to_drop:
      for col in columns_to_drop:
        if col in df.columns:
          df.drop(columns=[col],inplace=True)
    if drop_bid_ask:
      bid_ask_columns = [BIDOPEN,BIDHIGH,BIDLOW,BIDCLOSE,ASKOPEN,ASKHIGH,ASKLOW,ASKCLOSE]
      for col in bid_ask_columns:
        if col in df.columns:
          df.drop(columns=[col],inplace=True)
    return df
  