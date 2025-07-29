# jgtml
version='0.0.296'
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from jtc import (
    calculate_target_variable_min_max as calc_target_from_df,
    pto_target_calculation as calc_target_to_file,
    readMXFile as read
)

from jplt import (an_biv_plt2ds as plot_an_biv_plt2ds, an_bivariate_plot00 as plot_an_bivariate_plot00)

from ptottf import create_ttf_csv as create_ttf
from mlfsvc import create_mlf


from jgtapp import (fxtr,
                    fxaddorder,
                    fxmvstop,
                    fxmvstopgator,
                    fxmvstopfdb,
                    fxrmorder,
                    fxrmtrade,
                    ids,mlf,ttf,cds,pds,mx)

def __init__():
    """
    Initialize the jgtml module.
    """
    print("jgtml version: ", version)
    pass
