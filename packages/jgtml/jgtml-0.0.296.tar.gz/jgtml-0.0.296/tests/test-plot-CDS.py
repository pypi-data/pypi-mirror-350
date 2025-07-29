#%% Imports
import pandas as pd
import os
#import jgtml as jml
from jgtml import  jtc
import jgtml as jml

from jgtml import jplt
from jgtpy import JGTADS as ads

import tlid
tlid_tag = tlid.get_minutes()


crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

I_raw = "SPX500,GBP/USD"
T_raw = "D1,H4"

instruments = I_raw.split(',')
timeframes = T_raw.split(',')



print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        #jtc.pto_target_calculation(i,t)
        c,a,d=ads.plot(i,t,show=False)
        td=jml.calc_target_from_df(d)
        p=jplt.an_bivariate_plot00(td)
        p.show()




# %%
