# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages
from os.path import join, dirname
import pyss
import unittest

setup(    
    name='pyss',
    version=pyss.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=[
        'matplotlib==2.0.2'
        #,'Flask==0.8'
    ],
    include_package_data=True,
    test_suite='discover_tests',    
)
