About
=====

PyAVM provides the ``AVM()`` class to represent
[AVM](http://www.virtualastronomy.org/avm_metadata.php) meta-data:

    >>> from pyavm import AVM

Requirements
============

PyAVM supports Python 2.6, 2.7, 3.1, 3.2, and 3.3. No other dependencies are
needed simply to access AVM data from PNG and JPEG images.

However, the following optional dependencies are needed for more advanced
functionality:

* [Astropy](http://www.astropy.org) to handle WCS objects and FITS headers
* [py.test](http://www.pytest.org) and
  [PIL](http://www.pythonware.com/products/pil/) for tests

Installing
==========

To install PyAVM:

    python setup.py install

Parsing files
=============

To parse AVM meta-data from an existing file, simply create an instance of the
``AVM`` class using the filename of the image (or any file-like object):

    >>> avm = AVM('myexample.jpg')

Accessing the meta-data
=======================

You can view the contents of the ``avm`` object by using

    >>> print avm

The AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'

    >>> avm.Publisher
    'Chandra X-ray Observatory'

Creating and Updating tags
==========================

Tags can be modified in place:

    >>> avm.Spatial.Equinox = "B1950"

If the tag does not already exist, it is created.

Tag groups can be created using:

    >>> avm.create_group("Spatial")

after which tags can be created in the group:

    >>> avm.Spatial.Notes = "The WCS information was updated on 04/02/2010"

Creating an AVM object from scratch
===================================

To create an empty AVM meta-data holder, simply call ``AVM()`` without any
arguments:

    >>> avm = AVM()

Converting to a WCS object
==========================

It is possible to create a astropy.wcs.WCS object from the AVM meta-data:

    >>> wcs = avm.to_wcs()

By default, Spatial.FITSheader will be used if available, but if not, the WCS
information is extracted from the other Spatial.* tags. To force PyAVM to not
try Spatial.FITSheader, use:

    >>> wcs = avm.to_wcs(use_full_header=False)

Initializing from a FITS header
===============================

To create an AVM meta-data object from a FITS header, simply pass the header
(as a ``astropy.io.fits.Header`` instance) instead of a filename when
initializing the ``AVM`` object:

    >>> from astropy.io import fits
    >>> header = fits.getheader('image.fits')
    >>> avm = AVM(header)

By default, the AVM tag Spatial.FITSheader will be created, containing the
full header (in addition to the other Spatial.* keywords). This can be
disabled with:

    >>> avm = AVM(header, include_full_header=False)

Initializing from a WCS object
==============================

Similarly, it is possible to create an AVM meta-data object from a
``astropy.wcs.WCS`` instance:

    >>> from astropy.wcs import WCS
    >>> from pyavm import AVM
    >>> wcs = WCS('image.fits')
    >>> avm = AVM(wcs)

Tagging images with AVM meta-data
=================================

It is possible to embed AVM meta-data into an image file:

    >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

At this time, only JPG and PNG files are supported.