import pandas as pd

pd.options.mode.copy_on_write = True
#PerformanceWarning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)



from mlconstants import CONVERTION_EXCLUDED_COLUMNS


def add_lagging_columns(dfsrc: pd.DataFrame, columns_to_add_lags_to, lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_', dropna=True)->pd.DataFrame:
    new_cols = []  # List to hold new lagging columns
    convertion_included=[] # Those columns that are not in the excluded list (their parent somehow, we want to convert them to int when we add lagging columns but not those that are in the excluded list (mostly because they are double))
    for col in columns_to_add_lags_to:
        if col not in dfsrc.columns:
            print("WARN::Column not in dataframe:", col, " Skipping")
            continue
        else:
            for j in range(1, total_lagging_periods + 1):
                # Create new lagging column without modifying the original DataFrame
                lag_col_name = _create_lag_column_name(out_lag_midfix_str, col, j)
                lag_col = dfsrc[col].shift(j * lag_period).rename(lag_col_name)
                new_cols.append(lag_col)
                if col not in CONVERTION_EXCLUDED_COLUMNS:
                    convertion_included=convertion_included+[lag_col_name]

    # Concatenate the original DataFrame with the new columns
    dfsrc = pd.concat([dfsrc] + new_cols, axis=1)

    # Drop rows where there are no lag values
    if dropna:
        dfsrc.dropna(inplace=True)

    # Convert lagging columns to integer
    for col in columns_to_add_lags_to:
        for j in range(1, total_lagging_periods + 1):
            lag_col_name = _create_lag_column_name(out_lag_midfix_str, col, j)
            if lag_col_name in convertion_included: #Hopefully, double columns wont be converted
              dfsrc[lag_col_name] = dfsrc[lag_col_name].astype(int)
            else:
              pass

    return dfsrc

from mldatahelper import _create_lag_column_name

  
def add_lagging_columns_V1(dfsrc: pd.DataFrame, columns_to_add_lags_to, lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_',dropna=True):
  for col in columns_to_add_lags_to:
    if col not in dfsrc.columns:
      print("WARN::Column not in dataframe:", col, " Skipping")
      pass
    else:
      for j in range(1, total_lagging_periods + 1):
      # Using .loc to ensure the operation is done without warnings
        dfsrc.loc[:, f'{col}{out_lag_midfix_str}{j}'] = dfsrc[col].shift(j * lag_period)
  # Drop rows where there are no lag values
  if dropna:
    dfsrc.dropna(inplace=True)
    
  for col in columns_to_add_lags_to: #@STCIssue Isn't that done already ???  Or it thinks they are Double !!!!
    for j in range(1, total_lagging_periods + 1):
      dfsrc[f'{col}{out_lag_midfix_str}{j}']=dfsrc[f'{col}{out_lag_midfix_str}{j}'].astype(int)
  return dfsrc
