import unittest
import tempfile
import shutil
import os
import json
from jgtcommon import load_settings

class TestLoadSettings(unittest.TestCase):
  #just run the load_settings function
  def test_load_settings(self):
    settings=load_settings()
    self.assertTrue(settings is not None)

if __name__ == '__main__':
    unittest.main()