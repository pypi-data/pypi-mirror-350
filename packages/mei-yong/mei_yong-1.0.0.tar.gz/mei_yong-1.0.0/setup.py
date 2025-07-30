#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.txt", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='mei_yong',
    version='1.0.0',
    description='没用的计算器',
    long_description=long_description,
    long_description_content_type='text/plain',
    author='LGZM',
    author_email='lgzm666666@outlook.com',
    install_requires=[],
    license='GPLv3',
    packages=find_packages(include=['mei_yong', 'mei_yong.*']),
    entry_points={
        'console_scripts': [
            'mei_yong = mei_yong.cli:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Disassemblers',
    ],
    python_requires='>=3.6',
)
