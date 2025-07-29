import os
import tempfile
import unittest
from codebase_to_text import CodebaseToText
import time
import shutil
from tests.base_test import BaseTest

class TestIntegrationPerformance(BaseTest):
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
        self.assertTrue(duration < 10, f"Processing took too long: {duration} seconds")

    def test_github_repo_integration(self):
        # Use a small public GitHub repo for testing
        github_url = "https://github.com/octocat/Hello-World.git"
        converter = CodebaseToText(
            input_path=github_url,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=True,
            exclude_hidden=True,
            include_exts=None
        )
        converter.get_file()

        with open(self.output_file.name, "r") as f:
            content = f.read()
        # Check for known file or folder names in the repo
        self.assertIn("README", content)
        # Assert that .git related content is excluded
        self.assertNotIn(".git/config", content)
        self.assertNotIn(".git/HEAD", content)
        self.assertNotIn(".gitignore", content)
        # Check for content of a known file
        self.assertIn("Hello World!", content)

if __name__ == "__main__":
    unittest.main()
