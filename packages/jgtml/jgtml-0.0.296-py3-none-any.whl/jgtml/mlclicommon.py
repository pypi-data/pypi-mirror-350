"""
Common functions for various cli of the jgtml project

- instrument/timeframe arguments
- force_refresh
- columns_list_from_higher_tf
- bars_amount_V2_arguments
- use_fresh_argument
- dropna_volume_argument
- drop_bid_ask
- columns_to_keep
- columns_to_drop
- lag_period
- total_lagging_periods
- patternname

"""


import argparse
from jgtutils import jgtcommon
from jgtutils.jgtcommon import _get_group_by_title


from mlcliconstants import TTF_DEFAULT_PATTERN_NAME
from jgtutils.jgtcommon import add_patterns_arguments,add_timeframe_standalone_argument,new_parser,add_format_outputs_arguments
  
def __deprecate_force_read(args:argparse.Namespace):
  try:
    if hasattr(args,'force_read') and args.force_read is True:
      print("force_read is deprecated.  Use --fresh instead")
  except:
    pass

# def add_format_outputs_arguments(parser:argparse.ArgumentParser=None)->argparse.ArgumentParser:
#   global default_parser
#   if parser is None:
#     parser=default_parser
  
#   out_group=_get_group_by_title(parser,"Outputs")
#   f_exclusive=out_group.add_mutually_exclusive_group()
#   f_exclusive.add_argument("-json", "--json_output", help="Output in JSON format", action="store_true")
#   #Markdown
#   f_exclusive.add_argument("-md", "--markdown_output", help="Output in Markdown format", action="store_true")
#   return parser

# def add_patterns_arguments(parser:argparse.ArgumentParser=None)->argparse.ArgumentParser:
#   global default_parser
#   if parser is None:
#     parser=default_parser
  
#   pn_group=_get_group_by_title(parser,"Patterns")
#   pn_group.add_argument("-clh", "--columns_list_from_higher_tf", nargs='+', help="List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao", default=None)
  
#   pn_group.add_argument("-pn", "--patternname", help="Pattern Name")
  
#   pn_group.add_argument("-pls", "--list-patterns", help="List Patterns", action="store_true")
  
#   #Add the format outputs
#   parser=add_format_outputs_arguments(parser)
#   return parser

def check_arguments(args:argparse.Namespace)->argparse.Namespace:
  
  __deprecate_force_read(args)
  
  #If we are listing patterns, then we do that, print results and exit
  cli_output_patterns_list_then_exit(args)
  args=set_columns_list_from_pattern(args)
  args=_check_pattern_arguments(args)
  return args

def _check_pattern_arguments(args:argparse.Namespace,quiet=True)->argparse.Namespace:
  
  # if args.list_patterns:
  #   if not quiet:
  #     print("List Patterns")
  #   return args
  if not args.flag_columns_were_read:
    args=_convert_clh_args_as_csv_to_list(args)
  #if the patternname is not the default, then columns_list_from_higher_tf should be set
  try:
    pn = args.patternname
    columns_list = pndata__read_new_pattern_columns_list(pn=pn,args=args)
  except:
    columns_list = None
  if columns_list is None and not args.columns_list_from_higher_tf:
    example_cli = f"[...] -pn {args.patternname} -clh <col1 col2 col3>"
    print(example_cli)
    raise Exception("Pattern Name is not the default.  Please set the columns_list_from_higher_tf.  \n" + example_cli)
  # We might have passed the columns_list_from_higher_tf with CSV rathen than space separated, so we convert it to list
  return args

def cli_output_patterns_list_then_exit(args:argparse.Namespace):
    if args.list_patterns:
        output_type="object"
        try:
          json_output = True if args.json_output  else False
          md_output = True if args.markdown_output else False
          output_type="json" if json_output else "md" if md_output else "object"
        except:
          pass
        patterns_list_results=pndata__get_all_patterns(output_type=output_type,args=args)
        print(patterns_list_results)
        exit(0)



from mldatahelper import pndata__get_all_patterns, pndata__read_new_pattern_columns_list
def set_columns_list_from_pattern(args:argparse.Namespace):
  args.flag_columns_were_read=False
  if args.patternname and not args.columns_list_from_higher_tf:
    args.columns_list_from_higher_tf = pndata__read_new_pattern_columns_list(pn=args.patternname,args=args)
    args.flag_columns_were_read=True
  return args

def _convert_clh_args_as_csv_to_list(args:argparse.Namespace):
  try:
    our_first_value_with_might_have_csv:str = args.columns_list_from_higher_tf[0]
    flag_columns_have_csv_detected_string=our_first_value_with_might_have_csv.find(",")>=0
    flag_columns_are_csv_string = isinstance(our_first_value_with_might_have_csv,str) and flag_columns_have_csv_detected_string
    if args.patternname  and flag_columns_are_csv_string:
      our_new_list_items:list[str] = our_first_value_with_might_have_csv.split(",")
      c=0
      args.columns_list_from_higher_tf[0]=our_new_list_items[0]
      
      for item in our_new_list_items:      
        if c>0:
            args.columns_list_from_higher_tf.append(item)
        c+=1
  except:
    pass
  return args
        
        
        

## THAT BELLOW ARE TEST, DONT USE IT or MAKE IT WORKS.  
# #@STCIssue Mastery parent parsing
def create_parent_jgtcommon_parser(description:str,prog:str,epilog:str)->argparse.ArgumentParser:
  parser=argparse.ArgumentParser(add_help=False)
    #jgtcommon.new_parser(description,prog,epilog)
  parser.add_help=False
  parser=jgtcommon.add_instrument_timeframe_arguments(parser)
  parser=jgtcommon.add_use_fresh_argument(parser)
  parser=jgtcommon.add_bars_amount_V2_arguments(parser)
  return parser

def new_child_parser(description:str,prog:str,epilog:str)->argparse.ArgumentParser:
  parent_parser:argparse.ArgumentParser=create_parent_jgtcommon_parser(description,prog,epilog)
  parser = argparse.ArgumentParser(description=description,prog=prog+"-child",epilog=epilog)
  #parser.add_subparsers(dest='command',type[])
  
  # parser=jgtcommon.add_instrument_timeframe_arguments(parser)
  # parser=jgtcommon.add_use_fresh_argument(parser)
  # parser=jgtcommon.add_bars_amount_V2_arguments(parser)
  return parser



def parse_args(parser:argparse.ArgumentParser)->argparse.Namespace:
  #args:argparse.Namespace=jgtcommon.parse_args(parser)
  args=parser.parse_args()
  #raise "Not Implemented Fully.  #@STCIssue Parent Parser not implemented and understood"
  return args


