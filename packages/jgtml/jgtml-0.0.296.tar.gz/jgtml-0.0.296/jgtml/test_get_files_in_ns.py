import unittest
from unittest.mock import patch
import os
from mlutils import get_list_of_files_in_ns

class TestGetListOfFilesInNs(unittest.TestCase):

    @patch('mlutils.get_basedir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_multiple_files(self, mock_isfile, mock_listdir, mock_get_basedir):
        mock_get_basedir.return_value = '/fake/dir'
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'dir1']
        mock_isfile.side_effect = lambda x: not x.endswith('dir1')
        
        result = get_list_of_files_in_ns(True, 'pn')
        self.assertEqual(result, ['file1.txt', 'file2.txt'])

    @patch('mlutils.get_basedir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_no_files(self, mock_isfile, mock_listdir, mock_get_basedir):
        mock_get_basedir.return_value = '/fake/dir'
        mock_listdir.return_value = []
        mock_isfile.side_effect = lambda x: False
        
        result = get_list_of_files_in_ns(True, 'pn')
        self.assertEqual(result, [])

    @patch('mlutils.get_basedir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_mix_files_and_directories(self, mock_isfile, mock_listdir, mock_get_basedir):
        mock_get_basedir.return_value = '/fake/dir'
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'dir1', 'file3.txt']
        mock_isfile.side_effect = lambda x: not x.endswith('dir1')
        
        result = get_list_of_files_in_ns(True, 'pn')
        self.assertEqual(result, ['file1.txt', 'file2.txt', 'file3.txt'])

if __name__ == '__main__':
    unittest.main()