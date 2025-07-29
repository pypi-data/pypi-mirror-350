import unittest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
from jgtml.SignalOrderingHelper import create_fdb_entry_order



"""
The Last two rows of the CSV file:
2024-08-21 10:00:00,0.91687,0.91728,0.91635,0.91691,0.91696,0.91735,0.91642,0.91698,3348,0.916915,0.917315,0.916385,0.916945,0.91685,-0.04131217738,-0.16660641799,0.91789748219,0.91834963993,0.91826803675,0.90710133862,0.91091454742,0.91403437288,0.91014196311,0.90620074471,0.90529160356,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02777777778,1,0,1,0,1,0.0,0.0,0.0,red,-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,1,2,-+
2024-08-21 11:00:00,0.91691,0.91692,0.91646,0.9166,0.91698,0.91699,0.91655,0.91667,1667,0.916945,0.916955,0.916505,0.916635,0.91673,-0.07513993595,-0.18265915233,0.9179434451,0.91833030994,0.9180054294,0.90717694156,0.91103191928,0.91418247956,0.9101070839,0.90620436812,0.90530824173,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02699460108,0,0,0,0,1,0.0,0.0,0.0,red,-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,1,0,3,--
AUD-CAD_H1_cds_cache_24081918.csv
"""

class TestSignalOrderingHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Read the CSV file
        df = pd.read_csv('tests/fdb_data/AUD-CAD_H1_cds_cache_24082107.csv')

        # Extract signal_bar and current_bar
        cls.signal_bar = df.iloc[0].to_dict()
        cls.current_bar = df.iloc[1].to_dict()

    @patch('jgtml.SignalOrderingHelper.datetime')
    def test_create_fdb_entry_order_invalid_due_to_valid_gator(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 8, 21, 11, 0, 0)
        
        result = create_fdb_entry_order(
            i="AUD/CAD",
            signal_bar=self.signal_bar,
            current_bar=self.current_bar,
            lots=1,
            tick_shift=2,
            quiet=True,
            valid_gator_mouth_open_in_mouth=True,
            validate_signal_out_of_mouth=True,
            t="H1",
            validation_timestamp=datetime.now(),
            verbose_level=0
        )
        
        self.assertIsNone(result, "Expected the order to be invalid due to valid_gator")

if __name__ == "__main__":
    unittest.main()