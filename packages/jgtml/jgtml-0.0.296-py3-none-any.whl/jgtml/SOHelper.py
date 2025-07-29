import json
import pandas as pd
import numpy as np

def get_last_two_bars_OLD(df:pd.DataFrame)->{dict,dict}:
  current_bar = df.iloc[-1].copy()
  last_bar_completed = df.iloc[-2:].copy()
  completed_bars_dict = last_bar_completed.to_dict()
  current_bar_dict = current_bar.to_dict()
  return completed_bars_dict,current_bar_dict
  
def get_last_two_bars(df:pd.DataFrame):
  completed_bars=get_bar_at_index(df,-2)
  current_bar=get_bar_at_index(df,-1)
  return completed_bars,current_bar
  

def get_bar_at_index(df:pd.DataFrame,idx=-1,):
  tbar = df.iloc[idx]
  tbar_json_str = tbar.to_json()
  return json.loads(tbar_json_str)

def get_bar_at_index_v2(df:pd.DataFrame,idx=-1,format='%Y-%m-%d %H:%M:%S'):
  if 'Date' in df.columns:
    df2 = df.copy()
  else:
      df2 = df.copy().reset_index()
  df2['Date'] = pd.to_datetime(df2['Date'], format=format)
  tbar = df2.iloc[idx]
  tbar_json_str = tbar.to_json()
  return json.loads(tbar_json_str)