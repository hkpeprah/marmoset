import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Marmoset",
    version="1.1.4",
    author="Ford Peprah",
    author_email="user@example.com",
    packages=['marmoset', 'marmoset.core', 'marmoset.utils'],
    scripts=['bin/marmoset'],
    url="http://example.com",
    license='LICENSE.txt',
    description="Command-line interface for the UofW Marmoset Submission Server",
    long_description="",
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
        "mechanize == 0.2.5",
        "keyring == 3.3"
    ],
)

    
