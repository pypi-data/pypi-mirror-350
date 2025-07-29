import argparse
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from mlclicommon import (add_patterns_arguments,
                         check_arguments)

from mlcliconstants import TTFCLI_DESCRIPTION, TTFCLI_EPILOG, TTFCLI_PROG_NAME
from ptottf import create_ttf_csv # type: ignore
from jgtutils import jgtcommon

def _parse_args():
    parser:argparse.ArgumentParser=jgtcommon.new_parser(TTFCLI_DESCRIPTION,TTFCLI_EPILOG,TTFCLI_PROG_NAME)
    parser=jgtcommon.add_instrument_timeframe_arguments(parser)
    parser=jgtcommon.add_use_fresh_argument(parser)
    parser=jgtcommon.add_bars_amount_V2_arguments(parser)
    parser=jgtcommon.add_patterns_arguments(parser)
    
    #DEPRECATED
    #parser.add_argument("-fr", "--force_read", action="store_true", help="Force to read CDS (should increase speed but relies on existing data)")
  
    # #columns_list_from_higher_tf
    # pn_group=parser.add_argument_group("Patterns")
    # pn_group.add_argument("-clh", "--columns_list_from_higher_tf", nargs='+', help="List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao", default=None)
    # #@STCGoal Future Proto where Sub-Patterns are created from TTF with their corresponding Columns list and mayby Lags
    # #patternname
    # pn_group.add_argument("-pn", "--patternname", help="Pattern Name", default="ttf")
    

    args = jgtcommon.parse_args(parser)
    
    args =check_arguments(args)
    
    return args


def main():
  args = _parse_args()
  
  columns_list_from_higher_tf = args.columns_list_from_higher_tf if args.columns_list_from_higher_tf else None
  
  #print("Columns List from Higher TF:",columns_list_from_higher_tf)
  
  pseudo_force_read_flag = True if not args.fresh else False
  create_ttf_csv(args.instrument, args.timeframe, args.full if args.full else False, True if args.fresh else False, args.quotescount,pseudo_force_read_flag, columns_list_from_higher_tf=columns_list_from_higher_tf, pn=args.patternname, args=args)

if __name__ == "__main__":
  main()
  