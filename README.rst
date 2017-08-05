|Build Status| |Coverage Status|

About
-----

PyAVM is a module to represent, read, and write metadata following the
`*Astronomy Visualization
Metadata* <http://www.virtualastronomy.org/avm_metadata.php>`__ (AVM)
standard.

Requirements
------------

PyAVM supports Python 2.7 and 3.5+. No other dependencies are needed
simply to read and embed AVM meta-data.

However, the following optional dependencies are needed for more
advanced functionality:

-  `Numpy <http://www.numpy.org>`__ 1.10 or later
-  `Astropy <http://www.astropy.org>`__ to handle WCS objects and FITS
   headers
-  `py.test <http://www.pytest.org>`__ and
   `PIL <http://www.pythonware.com/products/pil/>`__ for tests

Installing and Reporting issues
-------------------------------

PyAVM can be installed with pip::

    pip install pyavm

Please report any issues you encounter via the `issue
tracker <https://github.com/astrofrog/pyavm/issues>`__ on GitHub.

Using PyAVM
-----------

Importing
~~~~~~~~~

PyAVM provides the ``AVM`` class to represent AVM meta-data, and is
imported as follows:

.. code:: python

    >>> from pyavm import AVM

Parsing files
~~~~~~~~~~~~~

To parse AVM meta-data from an existing image, simply call the
``from_image`` class method using the filename of the image (or any
file-like object):

.. code:: python

    >>> avm = AVM.from_image('myexample.jpg')

Only JPEG and PNG files are properly supported in that the parsing
follows the JPEG and PNG specification. For other file formats, PyAVM
will simply scan the contents of the file, looking for an XMP packet.
This method is less reliable, but should work in most real-life cases.

Accessing and setting the meta-data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can view the contents of the AVM object by using

.. code:: python

    >>> print(avm)

The AVM meta-data can be accessed using the attribute notation:

.. code:: python

    >>> avm.Spatial.Equinox
    'J2000'
    >>> avm.Publisher
    'Chandra X-ray Observatory'

Tags can be modified:

.. code:: python

    >>> avm.Spatial.Equinox = "B1950"
    >>> avm.Spatial.Notes = "The WCS information was updated on 04/02/2010"

Creating an AVM object from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an empty AVM meta-data holder, simply call ``AVM()`` without
any arguments:

.. code:: python

    >>> avm = AVM()

Note that this will create an AVM object following the 1.2
specification. If necessary, you can specify which version of the
standard to use:

.. code:: python

    >>> avm = AVM(version=1.1)

Converting to a WCS object
~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to create an Astropy WCS object from the AVM meta-data:

.. code:: python

    >>> wcs = avm.to_wcs()

By default, ``Spatial.FITSheader`` will be used if available, but if
not, the WCS information is extracted from the other ``Spatial.*`` tags.
To force PyAVM to not try ``Spatial.FITSheader``, use:

.. code:: python

    >>> wcs = avm.to_wcs(use_full_header=False)

Initializing from a FITS header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an AVM meta-data object from a FITS header, simply pass the
header (as an Astropy Header instance) to the ``from_header`` class
method:

.. code:: python

    >>> from astropy.io import fits
    >>> header = fits.getheader('image.fits')
    >>> avm = AVM.from_header(header)

By default, the AVM tag ``Spatial.FITSheader`` will be created,
containing the full header (in addition to the other ``Spatial.*``
tags). This can be disabled with:

.. code:: python

    >>> avm = AVM.from_header(header, include_full_header=False)

Initializing from a WCS object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly, it is possible to create an AVM meta-data object from an
Astropy WCS instance:

.. code:: python

    >>> from astropy.wcs import WCS
    >>> from pyavm import AVM
    >>> wcs = WCS('image.fits')
    >>> avm = AVM.from_wcs(wcs)

Tagging images with AVM meta-data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to embed AVM meta-data into an image file:

.. code:: python

    >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

At this time, only JPG and PNG files are supported for embedding.

.. |Build Status| image:: https://travis-ci.org/astrofrog/pyavm.svg?branch=master
   :target: https://travis-ci.org/astrofrog/pyavm
.. |Coverage Status| image:: https://coveralls.io/repos/astrofrog/pyavm/badge.svg?branch=master
   :target: https://coveralls.io/r/astrofrog/pyavm?branch=master
