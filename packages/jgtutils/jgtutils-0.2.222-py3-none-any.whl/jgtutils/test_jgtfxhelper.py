
import unittest
from unittest.mock import patch
from jgtfxhelper import mkfn_cfxdata_filepath

class TestMkfnCfxdataFilepath(unittest.TestCase):
    @patch('jgtfxhelper.mkfn_cdata_filepath')
    def test_mkfn_cfxdata_filepath_use_local(self, mock_mkfn_cdata_filepath):
        mock_mkfn_cdata_filepath.return_value = '/data/jgt/filename.txt'
        result = mkfn_cfxdata_filepath('filename.txt.txt', use_local=True,ext='txt')
        self.assertEqual(result, '/data/jgt/filename.txt')


    @patch('jgtfxhelper.get_data_path')
    def test_mkfn_cfxdata_filepath_not_use_local(self, mock_get_data_path):
        mock_get_data_path.return_value = '/data'
        result = mkfn_cfxdata_filepath('filename.txt', use_local=False)
        self.assertEqual(result, '/data/filename.txt')

if __name__ == '__main__':
    unittest.main()