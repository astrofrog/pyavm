#!/usr/bin/env python

from distutils.core import setup

setup(name='PyAVM',
      version='0.1.2',
      description='Simple pure-python AVM meta-data parsing',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='MIT',
      url='https://github.com/astrofrog/pyavm',
      packages=['pyavm'],
      provides=['pyavm'],
      keywords=['Scientific/Engineering'],
      long_description=open('README.md', 'rb').read(),
      classifiers=[
                   "Development Status :: 3 - Alpha",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
