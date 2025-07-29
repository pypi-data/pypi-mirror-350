#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'chibi>=0.5.5', 'chibi_hybrid>=0.0.1', 'chibi-atlas>=1.1.0',
    'chibi_requests>=1.2.0' ]

setup(
    author="Dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Utilities',
    ],
    description="run terminal commands",
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_command',
    name='chibi_command',
    packages=find_packages(include=['chibi_command', 'chibi_command.*']),
    url='https://github.com/dem4ply/chibi_command',
    version='2.1.1',
    zip_safe=False,
)
