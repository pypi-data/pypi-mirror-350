import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
pd.options.mode.copy_on_write = True

import anhelper

from jgtutils.jgtconstants import ZONE_INT,ZONE_BUY_ID,ZONE_SELL_ID,ZONE_NEUTRAL_ID,ZONE_BUY_STR,ZONE_SELL_STR,ZONE_NEUTRAL_STR
from jgtutils.colconverthelper import zone_str_to_id,get_zone_features_column_list_by_timeframe

from mlconstants import ZONE_DEFAULT_COLNAME
  
def column_zone_str_in_dataframe_to_id(df:pd.DataFrame,t:str,inplace=False,zone_colname=""):
    """
    Convert the ZONE columns from str to id in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The dataframe to convert the ZONE columns from str to id.
    t (str): The timeframe to convert the ZONE columns from str to id.
    inplace (bool): If True, the conversion is done in place. If False, a copy of the dataframe is returned with the conversion done.
    zone_colname (str): The name of the ZONE column to use. If not provided, the default ZCOL is used. (Planning to use ZONE_SIGNAL)
    
    Returns:
    pd.DataFrame: The dataframe with the ZONE columns converted from str to id.
    
    """
    if zone_colname=="":
        zone_colname=ZONE_DEFAULT_COLNAME
        
    if not inplace:
        df = df.copy()
    zcol_features_columns_list = get_zone_features_column_list_by_timeframe(t,zone_colname)
    for col_name in zcol_features_columns_list:
        df[col_name] = df[col_name].apply(lambda x: int(zone_str_to_id(x)))
          #zonecolor_str_to_id)
    return df

def _zoneint_add_lagging_feature(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True,zone_colname=""):
    if zone_colname=="":
        zone_colname=ZONE_DEFAULT_COLNAME
        
    if not inplace:
        df = df.copy()
    columns_to_add_lags_to = get_zone_features_column_list_by_timeframe(t,zone_colname)
    #columns_to_add_lags_to.append(zone_colname) #We want a lag for the current TF
    anhelper.add_lagging_columns(df, columns_to_add_lags_to, lag_period, total_lagging_periods, out_lag_midfix_str)
    for col in columns_to_add_lags_to:#@STCIssue Isn't that done already ???  Or it thinks they are Double !!!!
        for j in range(1, total_lagging_periods + 1):
            df[f'{col}{out_lag_midfix_str}{j}']=df[f'{col}{out_lag_midfix_str}{j}'].astype(int)
    return df
    

def wf_mk_zone_ready_dataset__240708(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True,zone_colname=""):
    if zone_colname=="":
        zone_colname=ZONE_DEFAULT_COLNAME
        
    if not inplace:
        df = df.copy()
    #column_zone_str_in_dataframe_to_id(df,t,inplace=True,zone_colname=zone_colname)
    _zoneint_add_lagging_feature(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,out_lag_midfix_str=out_lag_midfix_str,inplace=True,zone_colname=zone_colname)
    return df