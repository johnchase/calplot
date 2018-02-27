#!/usr/bin/env python

from setuptools import find_packages, setup
from glob import glob
__version__ = "0.0.0"

setup(name='calplot',
      author="John Chase",
      author_email="chasejohnh@gmail.com",
      version=__version__,
      packages=find_packages(),
      scripts=glob("scripts/*")
      )
