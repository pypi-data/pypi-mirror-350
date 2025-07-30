#!/usr/bin/env python

from io import open

from setuptools import setup

"""
:authors: Karim Muzafarov
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 Karim Muzafarov
"""

version = '1.0.3'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elasticsearch_tools',
    version=version,

    author='Karim90403',
    author_email='karim90403@gmail.ru',

    description=(
        u'Python module for working with elasticsearch, create queries and connections '
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Karim90403/elasticsearch-tools/',
    download_url='https://github.com/Karim90403/elasticsearch-tools/archive/refs/heads/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['elasticsearch_tools'],
    install_requires=['elasticsearch'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)