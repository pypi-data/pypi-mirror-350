# -*- coding: utf-8 -*-

from sys import version_info

from setuptools import setup, find_packages

__version__ = '1.0.2'  # 版本号1.0.2
requirements = open('requirements.txt').readlines()  # 依赖文件

if version_info < (3, 8, 0):
    raise SystemExit('Sorry! caplib requires python 3.8.0 or later.')

setup(
    name='caplib',
    description='',
    long_description='',
    license='',
    version=__version__,
    author='caprisktech.com',
    url='',
    packages=find_packages(exclude=["test"]),
    python_requires='>= 3.8.0',
    install_requires=requirements
)
