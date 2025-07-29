# -*- coding: utf-8 -*-
"""
Created on 23/5/2025 at 11:42
Author: Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Company: Intelligentica
"""
from setuptools import setup, find_packages

setup(
    name="routex",  # Must be unique on PyPI
    version="0.1.0",
    author="Abdelouahed Ben Mhamed",
    author_email="abdelouahed.benmhamed@um6p.ma",
    description="A Python toolkit for generating routing problem instances",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/INTELLIGENTICA/RouteX",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "scipy"  # List your dependencies
    ],
)