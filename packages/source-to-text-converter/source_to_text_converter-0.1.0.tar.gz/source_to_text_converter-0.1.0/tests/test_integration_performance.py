import os
import tempfile
import unittest
from codebase_to_text import CodebaseToText
import time
import shutil

class TestIntegrationPerformance(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for large file simulation
        self.test_dir = tempfile.TemporaryDirectory()
        self.output_file = tempfile.NamedTemporaryFile(delete=False)
        self.output_file.close()

    def tearDown(self):
        self.test_dir.cleanup()
        if os.path.exists(self.output_file.name):
            os.remove(self.output_file.name)

    def test_large_number_of_files(self):
        # Create a large number of small files
        num_files = 1000
        for i in range(num_files):
            file_path = os.path.join(self.test_dir.name, f"file_{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"This is file number {i}")

        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            include_exts=None
        )
        start_time = time.time()
        converter.get_file()
        duration = time.time() - start_time
        self.assertTrue(duration < 30, f"Processing took too long: {duration} seconds")

        with open(self.output_file.name, "r") as f:
            content = f.read()
        # Check some files are included in output
        self.assertIn("file_0.txt", content)
        self.assertIn("file_999.txt", content)

    def test_github_repo_integration(self):
        # Use a small public GitHub repo for testing
        github_url = "https://github.com/octocat/Hello-World.git"
        converter = CodebaseToText(
            input_path=github_url,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=True,
            exclude_hidden=False,
            include_exts=None
        )
        converter.get_file()

        with open(self.output_file.name, "r") as f:
            content = f.read()
        # Check for known file or folder names in the repo
        self.assertIn("README", content)
        self.assertIn("Hello-World", content)

if __name__ == "__main__":
    unittest.main()
