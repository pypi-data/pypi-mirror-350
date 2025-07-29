# source-to-text-converter

A utility tool to convert the content of software codebases (local or GitHub) into a single structured text or .docx file for easy analysis, documentation, or processing.

## Features

- Supports local directories and GitHub repositories as input.
- Preserves folder structure in the output.
- Outputs consolidated content as plain text or .docx.
- Option to exclude hidden files and directories.
- Verbose mode for detailed processing logs.
- File type filtering by extension.
- Robust error handling and cleanup.

## Installation

```bash
pip install source-to-text-converter
```

## Usage

### CLI

```bash
source-to-text-converter --input <input_path_or_url> --output <output_file> [options]
```

Options:

- `--input` (required): Local directory path or GitHub repo URL.
- `--output` (required): Output file path.
- `--output-type` (optional): `txt` (default) or `docx`.
- `--exclude-hidden` (optional): Exclude hidden files and directories.
- `--include-ext` (optional): Comma-separated list of file extensions to include (e.g., `.py,.js`).
- `--verbose` (optional): Show detailed logs.

### Python API

```python
from source_to_text_converter.source_to_text_converter import SourceToTextConverter

converter = SourceToTextConverter(
    input_path="/path/to/repo",
    output_path="output.txt",
    output_type="txt",
    exclude_hidden=True,
    include_exts=[".py", ".js"],
    verbose=True
)
converter.get_file()
```

## License

Apache License 2.0
