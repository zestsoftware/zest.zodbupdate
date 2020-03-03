# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    version="1.0.0b1",
    # thanks to this bug on Python 2.7
    # https://github.com/pypa/setuptools/issues/1136
    # we need one line in here.
    # setuptools 41.7.1 seems to fix it, but we may not want to depend on it.
    package_dir={"": "src"},
)
