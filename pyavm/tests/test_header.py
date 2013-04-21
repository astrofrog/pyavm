from __future__ import print_function, division

try:
    unicode
except:
    basestring = unicode = str

import os
import pytest

from ..avm import AVM, NoSpatialInformation

ROOT = os.path.dirname(os.path.abspath(__file__))


def test_from_header():
    from astropy.io import fits
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = AVM.from_header(header)
    assert isinstance(a.Spatial.FITSheader, basestring)
    assert a.Spatial.FITSheader == header
    # assert a.Spatial.Equinox == 2000.  # returns NaN at the moment
    assert a.Spatial.CoordsystemProjection == b'CAR'
    assert a.Spatial.ReferenceDimension[0] == 599
    assert a.Spatial.ReferenceDimension[1] == 599
    assert a.Spatial.ReferenceValue[0] == 0.
    assert a.Spatial.ReferenceValue[1] == 0.
    assert a.Spatial.ReferencePixel[0] == 299.628
    assert a.Spatial.ReferencePixel[1] == 299.394
    assert a.Spatial.Scale[0] == -0.001666666707
    assert a.Spatial.Scale[1] == +0.001666666707
    assert a.Spatial.Quality == 'Full'


def test_wcs_1():
    from astropy.io import fits
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = AVM.from_header(header)
    b = AVM.from_wcs(a.to_wcs())
    # assert a.Spatial.Equinox == b.Spatial.Equinox  # returns NaN at the moment
    assert a.Spatial.CoordsystemProjection == b.Spatial.CoordsystemProjection
    assert a.Spatial.ReferenceDimension[0] == b.Spatial.ReferenceDimension[0]
    assert a.Spatial.ReferenceDimension[1] == b.Spatial.ReferenceDimension[1]
    assert a.Spatial.ReferenceValue[0] == b.Spatial.ReferenceValue[0]
    assert a.Spatial.ReferenceValue[1] == b.Spatial.ReferenceValue[1]
    assert a.Spatial.ReferencePixel[0] == b.Spatial.ReferencePixel[0]
    assert a.Spatial.ReferencePixel[1] == b.Spatial.ReferencePixel[1]
    assert a.Spatial.Scale[0] == b.Spatial.Scale[0]
    assert a.Spatial.Scale[1] == b.Spatial.Scale[1]
    assert a.Spatial.Quality == b.Spatial.Quality


def test_wcs_2():
    from astropy.io import fits
    from astropy.wcs import WCS
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = WCS(header)
    b = AVM.from_wcs(a).to_wcs()
    # assert a.wcs.equinox == b.wcs.equinox
    assert a.wcs.ctype == b.wcs.ctype
    assert a.wcs.crval == b.wcs.crval
    assert a.wcs.crpix == b.wcs.crpix
    assert a.wcs.cdelt == b.wcs.cdelt
    assert a.wcs.crota == b.wcs.crota
    assert a.wcs.radesys == b.wcs.radesys
