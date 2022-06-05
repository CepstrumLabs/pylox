# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('VERSION') as f:
    version = f.read()

setup(
    name='pylox',
    version=version,
    description='LOX implementation in python',
    long_description=readme,
    author='Michael Karotsieris',
    author_email='michael.karotsieris@gmail.com',
    url='https://github.com/CepstrumLabs/pylox',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
