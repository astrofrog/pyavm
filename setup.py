#!/usr/bin/env python

from setuptools import setup

version = '0.9.3.dev0'

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(name='PyAVM',
      version=version,
      description='Simple pure-python AVM meta-data handling',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='MIT',
      url='http://astrofrog.github.io/pyavm/',
      packages=['pyavm', 'pyavm.tests'],
      package_data={'pyavm.tests': ['data/*.xml', 'data/*.hdr']},
      provides=['pyavm'],
      keywords=['Scientific/Engineering'],
      long_description=LONG_DESCRIPTION,
      classifiers=[
      "Development Status :: 4 - Beta",
      "Programming Language :: Python",
      "License :: OSI Approved :: MIT License",
      ],
      )
