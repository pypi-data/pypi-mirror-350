import os
import tempfile
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.output_file = tempfile.NamedTemporaryFile(delete=False)
        self.output_file.close()

    def tearDown(self):
        self.test_dir.cleanup()
        if os.path.exists(self.output_file.name):
            os.remove(self.output_file.name)