


#@STCGoal Future Proto where Sub-Patterns are created from TTF with their corresponding Columns list and mayby Lags

from mlconstants import MFI_DEFAULT_COLNAME
from mlconstants import default_columns_to_get_from_higher_tf
 def get_ttf_subpattern_columns_list_from_higher_tf(subpatternname:str):
  if subpatternname == "ttf":
    return default_columns_to_get_from_higher_tf
  if subpatternname == "mfi":
    return [MFI_DEFAULT_COLNAME]
  pass
  