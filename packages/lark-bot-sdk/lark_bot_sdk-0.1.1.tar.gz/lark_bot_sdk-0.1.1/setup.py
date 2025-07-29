#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lark_bot_sdk',
    version='0.1.1',
    description='飞书机器人消息SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feishu SDK Developer',
    author_email='example@example.com',
    url='https://github.com/yourusername/feishusdk',
    packages=find_packages(include=['lark_bot_sdk']),
    install_requires=[
        'lark_oapi>=1.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    keywords='feishu, lark, bot, sdk',
)
