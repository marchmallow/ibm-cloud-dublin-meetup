#!/usr/bin/env python

# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup, find_packages

desc = 'Demo service for posting tasks to redis.'

setup(
    name='demo-flask',
    version='0.1.19',
    description=('Demo push to redis'),
    long_description=desc,
    url='https://github.ibm.com/fd4b-agrotech/demo-flask',
    author='FD4B Prod',
    author_email='fd4bprod@us.ibm.com',
    license='Apache v2',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=[
        'Flask==1.0.2',
        'WTForms==2.2.1',
        'redis==2.10.6'
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'demo-flask = flaskform.__main__:main'
        ],
    },
)
