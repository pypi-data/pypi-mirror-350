#%%

import json
import pandas as pd

f="NZD-CAD_m15_2408291352_mouth_no_yet_open.csv"
import os
bdir="../tests/fdb_data"
fpath=os.path.join(bdir,f)

df=pd.read_csv(fpath)



from SOHelper import get_bar_at_index

# %%
cb=get_bar_at_index(df,-1)
lb=get_bar_at_index(df,-2)
# %%
cb
# %%
lb
# %%
lb["lips"]
# %%
cb["lips"]
# %%
