#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Zzz(1309458652@qq.com)
# Description:

from setuptools import setup, find_packages

setup(
    name = 'key_musicz',
    version = '0.1.0',
    keywords='key_musicz',
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    description = "键盘弹钢琴，keyboard to play piano",
    license = 'Apache License 2.0',
    url = 'https://github.com/buildCodeZ/key_musicz',
    author = 'Zzz',
    author_email = '1309458652@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['pynput', 'numpy', 'PyAudio','buildz','pyfluidsynth'],
)
