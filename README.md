About
-----

PyAVM is a module to represent, read, and write metadata following the [*Astronomy Visualization Metadata*](http://www.virtualastronomy.org/) (AVM) standard.

Requirements
------------

PyAVM supports Python 2.6, 2.7, 3.1, 3.2, and 3.3. No other dependencies are
needed simply to access AVM data from PNG and JPEG images.

However, the following optional dependencies are needed for more advanced
functionality:

* [Astropy](http://www.astropy.org) to handle WCS objects and FITS headers
* [py.test](http://www.pytest.org) and
  [PIL](http://www.pythonware.com/products/pil/) for tests

Installing and Reporting issues
-------------------------------

To install PyAVM, you can simply do:

    pip install pyavm

if you have ``pip`` installed. Otherwise, download the [latest tar file](https://pypi.python.org/pypi/PyAVM/), then install using:

    tar xvzf PyAVM-x.x.x.tar.gz
    cd PyAVM-x.x.x
    python setup.py install

Please report any issues you encounter via the [issue tracker](https://github.com/astrofrog/pyavm/issues) on GitHub.

Using PyAVM
-----------

### Importing

PyAVM provides the ``AVM`` class to represent AVM meta-data, and is imported as follows:

    >>> from pyavm import AVM

### Parsing files

To parse AVM meta-data from an existing file, simply call the ``from_image`` class method using the filename of the image (or any file-like object):

    >>> avm = AVM.from_image('myexample.jpg')

### Accessing and setting the meta-data

You can view the contents of the AVM object by using

    >>> print(avm)

The AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'
    >>> avm.Publisher
    'Chandra X-ray Observatory'

Tags can be modified:

    >>> avm.Spatial.Equinox = "B1950"
    >>> avm.Spatial.Notes = "The WCS information was updated on 04/02/2010"

### Creating an AVM object from scratch

To create an empty AVM meta-data holder, simply call ``AVM()`` without any
arguments:

    >>> avm = AVM()

Note that this will create an AVM object following the 1.2 specification. If necessary, you can specify which version of the standard to use:

    >>> avm = AVM(version=1.1)

### Converting to a WCS object

It is possible to create an Astropy WCS object from the AVM meta-data:

    >>> wcs = avm.to_wcs()

By default, ``Spatial.FITSheader`` will be used if available, but if not, the WCS
information is extracted from the other ``Spatial.*`` tags. To force PyAVM to not
try ``Spatial.FITSheader``, use:

    >>> wcs = avm.to_wcs(use_full_header=False)

### Initializing from a FITS header

To create an AVM meta-data object from a FITS header, simply pass the header
(as an Astropy Header instance) to the ``from_header`` class method:

    >>> from astropy.io import fits
    >>> header = fits.getheader('image.fits')
    >>> avm = AVM.from_header(header)

By default, the AVM tag ``Spatial.FITSheader`` will be created, containing the
full header (in addition to the other ``Spatial.*`` tags). This can be
disabled with:

    >>> avm = AVM.from_header(header, include_full_header=False)

### Initializing from a WCS object

Similarly, it is possible to create an AVM meta-data object from an Astropy WCS instance:

    >>> from astropy.wcs import WCS
    >>> from pyavm import AVM
    >>> wcs = WCS('image.fits')
    >>> avm = AVM.from_wcs(wcs)

### Tagging images with AVM meta-data

It is possible to embed AVM meta-data into an image file:

    >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

At this time, only JPG and PNG files are supported.