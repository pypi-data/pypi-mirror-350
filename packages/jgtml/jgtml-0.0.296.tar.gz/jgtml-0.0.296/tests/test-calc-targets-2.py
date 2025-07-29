#%% Imports
import pandas as pd
import os
#import jgtml as jml
from jgtml import  jtc

from jgtml import jplt

import tlid
tlid_tag = tlid.get_minutes()


crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

instruments = I_raw.split(',')
timeframes = T_raw.split(',')



print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        #Date,Volume,Open,High,Low,Close,Median,ao,ac,jaw,teeth,lips,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,fdbb,fdbs,fdb,aof,aofvalue,aoaz,aobz,zlc,zlcb,zlcs,aocolor,accolor,zcol,sz,bz,acs,acb,ss,sb,price_peak_above,price_peak_bellow,ao_peak_above,ao_peak_bellow,target,vector_ao_fdbs,vector_ao_fdbb
        # additional_columns_to_drop=['Volume','Open','High','Low','Close','Median','ao','ac','jaw','teeth','lips','fh','fl','fh3','fl3','fh5','fl5','fh8','fl8','fh13','fl13','fh21','fl21','fh34','fl34','fh55','fl55','fh89','fl89','fdbb','fdbs','fdb','aof','aofvalue','aoaz','aobz','zlc','zlcb','zlcs','aocolor','accolor','zcol','sz','bz','acs','acb','ss','sb','price_peak_above','price_peak_bellow','ao_peak_above','ao_peak_bellow','target','vector_ao_fdbs','vector_ao_fdbb']
        # additional_columns_to_drop=['Volume','Open','High','Low','Close','Median','ao','ac','jaw','teeth','lips','fh','fl','fh3','fl3','fh5','fl5','fh8','fl8','fh13','fl13','fh21','fl21','fh34','fl34','fh55','fl55','fh89','fl89','fdbb','fdbs','fdb','aof','aofvalue','aoaz','aobz','zlc','zlcb','zlcs','aocolor','accolor','zcol','sz','bz','acs','acb','ss','sb','price_peak_above','price_peak_bellow','ao_peak_above','ao_peak_bellow','target','vector_ao_fdbs','vector_ao_fdbb']
        selected_columns_to_keep  =['High','Low','ao','ac','jaw','teeth','lips','fh','fl','fdbb','fdbs','zlcb','zlcs','target','vector_ao_fdbs','vector_ao_fdbb']
        #selected_columns_to_keep=['Volume','High','Low','ao','ac','jaw','teeth','lips','fh','fl','fdbb','fdbs','aocolor','accolor','zcol','sz','bz','acs','acb','ss','sb','price_peak_above','price_peak_bellow','ao_peak_above','ao_peak_bellow']
        
        
        r,s1,s2= jtc.pto_target_calculation(i,t,pto_vec_fdb_ao_vector_window_flag=True,
                drop_calc_col=False,
                selected_columns_to_keep=selected_columns_to_keep)
        


