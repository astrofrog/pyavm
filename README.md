PyAVM provides the ``AVM()`` class to represent [AVM](http://www.virtualastronomy.org/avm_metadata.php) meta-data:

    >>> from pyavm import AVM

To parse AVM meta-data from an existing file, simply create an instance of this class using the filename of the image (or any file-like object):

    >>> avm = AVM('myexample.jpg')

Then, you can view the contents by using

    >>> print avm

or

    >>> avm

The AVM meta-data can be accessed using the attribute notation:

    >>> avm.Spatial.Equinox
    'J2000'

    >>> avm.Publisher
    'Chandra X-ray Observatory'

It is also possible to initialize an AVM object using a pywcs.WCS instance:

    >>> import pyfits
    >>> import pywcs
    >>> from pyavm import AVM
    >>> wcs = pywcs.WCS(pyfits.getheader('image.fits'))
    >>> avm = AVM(wcs)

Finally, it is possible to embed AVM meta-data into an image file:

    >>> avm.embed('original_image.jpg', 'tagged_image.jpg')

At this time, only JPG and PNG files are supported for embedding.