#!/usr/bin/env python

from distutils.core import setup

version = '0.1.3'

setup(name='PyAVM',
      version=version,
      description='Simple pure-python AVM meta-data parsing',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='MIT',
      url='https://github.com/astrofrog/pyavm',
      download_url='https://github.com/downloads/astrofrog/pyavm/PyAVM-%s.tar.gz' % version,
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
