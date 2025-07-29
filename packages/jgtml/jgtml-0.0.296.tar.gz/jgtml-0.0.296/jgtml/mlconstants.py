

from jgtutils.jgtconstants import ( AO,MFI_SIGNAL,AC,JAW,TEETH,LIPS,BJAW,BLIPS,BTEETH,TLIPS,TTEETH,TJAW,HIGH,LOW,CLOSE,OPEN,ASKCLOSE,ASKHIGH,ASKLOW,BIDCLOSE,BIDHIGH,BIDLOW,MFI)

from jgtutils.jgtconstants import ZONE_SIGNAL as ZONE_DEFAULT_COLNAME
from jgtutils.jgtconstants import MFI_SIGNAL as MFI_DEFAULT_COLNAME
from jgtutils.jgtconstants import FDB_TARGET as TARGET
MFI_DEFAULT_COLTYPE=int
ZONE_DEFAULT_COLTYPE=int
TARGET_COLTYPE=float

from jgtutils.coltypehelper import DTYPE_DEFINITIONS as DTYPE_DEFINITIONS__CDS

 
TTF_DTYPE_DEFINITION = {MFI_DEFAULT_COLNAME: MFI_DEFAULT_COLTYPE,ZONE_DEFAULT_COLNAME: ZONE_DEFAULT_COLTYPE, 'zone_sig_M1':int,'zone_sig_W1':int,'zone_sig_D1':int,'zone_sig_H4':int,'zone_sig_H1':int, 'mfi_sig_M1':int,'mfi_sig_W1':int,'mfi_sig_D1':int,'mfi_sig_H4':int,'mfi_sig_H1':int,'zcol':str,'mfi_sq':int,'mfi_green':int,'mfi_fade':int,'mfi_fake':int,'price_peak_above':int,'price_peak_bellow':int,'ao_peak_above':int,'ao_peak_bellow':int,'ao_sig_M1':float,'ao_sig_W1':float,'ao_sig_D1':float,'ao_sig_H4':float,'ao_sig_H1':float,'ao_sig_m15':float,'ao_sig_m5':float,'mfi_str':str}


default_columns_to_get_from_higher_tf = [MFI_DEFAULT_COLNAME, ZONE_DEFAULT_COLNAME, AO]

TTF_NOT_NEEDED_COLUMNS_LIST=[ 'mfi_str','zcol','price_peak_above', 'price_peak_bellow','ao_peak_above','ao_peak_bellow'] #Migrate to settings ??

TTF2RUN_DEFAULT=["mfi"]



#@STCGoal Sample Data for design of the columns
"""
SPX500,D1,S,-29.06,836,-24292.0,all_evalname_signals,,Unfiltered FDB Sell Signal
SPX500,D1,S,-28.18,567,-15980.0,sig_normal_mouth_is_open,,FDB Sell Signal when Normal Mouth is Open
SPX500,D1,S,-29.62,772,-22866.0,sig_is_out_of_normal_mouth,,FDB Sell Signal is Out of Normal Mouth and Mouth is Open
SPX500,D1,S,-32.67,667,-21793.0,sig_is_in_ctx_teeth_sum,tide,FDB Sell Signal In the Tide Alligator Teeth
SPX500,D1,S,-123.41,34,-4196.0,sig_ctx_mouth_is_open_and_in_ctx_lips,tide,Tide Alligator Mouth is Open and FDB Sell Signal is in the Tide Alligator Lips
SPX500,D1,S,-87.44,45,-3935.0,sig_ctx_mouth_is_open_and_in_ctx_teeth_sum,tide,Tide Alligator Mouth is Open and FDB Sell Signal is in the Tide Alligator Teeth
SPX500,D1,S,-29.06,836,-24292.0,all_evalname_signals,,Unfiltered FDB Sell Signal
SPX500,D1,S,-28.18,567,-15980.0,sig_normal_mouth_is_open,,FDB Sell Signal when Normal Mouth is Open
SPX500,D1,S,-29.62,772,-22866.0,sig_is_out_of_normal_mouth,,FDB Sell Signal is Out of Normal Mouth and Mouth is Open
SPX500,D1,S,-32.67,667,-21793.0,sig_is_in_ctx_teeth_sum,tide,FDB Sell Signal In the Tide Alligator Teeth
SPX500,D1,S,-123.41,34,-4196.0,sig_ctx_mouth_is_open_and_in_ctx_lips,tide,Tide Alligator Mouth is Open and FDB Sell Signal is in the Tide Alligator Lips
SPX500,D1,S,-87.44,45,-3935.0,sig_ctx_mouth_is_open_and_in_ctx_teeth_sum,tide,Tide Alligator Mouth is Open and FDB Sell Signal is in the Tide Alligator Teeth
SPX500,D1,B,290.77,559,162543.0,all_evalname_signals,,Unfiltered FDB Buy Signal
SPX500,D1,B,131.39,235,30877.0,sig_normal_mouth_is_open,,FDB Buy Signal when Normal Mouth is Open
SPX500,D1,B,251.87,483,121651.0,sig_is_out_of_normal_mouth,,FDB Buy Signal is Out of Normal Mouth and Mouth is Open
SPX500,D1,B,215.85,145,31298.0,sig_is_in_ctx_teeth_sum,tide,FDB Buy Signal In the Tide Alligator Teeth
SPX500,D1,B,380.39,263,100042.0,sig_ctx_mouth_is_open_and_in_ctx_lips,tide,Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Lips
SPX500,D1,B,-25.51,67,-1709.0,sig_ctx_mouth_is_open_and_in_ctx_teeth_sum,tide,Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Teeth

SPX500,D1,B,290.77,559,162543.0,all_evalname_signals,,Unfiltered FDB Buy Signal
SPX500,D1,B,131.39,235,30877.0,sig_normal_mouth_is_open,,FDB Buy Signal when Normal Mouth is Open
SPX500,D1,B,251.87,483,121651.0,sig_is_out_of_normal_mouth,,FDB Buy Signal is Out of Normal Mouth and Mouth is Open
SPX500,D1,B,215.85,145,31298.0,sig_is_in_ctx_teeth_sum,tide,FDB Buy Signal In the Tide Alligator Teeth
SPX500,D1,B,380.39,263,100042.0,sig_ctx_mouth_is_open_and_in_ctx_lips,tide,Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Lips
SPX500,D1,B,-25.51,67,-1709.0,sig_ctx_mouth_is_open_and_in_ctx_teeth_sum,tide,Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Teeth
"""






NORMAL_MOUTH_IS_OPEN_COLNAME='normal_mouth_is_open'
CURRENT_BAR_IS_OUT_OF_NORMAL_MOUTH_COLNAME='current_bar_is_out_of_normal_mouth'


#@STCGoal Meant to be used as base column to replace 'ctx' by 'big' or 'tide'
CURRENT_BAR_IS_IN_CTX_TEETH_COLNAME='current_bar_is_in_ctx_teeth'
CTX_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_CTX_LIPS_COLNAME='ctx_mouth_is_open_and_current_bar_is_in_ctx_lips'
MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_CTX_TEETH_COLNAME='mouth_is_open_and_current_bar_is_in_ctx_teeth'

#@STCIssue Big's column naming based on above that we might want to standardize later
CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME='current_bar_is_in_big_teeth'
BIG_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_LIPS_COLNAME='big_mouth_is_open_and_current_bar_is_in_big_lips'
MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME='mouth_is_open_and_current_bar_is_in_big_teeth'


#@STCIssue Tide's column naming based on above that we might want to standardize later
CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME='current_bar_is_in_tide_teeth'
TIDE_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_LIPS_COLNAME='tide_mouth_is_open_and_current_bar_is_in_tide_lips'
MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME='mouth_is_open_and_current_bar_is_in_tide_teeth'


MX_NS="targets/mx"


PATTERN_NS = "pn"



CONVERTION_EXCLUDED_COLUMNS=[AO,AC,JAW,TEETH,LIPS,BJAW,BLIPS,BTEETH,TLIPS,TTEETH,TJAW,HIGH,LOW,CLOSE,OPEN,ASKCLOSE,ASKHIGH,ASKLOW,BIDCLOSE,BIDHIGH,BIDLOW,MFI]