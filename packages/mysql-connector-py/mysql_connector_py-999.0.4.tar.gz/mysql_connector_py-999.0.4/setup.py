from setuptools import setup, find_packages
import os
import pathlib
import re
import shutil
import sys

from setuptools import Extension, find_packages, setup
GITHUB_URL = "https://github.com/mysql/mysql-connector-python"
METADATA_FILES = (
    "README.txt",
    "README.rst",
    "LICENSE.txt",
    "CHANGES.txt",
    "CONTRIBUTING.md",
    "SECURITY.md",
)
VERSION = "999.0.4"

def get_long_description() -> str:
    """Extracts a long description from the README.rst file that is suited for this specific package.
    """
    with open(pathlib.Path(os.getcwd(), "README.rst")) as file_handle:
        # The README.rst text is meant to be shared by both mysql and mysqlx packages, so after getting it we need to
        # parse it in order to remove the bits of text that are not meaningful for this package (mysql)
        long_description = file_handle.read()
    block_matches = re.finditer(
        pattern=(
            r'(?P<module_start>\.{2}\s+={2,}\s+(?P<module_tag>\<(?P<module_name>mysql|mysqlx|both)\>)(?P<repls>\s+'
            r'\[(?:(?:,\s*)?(?:repl(?:-mysql(?:x)?)?)\("(?:[^"]+)",\s*"(?:[^"]*)"\))+\])?\s+={2,})'
            r'(?P<block_text>.+?(?=\.{2}\s+={2,}))(?P<module_end>\.{2}\s+={2,}\s+\</(?P=module_name)\>\s+={2,})'
        ),
        string=long_description,
        flags=re.DOTALL)
    for block_match in block_matches:
        if block_match.group("module_name") == 'mysqlx':
            long_description = long_description.replace(block_match.group(), "")
        else:
            block_text = block_match.group("block_text")
            if block_match.group("repls"):
                repl_matches = re.finditer(pattern=r'(?P<repl_name>repl(?:-mysql(?:x)?)?)\("'
                                                   r'(?P<repl_source>[^"]+)",\s*"(?P<repl_target>[^"]*)"\)+',
                                           string=block_match.group("repls"))
                for repl_match in repl_matches:
                    repl_name = repl_match.group("repl_name")
                    repl_source = repl_match.group("repl_source")
                    repl_target = repl_match.group("repl_target")
                    if repl_target is None:
                        repl_target = ""
                    if repl_name == "repl" or repl_name.endswith("mysql"):
                        block_text = block_text.replace(repl_source, repl_target)
            long_description = long_description.replace(block_match.group(), block_text)
    # Make replacements for files that are directly accessible within GitHub but not within PyPI
    files_regex_fragment = "|".join(mf.replace(".", r"\.") for mf in METADATA_FILES)
    long_description = re.sub(pattern=rf"\<(?P<file_name>{files_regex_fragment})\>",
                              repl=f"<{GITHUB_URL}/blob/trunk/\g<file_name>>",
                              string=long_description)
    return long_description


setup(
    name="mysql-connector-py",  # ******** yourname! *** ** PyPI
    version=VERSION,
    author="OracleForks",
    author_email="your.email@example.com",
    description=(
            "A self-contained Python driver for communicating with MySQL "
            "servers, using an API that is compliant with the Python "
            "Database API Specification v2.0 (PEP 249)."
        ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/oracle/mysql-connector-py", # URL ****** ***********
    license="GNU GPLv2 (with FOSS License Exception)",
        keywords=[
            "mysql",
            "database",
            "db",
            "connector",
            "driver",
        ],
        project_urls={
            "Homepage": "https://dev.mysql.com/doc/connector-python/en/",
            "Documentation": "https://dev.mysql.com/doc/connector-python/en/",
            "Downloads": "https://dev.mysql.com/downloads/connector/python/",
            "Release Notes": "https://dev.mysql.com/doc/relnotes/connector-python/en/",
            "Bug System": "https://bugs.mysql.com/",
            "Slack": "https://mysqlcommunity.slack.com/messages/connectors",
            "Forums": "https://forums.mysql.com/list.php?50",
            "Blog": "https://blogs.oracle.com/mysql/",
        },
        packages=find_packages(exclude=["tests*"]), # ************* ******* *** ****** (***** * __init__.py),
    install_requires=[
        "mysql-connector-python>=8.0.0,<9.0.0", # **** ***********
        # ******** ****** *********** *****, **** *****
    ],
    classifiers=[
        # ******:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License", # *********, *** ********* * ****** LICENSE
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7", # *********** ****** Python
)
