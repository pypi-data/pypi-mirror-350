'''
Description:  
Author: Huang J
Date: 2025-05-26 10:33:14
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = "webseer"
DESCRIPTION = "Webseer 是一个语义驱动的网络情报者，根据用户定义的关注点，从互联网上主动搜集并结构化相关信息。与传统爬虫不同，Webseer 以目标为导向地探索网络，理解内容、追踪语义，而不是盲目抓取所有链接。"
URL = "https://github.com/AgBigdataLab/Webseer"
EMAIL = "hjie97bi@gmail.com"
AUTHOR = "Jie Huang"
REQUIRES_PYTHON = ">=3.10.0"
VERSION = "0.1.3"

REQUIRED = [
    "transformers>=4.51.3",
    "chunk-factory==0.1.5",
    "fake_useragent>=2.2.0",
    "playwright>=1.52.0",
    "numpy==1.26.4",
    "pymysql==1.1.1",
    "json_repair>=0.44.1",
    "validators>=0.35.0",
    "langdetect>=1.0.9"
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION
    
class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Pushing git tags…")
        os.system("git push --tags")

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()
        
        
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    url=URL,
    packages=find_packages(),
    keywords = ['python','windows','mac','linux','Webseer','crawl','scraper','LLM','playwright'],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Jupyter",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: Unix"
    ],
    cmdclass={"upload": UploadCommand},
)