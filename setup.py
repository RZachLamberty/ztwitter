#!/usr/bin/env python
from setuptools import setup

setup(
    name='ztwitter',
    version='1.0.0',
    description='Twitter api wrappers',
    include_package_data=True,
    author='Zach Lamberty',
    author_email='r.zach.lamberty@gmail.com',
    url='https://github.com/RZachLamberty/',
    packages=['ztwitter'],
    install_requires=[
        'pyyaml',
        'requests',
        'requests_oauthlib'
    ]
)
