#!/usr/bin/env python
from setuptools import setup

# See setup.cfg for configuration.
setup(
    package_data={
        'jsslib': ['libjsslib.dylib', 'libjsslib.so', 'jsslib.dll', 'jsslib.py', 'base.lex'],
    }
)

