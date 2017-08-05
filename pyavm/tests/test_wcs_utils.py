from itertools import product
import pytest

pytest.importorskip('numpy')
pytest.importorskip('astropy')

import numpy as np
from astropy.wcs import WCS

from ..wcs_utils import get_cdelt_crota

SCALES = [(0.4, 0.5),
          (-0.2, 0.9),
          (0.2, -0.5),
          (-0.4, -4.3)]

ROTATIONS = np.linspace(0, 330, 12)


@pytest.mark.parametrize(('scale', 'rotation'), product(SCALES, ROTATIONS))
def test_get_cdelt_crota(scale, rotation):

    scale_matrix = np.array([[scale[0], 0], [0, scale[1]]])
    theta = np.radians(rotation)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    cd = np.matmul(rotation_matrix, scale_matrix)

    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN']
    wcs.wcs.cd = cd

    cdelt1, cdelt2, crota2 = get_cdelt_crota(wcs)

    try:
        np.testing.assert_allclose(crota2, rotation)
        np.testing.assert_allclose(cdelt1, scale[0])
        np.testing.assert_allclose(cdelt2, scale[1])
    except AssertionError:
        np.testing.assert_allclose(crota2 + 180, rotation)
        np.testing.assert_allclose(cdelt1, -scale[0])
        np.testing.assert_allclose(cdelt2, -scale[1])
