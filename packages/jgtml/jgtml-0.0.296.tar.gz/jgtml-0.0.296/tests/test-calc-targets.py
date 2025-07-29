#%% Imports
import pandas as pd
import os
import jgtml as jml

#%% Input/Output directories
default_jgtpy_data_full= 'full/data'
default_jgtpy_data_full= '/var/lib/jgt/full/data'
data_dir_full = os.getenv('JGTPY_DATA_FULL', default_jgtpy_data_full)
indir_cds = os.path.join(data_dir_full, 'cds')
outdir_tmx = os.path.join(data_dir_full, 'targets', 'mx') #@STCIssue Hardcoded path future JGTPY_DATA_FULL/.../mx

# Create directory if it does not exist
if not os.path.exists(outdir_tmx):
    os.makedirs(outdir_tmx)


import tlid
tlid_tag = tlid.get_minutes()

#%% Read Data
crop_start_dt = "2010-01-01"
crop_end_dt = "2023-10-12"

crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

instruments = I_raw.split(',')
timeframes = T_raw.split(',')


#def pov_target_calculation_n_output240222(indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t


print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        #pov_target_calculation_n_output240222(calculate_target_variable_min_max, indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)
        jml.pov_calc_targets(indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)
        #pov_target_calculation_n_output240222(calculate_target_variable_min_max, indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)



