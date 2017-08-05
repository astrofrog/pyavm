import os
import pytest

from ..avm import AVM

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def test_from_image_jpg():
    avm = AVM.from_image(os.path.join(ROOT, 'eso_eso1723a_320.jpg'))
    assert avm.ID == 'eso1723a'


def test_from_image_png():
    avm = AVM.from_image(os.path.join(ROOT, 'eso_eso1723a_320.png'))
    assert avm.ID == 'eso1723a'


def test_from_image_other(tmpdir):
    # Here we test the brute-force search
    with open(os.path.join(ROOT, '3c321.avm.xml'), 'rb') as f:
        content = f.read()
    filename = tmpdir.join('testfile').strpath
    with open(filename, 'wb') as f:
        f.write(b'<?xpacket begin="<\ufeff>" id="W5M0MpCehiHzreSzNTczkc9d"?>')
        f.write(content)
        f.write(b'</x:xmpmeta>')
    avm = AVM.from_image(filename)
    assert avm.Publisher == 'Chandra X-ray Observatory'


def test_from_wcs_cd():
    pytest.importorskip('astropy')
    pytest.importorskip('numpy')
    import numpy as np
    from astropy.wcs import WCS
    scale = np.array([[-1.5, 0], [0, 2.5]])
    theta = np.radians(60)
    rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    cd = np.matmul(rotation, scale)
    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN']
    wcs.wcs.cd = cd
    avm = AVM.from_wcs(wcs)
    np.testing.assert_allclose(avm.Spatial.Scale, [-1.5, 2.5])
    np.testing.assert_allclose(avm.Spatial.Rotation, 60)
