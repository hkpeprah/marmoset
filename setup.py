import os
import sys
import marmoset

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Marmoset",
    version=marmoset.__version__,
    author=marmoset.__author__,
    author_email="user@example.com",
    packages=['marmoset', 'marmoset.core'],
    scripts=['bin/marmoset'],
    url="http://example.com",
    license='LICENSE.txt',
    description="Command-line interface for the UofW Marmoset Submission Server",
    long_description=marmoset.__description__,
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
        "mechanize == 0.2.5",
    ],
)

    
