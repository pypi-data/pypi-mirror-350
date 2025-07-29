# test_pncli.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the path to the module
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pncli

class TestPncli(unittest.TestCase):

    @patch('pncli._parse_args')
    @patch('pncli.pndata__get_all_patterns')
    @patch('pncli.pndata__write_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list_with_htf')
    def test_main_list_patterns(self, mock_read_with_htf, mock_read, mock_write, mock_get_all_patterns, mock_parse_args):
        # Mock arguments
        mock_args = MagicMock()
        mock_args.list_patterns = True
        mock_args.json_output = False
        mock_args.markdown_output = False
        mock_parse_args.return_value = mock_args

        # Mock function return values
        mock_get_all_patterns.return_value = "Pattern List"

        # Run main
        with patch('builtins.print') as mock_print:
            pncli.main()
            mock_print.assert_called_with("Pattern List")

    @patch('pncli._parse_args')
    @patch('pncli.pndata__write_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list_with_htf')
    def test_main_read_columns_list(self, mock_read_with_htf, mock_read, mock_write, mock_parse_args):
        # Mock arguments
        mock_args = MagicMock()
        mock_args.list_patterns = False
        mock_args.json_output = False
        mock_args.markdown_output = False
        mock_args.columns_list_from_higher_tf = None
        mock_args.flag_columns_were_read = False
        mock_args.timeframe = "-"
        mock_args.patternname = "test_pattern"
        mock_parse_args.return_value = mock_args

        # Mock function return values
        mock_read.return_value = ["col1", "col2"]

        # Run main
        with patch('builtins.print') as mock_print:
            pncli.main()
            mock_print.assert_called_with("Columns List from Pattern:", ["col1", "col2"])

    @patch('pncli._parse_args')
    @patch('pncli.pndata__write_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list_with_htf')
    def test_main_read_columns_list_with_timeframe(self, mock_read_with_htf, mock_read, mock_write, mock_parse_args):
        # Mock arguments
        mock_args = MagicMock()
        mock_args.list_patterns = False
        mock_args.json_output = False
        mock_args.markdown_output = False
        mock_args.columns_list_from_higher_tf = None
        mock_args.flag_columns_were_read = False
        mock_args.timeframe = "D1"
        mock_args.patternname = "test_pattern"
        mock_parse_args.return_value = mock_args

        # Mock function return values
        mock_read_with_htf.return_value = ["col1", "col2"]

        # Run main
        with patch('builtins.print') as mock_print:
            pncli.main()
            mock_print.assert_called_with("Columns List from Pattern:", ["col1", "col2"])

    @patch('pncli._parse_args')
    @patch('pncli.pndata__write_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list')
    @patch('pncli.pndata__read_new_pattern_columns_list_with_htf')
    def test_main_write_new_pattern_columns_list(self, mock_read_with_htf, mock_read, mock_write, mock_parse_args):
        # Mock arguments
        mock_args = MagicMock()
        mock_args.list_patterns = False
        mock_args.json_output = False
        mock_args.markdown_output = False
        mock_args.columns_list_from_higher_tf = ["col1", "col2"]
        mock_args.flag_columns_were_read = False
        mock_args.timeframe = "-"
        mock_args.patternname = "test_pattern"
        mock_parse_args.return_value = mock_args

        # Run main
        pncli.main()
        mock_write.assert_called_with(columns_list_from_higher_tf=["col1", "col2"], pn="test_pattern")

if __name__ == '__main__':
    unittest.main()