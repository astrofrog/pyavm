About
=====

PyAVM provides the ``AVM()`` class to represent [AVM](http://www.virtualastronomy.org/avm_metadata.php) meta-data:

    >>> from pyavm import AVM

Parsing files
=============

To parse AVM meta-data from an existing file, simply create an instance of the ``AVM`` class using the filename of the image (or any file-like object):

    >>> avm = AVM('myexample.jpg')

Accessing the meta-data
=======================

You can view the contents of the ``avm`` object by using

    >>> print avm

or

    >>> avm

The AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'

    >>> avm.Publisher
    'Chandra X-ray Observatory'

Converting to a WCS object
==========================

It is possible to create a pywcs.WCS object from the AVM meta-data:

    >>> wcs = avm.to_wcs()

By default, Spatial.FITSheader will be used if available, but if not, the WCS information is extracted from the other Spatial.* tags. To force PyAVM to not try Spatial.FITSheader, use:

    >>> wcs = avm.to_wcs(use_full_header=False)

Initializing from a FITS header
===============================

To create an AVM meta-data object from a FITS header, simply pass the header (as a ``pyfits.Header`` instance) instead of a filename when initializing the ``AVM`` object:

    >>> import pyfits
    >>> header = pyfits.getheader('image.fits')
    >>> avm = AVM(header)

By default, the AVM tag Spatial.FITSheader will be created, containing the full header (in addition to the other Spatial.* keywords). This can be disabled with:

    >>> avm = AVM(header, include_full_header=False)

Initializing from a WCS object
==============================

Similarly, it is possible to create an AVM meta-data object from a ``pywcs.WCS`` instance:

    >>> import pyfits
    >>> import pywcs
    >>> from pyavm import AVM
    >>> wcs = pywcs.WCS(pyfits.getheader('image.fits'))
    >>> avm = AVM(wcs)

Tagging images with AVM meta-data
=================================

It is possible to embed AVM meta-data into an image file:

    >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

At this time, only JPG and PNG files are supported for embedding.