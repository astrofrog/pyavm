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
