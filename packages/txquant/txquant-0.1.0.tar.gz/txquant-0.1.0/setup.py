# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README.md文件
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="txquant",
    version="0.1.0",
    packages=find_packages(),
    author="95ge",
    author_email="445646258@qq.com",
    description="天行量化，一个量化回测框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/95ge/txquant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
    install_requires=[
        'LTtx',
        'pyzmq',
        'requests',
        'pandas',
        'pandas_market_calendars',
        'cnlunar',
    ],
) 