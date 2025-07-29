
#@STCIssue Any Mouth Related Signals have a relationship with Selling or Buying.  Can we represent this in the features?  For that, I think we have to consider the Model is going to evaluate a Selling or Buying Signal, therefore, can we represent the Mouth Signals for either Selling or Buying?  If so, how?  
#@STCGoal Wrap the Feature preparation done in these sessions.  As result: we have a file for an input POV in the JGTPY_DATA_FULL/mlf/$i_$t.csv
##@STCGoal It contains columns feature ready for the model.

""" # TO ADJUST....
  'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'mfi_str_M1', 'zcol_M1', 'ao_M1', 'mfi_str_W1',
       'zcol_W1', 'ao_W1'
"""
##@STCGoal It can be a source for the making of MX Data.

from jgtml import mfihelper2 as mfihelper, mxconstants as mxc, mxhelper as mxhelper,realityhelper,zonehelper
from jgtutils.jgtconstants import JAW,TEETH,LIPS,HIGH,LOW,BJAW,BTEETH,BLIPS,TJAW,TTEETH,TLIPS

#@STCIssue Requires validation from the jgtml_obsds_240515_TIDE_SIGNALS.py prototype
_NOT_VALIDATED__SEE_RAISED_MESSAGE = 'Not Validated, see: jgtml_obsds_240515_TIDE_SIGNALS.py for logics'



def __detect_directions(df,detected_direction_colname = 'detected_dir',colvalue_if_direction_is_sell = -1,colvalue_if_direction_is_buy = 1,colvalue_if_oscillating = 0):
  """
  Detect the directions of the normal alligator (JAW,TEETH,LIPS) with the relationship of current price (HIGH,LOW).
  
  Parameters:
  df: pd.DataFrame - the dataframe to detect the directions of the normal alligator using the 3 alligators existing columns (JAW,TEETH,LIPS) and the current price (HIGH,LOW)
  detected_direction_colname: str - the column name to store the detected direction
  colvalue_if_direction_is_sell: str - the column value if the direction is sell
  colvalue_if_direction_is_buy: str - the column value if the direction is buy
  colvalue_if_oscillating: str - the column value if the direction is oscillating
  
  Returns:
  pd.DataFrame - the dataframe with the directions of the normal alligator detected
  """
  
  #@STCGoal What is the optimal way to dectect direction ? 
  def evaluate_direction(row):
    if row[JAW] > row[TEETH] and row[TEETH] > row[LIPS] and row[HIGH] < row[LIPS]:
      return colvalue_if_direction_is_sell
    elif row[JAW] < row[TEETH] and row[TEETH] < row[LIPS] and row[LOW] > row[LIPS]:
      return colvalue_if_direction_is_buy
    else:
      return colvalue_if_oscillating

  
  #df[detected_direction_colname]= colvalue_if_direction_is_sell if df[JAW] > df[TEETH] and df[TEETH] > df[LIPS] and df[HIGH] < df[LIPS] else colvalue_if_direction_is_buy if df[JAW] < df[TEETH] and df[TEETH] < df[LIPS] and df[LOW] > df[LIPS] else colvalue_if_oscillating
  df[detected_direction_colname] = df.apply(evaluate_direction, axis=1)
  return df

from mlconstants import NORMAL_MOUTH_IS_OPEN_COLNAME
def __add_normal_mouth_is_open(df):
  """
  Add the Normal Mouth Is Open Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Normal Mouth Is Open Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Normal Mouth Is Open Flag added
  """
  detected_direction=__detect_directions(df)
  df[NORMAL_MOUTH_IS_OPEN_COLNAME] = (df[JAW] > df[TEETH]) & (df[TEETH] > df[LIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df

from mlconstants import CURRENT_BAR_IS_OUT_OF_NORMAL_MOUTH_COLNAME
def __add_current_bar_is_out_of_normal_mouth(df):
  """
  Add the Current Bar Is Out of Normal Mouth Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Current Bar Is Out of Normal Mouth Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Current Bar Is Out of Normal Mouth Flag added
  """

  df[CURRENT_BAR_IS_OUT_OF_NORMAL_MOUTH_COLNAME] = (df[HIGH] > df[JAW]) | (df[LOW] < df[LIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df


def _add_normal_alligator_flag_signals(df,
                    add_normal_mouth_is_open=True,
                    add_current_bar_is_out_of_normal_mouth=True
                    ):
  """
  Add the Normal Alligator Flag Signals to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Normal Alligator Flag Signals to
  add_normal_mouth_is_open: bool - Add flag to output that tells if the normal alligator mouth is Open
  add_current_bar_is_out_of_normal_mouth: bool - Signal Out of the Normal Alligator Mouth
  
  Returns:
  pd.DataFrame - the dataframe with the Normal Alligator Flag Signals added
  """
  if add_normal_mouth_is_open:
    __add_normal_mouth_is_open(df)
  if add_current_bar_is_out_of_normal_mouth:
    __add_current_bar_is_out_of_normal_mouth(df)
  

from mlconstants import CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME
def __add_current_bar_is_in_big_teeth(df):
  """
  Add the Current Bar Is In Big Teeth Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Current Bar Is In Big Teeth Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Current Bar Is In Big Teeth Flag added
  """
  df[CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME] = (df[BTEETH] > df[BJAW]) & (df[BTEETH] > df[BLIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df

#__add_big_mouth_is_open_and_current_bar_is_in_big_lips(df)
from mlconstants import BIG_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_LIPS_COLNAME
def __add_big_mouth_is_open_and_current_bar_is_in_big_lips(df):
  """
  Add the Big Mouth Is Open and Current Bar Is In Big Lips Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Big Mouth Is Open and Current Bar Is In Big Lips Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Big Mouth Is Open and Current Bar Is In Big Lips Flag added
  """
  df[BIG_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_LIPS_COLNAME] = (df[BJAW] > df[BTEETH]) & (df[BJAW] > df[BLIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df

#__add_mouth_is_open_and_current_bar_is_in_big_teeth(df)
from mlconstants import MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME
def __add_mouth_is_open_and_current_bar_is_in_big_teeth(df):
  """
  Add the Mouth Is Open and Current Bar Is In Big Teeth Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Mouth Is Open and Current Bar Is In Big Teeth Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Mouth Is Open and Current Bar Is In Big Teeth Flag added
  """
  df[MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME] = (df[BLIPS] > df[BTEETH]) & (df[BLIPS] > df[BJAW]) #GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df


def _add_big_mouth_flag_signals(df,
                    add_current_bar_is_in_big_teeth=True,
                    add_big_mouth_is_open_and_current_bar_is_in_big_lips=True,
                    add_mouth_is_open_and_current_bar_is_in_big_teeth=True):
  """
  Add the Big Mouth Flag Signals to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Big Mouth Flag Signals to
  add_current_bar_is_in_big_teeth: bool - Signal current bar is in Big Teeth
  add_big_mouth_is_open_and_current_bar_is_in_big_lips: bool - Signal Big Mouth is Open and Current Bar is in Big Lips
  add_mouth_is_open_and_current_bar_is_in_big_teeth: bool - Signal Big Mouth is Open and Current Bar is in Big Teeth
  
  
  Returns:
  pd.DataFrame - the dataframe with the Big Mouth Flag Signals added
  """
  if add_current_bar_is_in_big_teeth:
    __add_current_bar_is_in_big_teeth(df)
  if add_big_mouth_is_open_and_current_bar_is_in_big_lips:
    __add_big_mouth_is_open_and_current_bar_is_in_big_lips(df)
  if add_mouth_is_open_and_current_bar_is_in_big_teeth:
    __add_mouth_is_open_and_current_bar_is_in_big_teeth(df)













from mlconstants import CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME
def __add_current_bar_is_in_tide_teeth(df):
  """
  Add the Current Bar Is In Big Teeth Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Current Bar Is In Big Teeth Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Current Bar Is In Big Teeth Flag added
  """
  df[CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME] = (df[TTEETH] > df[TJAW]) & (df[TTEETH] > df[TLIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df

#__add_tide_mouth_is_open_and_current_bar_is_in_tide_lips(df)
from mlconstants import TIDE_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_LIPS_COLNAME
def __add_tide_mouth_is_open_and_current_bar_is_in_tide_lips(df):
  """
  Add the Big Mouth Is Open and Current Bar Is In Big Lips Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Big Mouth Is Open and Current Bar Is In Big Lips Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Big Mouth Is Open and Current Bar Is In Big Lips Flag added
  """
  df[TIDE_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_LIPS_COLNAME] = (df[TJAW] > df[TTEETH]) & (df[TJAW] > df[TLIPS])#GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df

#__add_mouth_is_open_and_current_bar_is_in_tide_teeth(df)
from mlconstants import MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME
def __add_mouth_is_open_and_current_bar_is_in_tide_teeth(df):
  """
  Add the Mouth Is Open and Current Bar Is In Big Teeth Flag to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Mouth Is Open and Current Bar Is In Big Teeth Flag to
  
  Returns:
  pd.DataFrame - the dataframe with the Mouth Is Open and Current Bar Is In Big Teeth Flag added
  """
  df[MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME] = (df[TLIPS] > df[TTEETH]) & (df[TLIPS] > df[TJAW]) #GENERATED
  raise NotImplementedError(_NOT_VALIDATED__SEE_RAISED_MESSAGE)
  return df



def _add_tide_mouth_flag_signals(df,
                    add_current_bar_is_in_tide_teeth=True,
                    add_tide_mouth_is_open_and_current_bar_is_in_tide_lips=True,
                    add_mouth_is_open_and_current_bar_is_in_tide_teeth=True):
  """
  Add the tide Mouth Flag Signals to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the tide Mouth Flag Signals to
  add_current_bar_is_in_tide_teeth: bool - Signal current bar is in tide Teeth
  add_tide_mouth_is_open_and_current_bar_is_in_tide_lips: bool - Signal tide Mouth is Open and Current Bar is in tide Lips
  add_mouth_is_open_and_current_bar_is_in_tide_teeth: bool - Signal tide Mouth is Open and Current Bar is in tide Teeth
  
  
  Returns:
  pd.DataFrame - the dataframe with the tide Mouth Flag Signals added
  """
  if add_current_bar_is_in_tide_teeth:
    __add_current_bar_is_in_tide_teeth(df)
  if add_tide_mouth_is_open_and_current_bar_is_in_tide_lips:
    __add_tide_mouth_is_open_and_current_bar_is_in_tide_lips(df)
  if add_mouth_is_open_and_current_bar_is_in_tide_teeth:
    __add_mouth_is_open_and_current_bar_is_in_tide_teeth(df)












_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE = 'Not implemented yet.  See: pto_240706_patterning_helper.ipynb,pto_240706_patterning_helper_C02.ipynb,pto_240706_patterning_helper_C03.ipynb,pto_240706_patterning_helper_C04.ipynb,pto_240706_patterning_helper_C04b.ipynb,pto_240706__validation_240709.ipynb'
def _add_mfis_lag_feature(df):
  """
  Add the MFI Lag Feature to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the MFI Lag Feature to
  
  Returns:
  pd.DataFrame - the dataframe with the MFI Lag Feature added
  """
  raise NotImplementedError(_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE)

def _add_zone_lag_feature(df):
  """
  Add the Zone Lag Feature to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the Zone Lag Feature to
  
  Returns:
  pd.DataFrame - the dataframe with the Zone Lag Feature added
  """
  raise NotImplementedError(_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE)

def _add_ao_above_bellow_peaks_lag_feature(df):
  """
  Add the AO Above Bellow Peaks Lag Feature to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the AO Above Bellow Peaks Lag Feature to
  
  Returns:
  pd.DataFrame - the dataframe with the AO Above Bellow Peaks Lag Feature added
  """
  raise NotImplementedError(_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE)

def _add_ao_lag_feature(df):
  """
  Add the AO Lag Feature to the dataframe.
  
  Parameters:
  df: pd.DataFrame - the dataframe to add the AO Lag Feature to
  
  Returns:
  pd.DataFrame - the dataframe with the AO Lag Feature added
  """
  raise NotImplementedError(_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE)


def _get_data_for_instrument_timeframe(i,t,
                                       use_full=True,force_refresh=False,):
  """
  Get the data for the instrument and timeframe.
  
  Parameters:
  i: str - the instrument
  t: str - the timeframe
  use_full: bool - use the full data or not
  force_refresh: bool - force a refresh of the data or not
  
  Returns:
  pd.DataFrame - the data for the instrument and timeframe
  """
  from realityhelper import _load_ttf_data
  df=_load_ttf_data(i, t, use_full)
  raise NotImplementedError(_PTO_2407_NOT_IMPLEMENTED__or_JUST_LINKED_TO_CODE__MESSAGE)
  
def create_mlf_data__STUB(i,
                          t,
                          use_full=True,
                          force_refresh=False,
                          add_mfis_lag_feature=True,
                          add_zone_lag_feature=True,
                          add_ao_above_bellow_peaks_lag_feature=True,
                          add_ao_lag_feature=True,
                          add_normal_mouth_is_open=True,
                          add_current_bar_is_out_of_normal_mouth=True,
                          add_current_bar_is_in_big_teeth=True,
                          add_big_mouth_is_open_and_current_bar_is_in_big_lips=True,
                          add_mouth_is_open_and_current_bar_is_in_big_teeth=True,
                          add_current_bar_is_in_tide_teeth=True,
                          add_tide_mouth_is_open_and_current_bar_is_in_tide_lips=True,
                          add_mouth_is_open_and_current_bar_is_in_tide_teeth=True,
                    ):
  """
  Wrap all the creation we've been doing in the prototyping sessions. (2407) - See: pto_240706_patterning_helper.ipynb,pto_240706_patterning_helper_C02.ipynb,pto_240706_patterning_helper_C03.ipynb,pto_240706_patterning_helper_C04.ipynb,pto_240706_patterning_helper_C04b.ipynb,pto_240706__validation_240709.ipynb, $jgtml/samples/jgtml_obsds_240515_SIGNALS.result.csv
  
  Parameters:
  i: str - the instrument
  t: str - the timeframe
  use_full: bool - use the full data or not
  add_mfis_lag_feature: bool - add the mfi lag feature or not
  add_zone_lag_feature: bool - add the zone lag feature or not
  add_ao_above_bellow_peaks_lag_feature: bool - add the ao above bellow peaks lag feature or not
  add_ao_lag_feature: bool - add the ao lag feature or not (CURRENTLY IMPLEMENTED in the add_mfis_lag_feature)
  add_normal_mouth_is_open: bool - Add flag to output that tells if the normal alligator mouth is Open
  add_current_bar_is_out_of_normal_mouth: bool - Signal Out of the Normal Alligator Mouth
  add_current_bar_is_in_big_teeth: bool - Signal current bar is in Big Teeth
  add_big_mouth_is_open_and_current_bar_is_in_big_lips: bool - Signal Big Mouth is Open and Current Bar is in Big Lips
  add_mouth_is_open_and_current_bar_is_in_big_teeth: bool - Signal Big Mouth is Open and Current Bar is in Big Teeth
  add_current_bar_is_in_tide_teeth: bool - Signal current bar is in Tide Teeth
  add_tide_mouth_is_open_and_current_bar_is_in_tide_lips: bool - Signal Tide Mouth is Open and Current Bar is in Tide Lips
  add_mouth_is_open_and_current_bar_is_in_tide_teeth: bool - Signal Tide Mouth is Open and Current Bar is in Tide Teeth
  """
  df=_get_data_for_instrument_timeframe(i,t,use_full=use_full,force_refresh=force_refresh)
  
  if add_mfis_lag_feature:
    _add_mfis_lag_feature(df)
  if add_zone_lag_feature:
    _add_zone_lag_feature(df)
  if add_ao_above_bellow_peaks_lag_feature:
    _add_ao_above_bellow_peaks_lag_feature(df)
  if add_ao_lag_feature:
    _add_ao_lag_feature(df)
  
  
  _add_normal_alligator_flag_signals(df,add_normal_mouth_is_open=add_normal_mouth_is_open,
                    add_current_bar_is_out_of_normal_mouth=add_current_bar_is_out_of_normal_mouth)
    
  
  _add_big_mouth_flag_signals(df,
                    add_current_bar_is_in_big_teeth=add_current_bar_is_in_big_teeth,
                    add_big_mouth_is_open_and_current_bar_is_in_big_lips=add_big_mouth_is_open_and_current_bar_is_in_big_lips,
                    add_mouth_is_open_and_current_bar_is_in_big_teeth=add_mouth_is_open_and_current_bar_is_in_big_teeth)
  
  
  
  _add_tide_mouth_flag_signals(df,
                    add_current_bar_is_in_tide_teeth=add_current_bar_is_in_tide_teeth,
                    add_tide_mouth_is_open_and_current_bar_is_in_tide_lips=add_tide_mouth_is_open_and_current_bar_is_in_tide_lips,
                    add_mouth_is_open_and_current_bar_is_in_tide_teeth=add_mouth_is_open_and_current_bar_is_in_tide_teeth)
  raise NotImplementedError('Not implemented yet.  See: pto_240706_patterning_helper.ipynb,pto_240706_patterning_helper_C02.ipynb,pto_240706_patterning_helper_C03.ipynb,pto_240706_patterning_helper_C04.ipynb,pto_240706_patterning_helper_C04b.ipynb,pto_240706__validation_240709.ipynb')
  pass

  