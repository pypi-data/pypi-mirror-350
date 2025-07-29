
#@STCGoal A Class to store MX stuff out of the way from jtc



import pandas as pd
import numpy as np
from jgtutils.jgtconstants import DATE,ZLCB,ZLCS


def count_bars_before_zero_line_cross(df:pd.DataFrame,turn_negative_if_sell=True):
    bars_before_signal = 0
    signal_was_sell=False
    for i in range(len(df) - 1, -1, -1):
      prev_row = df.iloc[i]
      if prev_row[ZLCS] or prev_row[ZLCB]:
        if prev_row[ZLCS]:
          signal_was_sell=True
        break
      bars_before_signal += 1
    if signal_was_sell and turn_negative_if_sell:
      bars_before_signal=bars_before_signal*-1 #turn it into a negative number
    return bars_before_signal


