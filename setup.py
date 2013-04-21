#!/usr/bin/env python

from distutils.core import setup

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py

version = '0.9.1'

setup(name='PyAVM',
      version=version,
      description='Simple pure-python AVM meta-data handling',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='MIT',
      url='http://astrofrog.github.io/pyavm/',
      packages=['pyavm', 'pyavm.tests'],
      package_data={'pyavm.tests':['data/*.xml', 'data/*.hdr']},
      provides=['pyavm'],
      cmdclass={'build_py': build_py},
      keywords=['Scientific/Engineering'],
      long_description="PyAVM is a module to represent, read, and write metadata following the `Astronomy Visualization Metadata <http://www.virtualastronomy.org/avm_metadata.php>`_ (AVM) standard.",
      classifiers=[
      "Development Status :: 4 - Beta",
      "Programming Language :: Python",
      "License :: OSI Approved :: MIT License",
      ],
      )
