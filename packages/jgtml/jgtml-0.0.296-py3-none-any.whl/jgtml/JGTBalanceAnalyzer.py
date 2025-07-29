

import pandas as pd
# Use jgtconstants column names from jgtutils
from jgtutils.jgtconstants import LOW,HIGH,FDBB,FDBS,BJAW,BLIPS,BTEETH,JAW,TEETH,LIPS,FDB_TARGET,VECTOR_AO_FDBS_COUNT,VECTOR_AO_FDBB_COUNT,VECTOR_AO_FDB_COUNT,TJAW,TLIPS,TTEETH


def get_alligator_column_names_from_ctx_name(ctx_name):
    if ctx_name=="ripple" or ctx_name=="normal":
        cteeth_colname = TEETH
        clips_colname = LIPS
        cjaw_colname = JAW

    if ctx_name=="tide":
        cteeth_colname = TTEETH
        clips_colname = TLIPS
        cjaw_colname = TJAW


    if ctx_name=="big":
        cteeth_colname = BTEETH
        clips_colname = BLIPS
        cjaw_colname = BJAW
    return cteeth_colname,clips_colname,cjaw_colname





def generate_column_names_for_direction(ctx_name,direction)->list[str]:
  
    out_sig_is_in_ctx_teeth_sum_colname = f"{direction}_sig_is_in_{ctx_name}_teeth_sum"
    out_sig_ctx_mouth_is_open_and_signal_is_in_ctx_lips_sum_colname = f"{direction}_sig_{ctx_name}_mouth_is_open_and_in_{ctx_name}_lips"
    out_sig_ctx_mouth_is_open_and_signal_is_in_ctx_teeth_sum_colname = f"{direction}_sig_{ctx_name}_mouth_is_open_and_in_{ctx_name}_teeth_sum"
    out_sig_normal_mouth_is_open_sum_colname = "sig_normal_mouth_is_open"

    
    return {
        "sig_is_in_ctx_teeth_sum": out_sig_is_in_ctx_teeth_sum_colname,
        "sig_ctx_mouth_is_open_and_in_ctx_lips": out_sig_ctx_mouth_is_open_and_signal_is_in_ctx_lips_sum_colname,
        "sig_ctx_mouth_is_open_and_in_ctx_teeth_sum": out_sig_ctx_mouth_is_open_and_signal_is_in_ctx_teeth_sum_colname,
        "sig_normal_mouth_is_open_sum": out_sig_normal_mouth_is_open_sum_colname
    }



# Base filtering
def _filter_sig_is_out_of_normal_mouth_sell(dfsrc):
    df_sig_is_out_of_normal_mouth = dfsrc[dfsrc[LOW] > dfsrc[LIPS]].copy()
    df_sig_is_out_of_normal_mouth = df_sig_is_out_of_normal_mouth[df_sig_is_out_of_normal_mouth[LOW] > df_sig_is_out_of_normal_mouth[TEETH]]
    return df_sig_is_out_of_normal_mouth

def _filter_sig_normal_mouth_is_open_sell(dfsrc):
    df_sig_normal_mouth_is_open = dfsrc[dfsrc[JAW] < dfsrc[TEETH]].copy()
    df_sig_normal_mouth_is_open = df_sig_normal_mouth_is_open[df_sig_normal_mouth_is_open[TEETH] < df_sig_normal_mouth_is_open[LIPS]]
    df_sig_normal_mouth_is_open = df_sig_normal_mouth_is_open[df_sig_normal_mouth_is_open[JAW] < df_sig_normal_mouth_is_open[LIPS]]
    return df_sig_normal_mouth_is_open

def _filter_sig_is_out_of_normal_mouth_buy(dfsrc):
    df_sig_is_out_of_normal_mouth = dfsrc[dfsrc[HIGH] < dfsrc[LIPS]].copy()
    df_sig_is_out_of_normal_mouth = df_sig_is_out_of_normal_mouth[df_sig_is_out_of_normal_mouth[HIGH] < df_sig_is_out_of_normal_mouth[TEETH]]
    return df_sig_is_out_of_normal_mouth

def _filter_sig_normal_mouth_is_open_buy(dfsrc):
    df_sig_normal_mouth_is_open = dfsrc[dfsrc[JAW] > dfsrc[TEETH]].copy()
    df_sig_normal_mouth_is_open = df_sig_normal_mouth_is_open[df_sig_normal_mouth_is_open[TEETH] > df_sig_normal_mouth_is_open[LIPS]]
    df_sig_normal_mouth_is_open = df_sig_normal_mouth_is_open[df_sig_normal_mouth_is_open[JAW] > df_sig_normal_mouth_is_open[LIPS]]
    return df_sig_normal_mouth_is_open



def filter_sig_is_out_of_normal_mouth(dfsrc,bs,ctx_name):
  teval_colname, cteeth_colname = __get_column_names_from_context(bs, ctx_name)
  raise NotImplementedError("Not implemented yet")
  


def filter_sig_is_in_ctx_teeth(dfsrc,bs,ctx_name):
  teval_colname,cteeth_colname,clips_colname,cjaw_colname = __get_column_names_from_context(bs, ctx_name)
  df_sig_is_in_ctx_teeth = _filter_sig_is_in_ctx_teeth_sell(dfsrc, cteeth_colname, teval_colname) if bs=="S" else _filter_sig_is_in_ctx_teeth_buy(dfsrc, cteeth_colname, teval_colname)
  return df_sig_is_in_ctx_teeth


def filter_sig_ctx_mouth_is_open_and_in_ctx_teeth(dfsrc,bs,ctx_name):
  teval_colname,cteeth_colname,clips_colname,cjaw_colname = __get_column_names_from_context(bs, ctx_name)
  df_sig_ctx_mouth_is_open_and_in_ctx_teeth=_filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_sell(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname) if bs=="S" else _filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_buy(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname)    
  return df_sig_ctx_mouth_is_open_and_in_ctx_teeth

def filter_sig_ctx_mouth_is_open_and_in_ctx_lips(dfsrc,bs,ctx_name):
  teval_colname,cteeth_colname,clips_colname,cjaw_colname = __get_column_names_from_context(bs, ctx_name)
  #print("teval_colname",teval_colname)
  #print("cteeth_colname",cteeth_colname)
  #print("clips_colname",clips_colname)
  #print("cjaw_colname",cjaw_colname)
  df_sig_ctx_mouth_is_open_and_in_ctx_lips=_filter_sig_ctx_mouth_is_open_and_in_ctx_lips_sell(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname)  if bs=="S" else _filter_sig_ctx_mouth_is_open_and_in_ctx_lips_buy(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname)
  return df_sig_ctx_mouth_is_open_and_in_ctx_lips


def __new_ctx_colname(ctx_name,bs,ctx_basename,tolower=False):
  new_col = ctx_basename.replace("_ctx_","_"+ctx_name+"_")  + "_"+bs#.lower()
  fixed_return = new_col.replace("__","_")
  
  return fixed_return if not tolower else fixed_return.lower()

def add_sig_ctx_mouth_is_open_and_in_ctx_lips(dfsrc, bs,ctx_name, new_col=None,ctx_basename = "sig_ctx_mouth_is_open_and_in_ctx_lips")->pd.DataFrame:
  teval_colname,cteeth_colname,clips_colname,cjaw_colname = __get_column_names_from_context(bs, ctx_name)
  if new_col is None:    
    new_col = __new_ctx_colname(ctx_name,bs,ctx_basename)
    
  # Create a boolean mask based on the conditions
  if bs=="S":
    mask = (
        (dfsrc[teval_colname] < dfsrc[clips_colname]) &
        (dfsrc[clips_colname] < dfsrc[cteeth_colname]) &
        (dfsrc[cteeth_colname] < dfsrc[cjaw_colname])
    )
  else:
    mask = (
      (dfsrc[teval_colname] > dfsrc[clips_colname]) &
      (dfsrc[clips_colname] > dfsrc[cteeth_colname]) &
      (dfsrc[cteeth_colname] > dfsrc[cjaw_colname])
      )
    
  
  # Add a new column based on the mask
  dfsrc[new_col] = mask.astype(int)
  
  return dfsrc


# CTX filtering

def _filter_sig_is_in_ctx_teeth_sell(dfsrc, cteeth_colname, teval_colname):
    df_sig_is_in_ctx_teeth=dfsrc[
    dfsrc[teval_colname] > dfsrc[cteeth_colname]
    ].copy()
    return df_sig_is_in_ctx_teeth

def _filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname):
    df_sig_is_in_ctx_teeth=df_sig_is_out_of_normal_mouth[
    df_sig_is_out_of_normal_mouth[teval_colname] < df_sig_is_out_of_normal_mouth[cteeth_colname]
    ].copy()
    return df_sig_is_in_ctx_teeth

  

"""
df_sig_is_in_ctx_teeth = filter_sig_is_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname) if bs=="S" else filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname)

df_sig_ctx_mouth_is_open_and_in_ctx_teeth=filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, clips_colname, cjaw_colname, teval_colname) if bs=="S" else filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, clips_colname, cjaw_colname, teval_colname)    

df_sig_ctx_mouth_is_open_and_in_ctx_lips=filter_sig_ctx_mouth_is_open_and_in_ctx_lips_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, clips_colname, cjaw_colname, teval_colname)  if bs=="S" else filter_sig_ctx_mouth_is_open_and_in_ctx_lips_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, clips_colname, cjaw_colname, teval_colname)
"""

def _filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_sell(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname):
    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = dfsrc[
        dfsrc[teval_colname] > dfsrc[cteeth_colname]
        ].copy()

    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = df_sig_ctx_mouth_is_open_and_in_ctx_teeth[  
        df_sig_ctx_mouth_is_open_and_in_ctx_teeth[clips_colname] < df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cteeth_colname]
        ]
    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = df_sig_ctx_mouth_is_open_and_in_ctx_teeth[  
        df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cteeth_colname] < df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cjaw_colname]
        ]
    return df_sig_ctx_mouth_is_open_and_in_ctx_teeth

def _filter_sig_ctx_mouth_is_open_and_in_ctx_teeth_buy(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname):
    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = dfsrc[
        dfsrc[teval_colname] < dfsrc[cteeth_colname]
        ].copy()

    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = df_sig_ctx_mouth_is_open_and_in_ctx_teeth[  
        df_sig_ctx_mouth_is_open_and_in_ctx_teeth[clips_colname] > df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cteeth_colname]
        ]
    df_sig_ctx_mouth_is_open_and_in_ctx_teeth = df_sig_ctx_mouth_is_open_and_in_ctx_teeth[  
        df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cteeth_colname] > df_sig_ctx_mouth_is_open_and_in_ctx_teeth[cjaw_colname]
        ]
        
    return df_sig_ctx_mouth_is_open_and_in_ctx_teeth


def _filter_sig_ctx_mouth_is_open_and_in_ctx_lips_sell(dfsrc, cteeth_colname, clips_colname, cjaw_colname, teval_colname):
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = dfsrc[
        dfsrc[teval_colname] < dfsrc[clips_colname]
        ].copy()

    # the CMouth is Openned
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = df_sig_ctx_mouth_is_open_and_in_ctx_lips[
        df_sig_ctx_mouth_is_open_and_in_ctx_lips[clips_colname] < df_sig_ctx_mouth_is_open_and_in_ctx_lips[cteeth_colname]
        ]
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = df_sig_ctx_mouth_is_open_and_in_ctx_lips[
        df_sig_ctx_mouth_is_open_and_in_ctx_lips[cteeth_colname] < df_sig_ctx_mouth_is_open_and_in_ctx_lips[cjaw_colname]
        ]
    return df_sig_ctx_mouth_is_open_and_in_ctx_lips



def _filter_sig_ctx_mouth_is_open_and_in_ctx_lips_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, clips_colname, cjaw_colname, teval_colname):
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = df_sig_is_out_of_normal_mouth[
        df_sig_is_out_of_normal_mouth[teval_colname] > df_sig_is_out_of_normal_mouth[clips_colname]
        ].copy()

    # the BMouth is Openned
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = df_sig_ctx_mouth_is_open_and_in_ctx_lips[
        df_sig_ctx_mouth_is_open_and_in_ctx_lips[clips_colname] > df_sig_ctx_mouth_is_open_and_in_ctx_lips[cteeth_colname]
        ]
    df_sig_ctx_mouth_is_open_and_in_ctx_lips = df_sig_ctx_mouth_is_open_and_in_ctx_lips[
        df_sig_ctx_mouth_is_open_and_in_ctx_lips[cteeth_colname] > df_sig_ctx_mouth_is_open_and_in_ctx_lips[cjaw_colname]
        ]
        
    return df_sig_ctx_mouth_is_open_and_in_ctx_lips



def __get_column_names_from_context(bs, ctx_name):
    teval_colname = LOW if bs=="S" else HIGH
    cteeth_colname,clips_colname,cjaw_colname=get_alligator_column_names_from_ctx_name(ctx_name)
    return teval_colname,cteeth_colname,clips_colname,cjaw_colname