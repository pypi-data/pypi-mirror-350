import pandas as pd

from mlconstants import MFI_DEFAULT_COLNAME
from jgtutils.colconverthelper import mfi_str_to_id,mfi_signal_to_str,get_mfi_features_column_list_by_timeframe


def column_mfi_str_in_dataframe_to_id(df:pd.DataFrame,t:str,inplace=False,mfi_colname=""):
    """
    Convert the MFI string columns in the dataframe to their corresponding MFI ID.
    
    Parameters:
    df (pd.DataFrame): The dataframe to convert the MFI string columns to their corresponding MFI ID.
    t (str): The timeframe to get the MFI features columns for.
    mfi_colname (str): The name of the MFI column to use. Default is MFI_VAL (plan to upgrade to MFI_SIGNAL)
    
    Returns:
    pd.DataFrame: The dataframe with the MFI string columns converted to their corresponding MFI ID.
    """
    if mfi_colname=="":
        mfi_colname=MFI_DEFAULT_COLNAME
    
    if not inplace:
        df = df.copy()
    
    mfi_str_selected_columns=get_mfi_features_column_list_by_timeframe(t,mfi_colname)
    
    for col_name in mfi_str_selected_columns:
        #check if the column exists in the dataframe
        if col_name not in df.columns:
            continue
        df[col_name] = df[col_name].apply(lambda x: int(mfi_str_to_id(x)))
    return df

def column_mfi_str_back_to_str_in_dataframe(df:pd.DataFrame,t:str,inplace=False,mfi_colname=""):
    if not inplace:
        df = df.copy()    
    mfi_str_selected_columns=get_mfi_features_column_list_by_timeframe(t,mfi_colname)
    for col_name in mfi_str_selected_columns:
        #check if the column exists in the dataframe
        if col_name not in df.columns:
            continue
        df[col_name] = df[col_name].apply(lambda x: mfi_signal_to_str(x)).copy()
    return df