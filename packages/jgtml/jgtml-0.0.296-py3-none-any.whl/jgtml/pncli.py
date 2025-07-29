import argparse
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtutils import jgtcommon
from mlclicommon import add_patterns_arguments,add_timeframe_standalone_argument
from mlclicommon import __deprecate_force_read, check_arguments,add_format_outputs_arguments
from mlcliconstants import PNCLI_DESCRIPTION, PNCLI_EPILOG, PNCLI_PROG_NAME
from mldatahelper import pndata__write_new_pattern_columns_list,pndata__read_new_pattern_columns_list,pndata__read_new_pattern_columns_list_with_htf,pndata__get_all_patterns

def _parse_args():
    parser=jgtcommon.new_parser(PNCLI_DESCRIPTION, PNCLI_EPILOG, PNCLI_PROG_NAME)

    parser=add_patterns_arguments(parser)
    parser=add_timeframe_standalone_argument(parser)

    args = jgtcommon.parse_args(parser)
    args=check_arguments(args)
    return args

DEV_2407=False
def main():
    args = _parse_args()
    
    
    if DEV_2407:
        print(args)
    
    #cli_output_patterns_list(args)
        
    columns_list_from_higher_tf = args.columns_list_from_higher_tf if args.columns_list_from_higher_tf else None
    
    if columns_list_from_higher_tf and not args.flag_columns_were_read:
        pndata__write_new_pattern_columns_list(columns_list_from_higher_tf=columns_list_from_higher_tf, pn=args.patternname)
    else:
        if not args.timeframe or args.timeframe == "-":
            columns_list = pndata__read_new_pattern_columns_list(pn=args.patternname)
        else:
            columns_list = pndata__read_new_pattern_columns_list_with_htf(pn=args.patternname, t=args.timeframe)
        print("Columns List from Pattern:", columns_list)




if __name__ == "__main__":
    main()