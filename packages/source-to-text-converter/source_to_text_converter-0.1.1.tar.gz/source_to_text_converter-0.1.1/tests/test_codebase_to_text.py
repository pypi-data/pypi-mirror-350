import os
import tempfile
import unittest
from codebase_to_text import CodebaseToText
from io import StringIO
import sys
from docx import Document
from unittest import mock
import git
from tests.base_test import BaseTest
import builtins

class TestCodebaseToText(BaseTest):
    def setUp(self):
        # Create a temporary directory with some test files
        super().setUp()
        self.file1_path = os.path.join(self.test_dir.name, "file1.py")
        self.file2_path = os.path.join(self.test_dir.name, "file2.txt")
        self.hidden_file_path = os.path.join(self.test_dir.name, ".hiddenfile")
        with open(self.file1_path, "w") as f:
            f.write("print('Hello World')")
        with open(self.file2_path, "w") as f:
            f.write("This is a text file.")
        with open(self.hidden_file_path, "w") as f:
            f.write("Hidden content")

    def get_file_contents_section(self, content):
        file_contents_start = content.find("File Contents")
        return content[file_contents_start:]

    def test_local_directory_txt_output(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            include_exts=None
        )
        converter.get_file()
        with open(self.output_file.name, "r") as f:
            content = f.read()
        self.assertIn("file1.py", content)
        self.assertIn("file2.txt", content)
        self.assertIn("print('Hello World')", content)
        self.assertIn("This is a text file.", content)

    def test_exclude_hidden_files(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=False,
            exclude_hidden=True
        )
        converter.get_file()
        with open(self.output_file.name, "r") as f:
            content = f.read()
        # Only check the File Contents section for hidden files exclusion
        file_contents = self.get_file_contents_section(content)
        self.assertNotIn(".hiddenfile", file_contents)
        self.assertNotIn("Hidden content", file_contents)

    def test_include_ext_filter(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=False,
            exclude_hidden=False,
            include_exts=[".py"]
        )
        converter.get_file()
        with open(self.output_file.name, "r") as f:
            content = f.read()
        # Only check the File Contents section for extension filter
        file_contents = self.get_file_contents_section(content)
        self.assertIn("file1.py", file_contents)
        self.assertIn("print('Hello World')", file_contents)
        self.assertNotIn("file2.txt", file_contents)

    def test_invalid_output_type(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="invalid",
            verbose=False,
            exclude_hidden=False,
            include_exts=None
        )
        with self.assertRaises(ValueError):
            converter.get_file()

    def test_docx_output(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="docx",
            verbose=False,
            exclude_hidden=False,
            include_exts=None
        )
        converter.get_file()
        doc = Document(self.output_file.name)
        texts = [p.text for p in doc.paragraphs]
        self.assertIn("Folder Structure", texts)
        self.assertTrue(any("file1.py" in t for t in texts))
        self.assertTrue(any("print('Hello World')" in t for t in texts))

    def test_verbose_output(self):
        converter = CodebaseToText(
            input_path=self.test_dir.name,
            output_path=self.output_file.name,
            output_type="txt",
            verbose=True,
            exclude_hidden=False,
            include_exts=None
        )
        with self.assertLogs(level='DEBUG') as log:
            converter.get_file()
        self.assertTrue(any("Processing:" in message for message in log.output))

    @mock.patch('codebase_to_text.git.Repo.clone_from')
    def test_github_repo_clone_success(self, mock_clone):
        mock_clone.return_value = None
        converter = CodebaseToText(
            input_path="https://github.com/user/repo.git",
            output_path=self.output_file.name,
            output_type="txt",
            verbose=True,
            exclude_hidden=False,
            include_exts=None
        )
        with mock.patch('codebase_to_text.tempfile.mkdtemp') as mock_mkdtemp:
            mock_mkdtemp.return_value = "/fake/temp/dir"
            with mock.patch.object(converter, '_parse_folder', return_value="folder structure"):
                with mock.patch.object(converter, '_process_files', return_value="file contents"):
                    converter.get_file()
        mock_clone.assert_called_once_with("https://github.com/user/repo.git", "/fake/temp/dir")

    @mock.patch('codebase_to_text.git.Repo.clone_from', side_effect=Exception("Clone failed"))
    def test_github_repo_clone_failure(self, mock_clone):
        converter = CodebaseToText(
            input_path="https://github.com/user/repo.git",
            output_path=self.output_file.name,
            output_type="txt",
            verbose=True,
            exclude_hidden=False,
            include_exts=None
        )
        with self.assertRaises(Exception) as cm:
            converter.get_file()
        self.assertIn("Clone failed", str(cm.exception))

    def test_file_read_error_handling(self):
        # Mock open to raise an exception when reading file1.py
        def open_side_effect(file_path, *args, **kwargs):
            if file_path == self.file1_path:
                raise IOError("Error reading file")
            return original_open(file_path, *args, **kwargs)

        original_open = builtins.open
        with mock.patch("builtins.open", side_effect=open_side_effect):
            with self.assertLogs('source_to_text_converter.source_to_text_converter', level='WARNING') as log:
                converter = CodebaseToText(
                    input_path=self.test_dir.name,
                    output_path=self.output_file.name,
                    output_type="txt",
                    verbose=False,
                    exclude_hidden=False,
                    include_exts=None
                )
                converter.get_file()
                self.assertTrue(any("Error reading file" in message for message in log.output))

if __name__ == "__main__":
    unittest.main()
