from setuptools import setup, find_packages

# ****** README *** long_description
with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# ****** ****** ** __init__.py ****** ******
# *** ********* ******* ****** * ***** *****
def get_version():
    return "999.0.0"



VERSION = get_version() # ******** ******

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
    long_description=long_description,
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
    packages=find_packages(exclude=["tests*"]), # ************* ******* *** ****** (***** * __init__.py)
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
