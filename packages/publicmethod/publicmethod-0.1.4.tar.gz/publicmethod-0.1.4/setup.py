#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
仅用于兼容旧版本pip的安装桥接文件。
对于现代Python包，推荐使用pyproject.toml。
"""

from setuptools import setup

setup(
    name="publicmethod",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
) 