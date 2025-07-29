#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: Keker-dev
:license: MIT License, see LICENSE file

:copyright: (c) 2025 Keker-dev
"""

version = '1.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fear_module',
    version=version,

    author='Keker',
    author_email='timaiv112008@gmail.com',

    description=(
        u'Python module for making fear apps '
        u'Fear Application'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Keker-dev/fear_module',
    download_url='https://github.com/Keker-dev/fear_module/archive/main.zip',

    license="MIT License, see LICENSE file",

    packages=['fear_module'],
    install_requires=['comtypes', 'keyboard', 'pillow', 'psutil', 'pycaw', 'pygame', 'pyperclip'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
