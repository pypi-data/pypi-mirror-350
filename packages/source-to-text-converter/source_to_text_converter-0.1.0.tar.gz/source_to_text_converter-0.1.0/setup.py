from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="source-to-text-converter",
    version="0.1.0",
    author="fisamy",
    author_email="SourceToTextConverter@fisamy.work",
    description="A tool to convert source code to text or docx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fisamy/source-to-text-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "gitpython",
        "python-docx",
    ],
    entry_points={
        'console_scripts': [
            'source-to-text-converter=source_to_text_converter:main',
        ],
    },
)