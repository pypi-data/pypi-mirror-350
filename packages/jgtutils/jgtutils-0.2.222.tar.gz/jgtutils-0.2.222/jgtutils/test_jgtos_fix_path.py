import unittest
from jgtos import fix_path_ext

class TestFixPathExt(unittest.TestCase):
    def test_fix_path_ext(self):
        # Test case 1: Existing extension is replaced with the desired extension
        fpath = "path/to/file.csv.csv"
        ext = "csv"
        expected_result = "path/to/file.csv"
        result = fix_path_ext(ext, fpath)
        self.assertEqual(result, expected_result)

        # Test case 2: Existing extension is replaced with the desired extension (with multiple dots in the file name)
        fpath = "path/to/file.name.csv"
        ext = "csv"
        expected_result = "path/to/file.name.csv"
        result = fix_path_ext(ext, fpath)
        self.assertEqual(result, expected_result)

        # Test case 3: Existing extension is replaced with the desired extension (with no existing extension)
        fpath = "path/to/file"
        ext = "csv"
        expected_result = "path/to/file.csv"
        result = fix_path_ext(ext, fpath)
        self.assertEqual(result, expected_result)

        # Test case 4: Existing extension is replaced with the desired extension (with no existing extension and multiple dots in the file name)
        fpath = "path/to/file.name"
        ext = "csv"
        expected_result = "path/to/file.name.csv"
        result = fix_path_ext(ext, fpath)
        self.assertEqual(result, expected_result)

        # Test case 5: Existing extension is replaced with the desired extension (with existing extension different from the desired extension)
        fpath = "path/to/file.txt"
        ext = "txt"
        expected_result = "path/to/file.txt"
        result = fix_path_ext(ext, fpath)
        self.assertEqual(result, expected_result)

        # # Test case 6: Existing extension is replaced with the desired extension (with existing extension same as the desired extension)
        fpath = "path/to/file"
        ext = None
        exception_message=f"No extension found in the file path: {fpath}"
        with self.assertRaises(Exception) as context:
            result = fix_path_ext(ext, fpath)
        self.assertEqual(exception_message, str(context.exception))
          
          

if __name__ == '__main__':
    unittest.main()