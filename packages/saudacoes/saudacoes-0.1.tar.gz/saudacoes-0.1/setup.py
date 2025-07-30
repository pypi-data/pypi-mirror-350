# -*- coding: utf-8 -*-
"""
Created on Tue May 27 14:26:06 2025

@author: anari
"""

from setuptools import setup, find_packages

setup(
    name='saudacoes',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Teu Nome',
    description='Um pacote de exemplo com mensagens de saudação.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
