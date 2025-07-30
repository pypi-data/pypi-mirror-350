import sys
from shutil import rmtree
from pathlib import Path
from setuptools import setup, Command

HERE = Path(__file__).parent
README = (HERE.joinpath("readme.md")).read_text()

setup(
    name="mkdocs-suppress-logs-plugin",
    version="0.1.1",
    packages=["mkdocs_suppress_logs_plugin"],
    url="https://github.com/darrelk/mkdocs-suppress-logs-plugin",
    license="MIT",
    author="darrelk",
    author_email="darrelkley@gmail.com",
    description="MkDocs plugin to suppress unwanted log messages using pattern matching.",
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={
        "mkdocs.plugins": [
            "suppress_logs = mkdocs_suppress_logs_plugin:SuppressLogsPlugin"
        ]
    },
    install_requires=["mkdocs>=1.1"],
    python_requires='>=3.7',
)
