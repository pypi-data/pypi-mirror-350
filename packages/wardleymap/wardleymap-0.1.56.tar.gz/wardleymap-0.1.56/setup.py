"""
This module sets up the 'wardleymap' package for distribution.

The 'wardleymap' package is designed for creating and visualising Wardley Maps,
a type of strategy map that helps businesses understand their value chain
and the landscape in which they operate. Developed by Mark Craddock,
this package provides tools to generate, analyse, and visualize these maps.
"""

from setuptools import setup, find_packages

setup(
    name='wardleymap',
    version='0.1.56',
    author='Mark Craddock',
    author_email='wardley@firstliot.uk',
    description='A Python package to create and visualise Wardley Maps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://wardleymaps.ai/',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'pyvis',
        'networkx',
        'toml',
        'werkzeug',
        'pyyaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
