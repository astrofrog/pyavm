from __future__ import print_function, division

try:
    unicode
except:
    basestring = unicode = str

import os
import pytest

pytest.importorskip('astropy')

from astropy.io import fits
from astropy.wcs import WCS

from ..avm import AVM, NoSpatialInformation

ROOT = os.path.dirname(os.path.abspath(__file__))


def test_from_header():
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = AVM.from_header(header)
    assert isinstance(a.Spatial.FITSheader, basestring)
    assert a.Spatial.FITSheader == header
    # assert a.Spatial.Equinox == 2000.  # returns NaN at the moment
    assert a.Spatial.CoordsystemProjection == 'CAR'
    assert a.Spatial.ReferenceDimension[0] == 599
    assert a.Spatial.ReferenceDimension[1] == 599
    assert a.Spatial.ReferenceValue[0] == 0.
    assert a.Spatial.ReferenceValue[1] == 0.
    assert a.Spatial.ReferencePixel[0] == 299.628
    assert a.Spatial.ReferencePixel[1] == 299.394
    assert a.Spatial.Scale[0] == -0.001666666707
    assert a.Spatial.Scale[1] == +0.001666666707
    assert a.Spatial.Quality == 'Full'


def test_from_header_cd():
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    header['CD1_1'] = header.pop('CDELT1')
    header['CD2_2'] = header.pop('CDELT2')
    a = AVM.from_header(header)
    assert isinstance(a.Spatial.FITSheader, basestring)
    assert a.Spatial.FITSheader == header
    # assert a.Spatial.Equinox == 2000.  # returns NaN at the moment
    assert a.Spatial.CoordsystemProjection == 'CAR'
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
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = AVM.from_header(header)
    b = AVM.from_wcs(a.to_wcs(), shape=(header['NAXIS2'], header['NAXIS1']))
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
    header = fits.Header.fromtextfile(os.path.join(ROOT, 'data', 'example_header.hdr'))
    a = WCS(header)
    b = AVM.from_wcs(a).to_wcs()
    # assert a.wcs.equinox == b.wcs.equinox
    assert a.wcs.ctype[0] == b.wcs.ctype[0]
    assert a.wcs.ctype[1] == b.wcs.ctype[1]
    assert a.wcs.crval[0] == b.wcs.crval[0]
    assert a.wcs.crval[1] == b.wcs.crval[1]
    assert a.wcs.crpix[0] == b.wcs.crpix[0]
    assert a.wcs.crpix[1] == b.wcs.crpix[1]
    assert a.wcs.cdelt[0] == b.wcs.cdelt[0]
    assert a.wcs.cdelt[1] == b.wcs.cdelt[1]
    assert a.wcs.crota[0] == b.wcs.crota[0]
    assert a.wcs.crota[1] == b.wcs.crota[1]
    assert a.wcs.radesys == b.wcs.radesys
