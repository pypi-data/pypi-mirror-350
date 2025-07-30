#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# read long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# setup
setup(
    packages=find_packages(exclude=["tests*", "examples*"]),
)
