import unittest
from unittest.mock import patch
from jgtml.SignalOrderingHelper import valid_gator,is_bar_out_of_mouth,is_mouth_open

import pandas as pd

#The Last two rows of the CSV file:
AUDCAD_H1_24082111_CSV_ROWS="""
2024-08-21 10:00:00,0.91687,0.91728,0.91635,0.91691,0.91696,0.91735,0.91642,0.91698,3348,0.916915,0.917315,0.916385,0.916945,0.91685,-0.04131217738,-0.16660641799,0.91789748219,0.91834963993,0.91826803675,0.90710133862,0.91091454742,0.91403437288,0.91014196311,0.90620074471,0.90529160356,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02777777778,1,0,1,0,1,0.0,0.0,0.0,red,-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,1,2,-+
2024-08-21 11:00:00,0.91691,0.91692,0.91646,0.9166,0.91698,0.91699,0.91655,0.91667,1667,0.916945,0.916955,0.916505,0.916635,0.91673,-0.07513993595,-0.18265915233,0.9179434451,0.91833030994,0.9180054294,0.90717694156,0.91103191928,0.91418247956,0.9101070839,0.90620436812,0.90530824173,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02699460108,0,0,0,0,1,0.0,0.0,0.0,red,-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,1,0,3,--

"""
from SOHelper import get_last_two_bars,get_bar_at_index

AUD_CAD_H1_cds_cache_24081918_mouth_open_sell_no_ao_divergence="AUD-CAD_H1_cds_cache_24081918_mouth_open_sell_no_ao_divergence.csv"

EUR_JPY_H1_cds_cache_240821="EUR-JPY_H1_cds_cache__24082112.csv"

mouth_closed_samples=[
  {
    "fn":EUR_JPY_H1_cds_cache_240821,
    "date_from":"2024-08-21 05:00:00",
    "expected":False
  },
  {
    "fn":EUR_JPY_H1_cds_cache_240821,
    "date_from":"2024-08-20 23:00:00",
    "direction":"S",
    "expected":True
  },
  {
    "fn":"NZD-CAD_m15_2408291352_mouth_no_yet_open.csv",
    "date_from":"2024-08-29 17:45:00",
    "direction":"B",
    "expected":True
  }]

fdb_samples=[
  {
    "fn":EUR_JPY_H1_cds_cache_240821,
    "date_from":"2024-08-20 23:00:00",
    "expected":True
  }]

_FDB_DIR="tests/fdb_data"#

class TestCDSBase(unittest.TestCase):
  def read_last_two_bars(self, fn):
      data=self._read_cds_df(fn)
      last_bar_completed,current_bar = get_last_two_bars(data)
      return last_bar_completed,current_bar

  def __mksamplepath(self,fn):
    return f"{_FDB_DIR}/{fn}"
  
  def _read_cds_df(self,fn):
    fpath=self.__mksamplepath(fn)
    data=pd.read_csv(fpath,index_col=0,parse_dates=True)
    return data
  
  def _read_cds_df_from_dt(self,fn,date_from):
    data=self._read_cds_df(fn)
    filtered_data = data.loc[:date_from]
    return filtered_data
  
  def getbars_from_date_from(self,fn,date_from):
    data=self._read_cds_df_from_dt(fn,date_from)
    last_bar_completed,current_bar = get_last_two_bars(data)
    return last_bar_completed,current_bar
  
  def getbars_sample_mouth_closed(self,index = 0):    
    sample=mouth_closed_samples[index]
    fn=sample["fn"]
    date_from=sample["date_from"]
    expected=sample["expected"]
    last_bar_completed,current_bar=self.getbars_from_date_from(fn,date_from)
    return last_bar_completed,current_bar
  
  def _getbars_mouth_is_open_sell__240821(self)->{dict,dict}:
    fn = AUD_CAD_H1_cds_cache_24081918_mouth_open_sell_no_ao_divergence
    last_bar_completed:dict=None;current_bar:dict=None
    last_bar_completed,current_bar=self.read_last_two_bars(fn)
    return last_bar_completed,current_bar
  
class TestValidGator(TestCDSBase):

  def test_is_mouth_open_sell_returns_true(self):
    #fn = AUD_CAD_H1_cds_cache_24081918_mouth_open_sell_no_ao_divergence
    last_bar_completed:dict=None;current_bar:dict=None
    last_bar_completed,current_bar=self._getbars_mouth_is_open_sell__240821()#self.read_last_two_bars(fn)
    bar_is_open_result=is_mouth_open(last_bar_completed,"S")
    self.assertTrue(bar_is_open_result)
    
    last_bar_completed,current_bar=self.getbars_sample_mouth_closed(1)
    bar_is_open_result=is_mouth_open(last_bar_completed,"S")    
    self.assertTrue(bar_is_open_result)
    
    
    # last_bar_completed,current_bar=self.getbars_sample_mouth_closed(2)
    # bar_is_open_result=is_mouth_open(last_bar_completed,"B")    
    # self.assertTrue(not bar_is_open_result)
     
  def test_just_read_signal_bar(self):
    #last_bar_completed,current_bar=self.getbars_sample_mouth_closed(0)
    #2024-08-21 05:00:00
    #csv_row="2024-08-21 05:00:00,161.973,162.109,161.798,161.949,161.982,162.115,161.808,161.956,23391,161.9775,162.112,161.803,161.9525,161.9575,-0.08813831458,0.16262604882,162.05949208356,161.81334755481,161.70897286942,161.98782405994,162.14974848394,162.39240577169,167.78448679655,164.04704230017,162.06170393055,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.32102090548,0,1,-1,0,1,0.0,0.0,0.0,green,1.0,0.0,1.0,0.0,0.0,0.0,0.0,0,0,0,0,1,0,0,0,1,+-"
    #csv_header="Date,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose,Volume,Open,High,Low,Close,Median,ao,ac,jaw,teeth,lips,bjaw,bteeth,blips,tjaw,tteeth,tlips,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,mfi,fdbb,fdbs,fdb,aoaz,aobz,zlc,zlcb,zlcs,zcol,zone_sig,sz,bz,acs,acb,ss,sb,price_peak_above,price_peak_bellow,ao_peak_above,ao_peak_bellow,mfi_sq,mfi_green,mfi_fade,mfi_fake,mfi_sig,mfi_str"
    #csv_data=csv_header+"\n"+csv_row
    data = self._read_cds_df("just_read_bar_sample.csv")
    validation_bar=get_bar_at_index(data,-1)
    validation_date = pd.to_datetime(validation_bar["Date"], format='%Y-%m-%d %H:%M:%S')
    self.assertEqual(validation_date,"2024-08-21 05:00:00")
    
    
    
  def test_is_mouth_open_buy_returns_false(self):
    last_bar_completed,current_bar=self._getbars_mouth_is_open_sell__240821()
    bar_is_open_result=is_mouth_open(last_bar_completed,"B")
    self.assertFalse(bar_is_open_result)
    
    #2nd sample
    last_bar_completed,current_bar=self.getbars_sample_mouth_closed(0)
    bar_is_open_result=is_mouth_open(last_bar_completed,"B")
    
    self.assertFalse(bar_is_open_result)
    
    

  # def read_last_two_bars(self, fn):
  #     data=self._read_cds_df(fn)
  #     last_bar_completed,current_bar = get_last_two_bars(data)
  #     return last_bar_completed,current_bar

  # def _read_cds_df(self,fn):
  #   data=pd.read_csv(fn,index_col=0,parse_dates=True)
  #   return data
  
  def test_valid_gator_returns_true(self):
    
    #data=pd.read_csv(pd.compat.StringIO(AUDCAD_H1_24082111_CSV_ROWS),header=None)
    data = pd.read_csv('tests/fdb_data/AUD-CAD_H1_cds_cache_24082107.csv')
    
    
    last_bar_completed,current_bar = get_last_two_bars(data)
    
    bs = "B"

    result = valid_gator(last_bar_completed, current_bar, bs)

    self.assertTrue(result)

  def test_valid_gator_returns_false(self):
    last_bar_completed = {
      'HIGH': 0.91735,
      'LOW': 0.91642,
      'FDB': 0,
      'ASKHIGH': 0.91789748219,
      'BIDLOW': 0.91014196311,
      'JAW': 0.90529160356,
      'TEETH': 0.90529160356,
      'LIPS': 0.90529160356
    }
    current_bar = {
      'HIGH': 0.91698,
      'LOW': 0.91667,
      'FDB': 0,
      'ASKHIGH': 0.9179434451,
      'BIDLOW': 0.9101070839,
      'JAW': 0.90530824173,
      'TEETH': 0.90530824173,
      'LIPS': 0.90530824173
    }
    bs = "S"

    result = valid_gator(last_bar_completed, current_bar, bs)

    self.assertFalse(result)

if __name__ == "__main__":
  unittest.main()