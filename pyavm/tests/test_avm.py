import os

import pytest

from ..avm import AVM

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_from_image_jpg():
    avm = AVM.from_image(os.path.join(ROOT, "eso_eso1723a_320.jpg"))
    assert avm.ID == "eso1723a"


def test_from_image_png():
    avm = AVM.from_image(os.path.join(ROOT, "eso_eso1723a_320.png"))
    assert avm.ID == "eso1723a"


def test_from_image_other(tmpdir):
    # Here we test the brute-force search
    with open(os.path.join(ROOT, "3c321.avm.xml"), "rb") as f:
        content = f.read()
    filename = tmpdir.join("testfile").strpath
    with open(filename, "wb") as f:
        f.write(b'<?xpacket begin="<\ufeff>" id="W5M0MpCehiHzreSzNTczkc9d"?>')
        f.write(content)
        f.write(b"</x:xmpmeta>")
    avm = AVM.from_image(filename)
    assert avm.Publisher == "Chandra X-ray Observatory"


def test_from_wcs_cd():
    pytest.importorskip("astropy")
    pytest.importorskip("numpy")
    import numpy as np
    from astropy.wcs import WCS

    scale = np.array([[-1.5, 0], [0, 2.5]])
    theta = np.radians(60)
    rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    cd = np.matmul(rotation, scale)
    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    wcs.wcs.cd = cd
    avm = AVM.from_wcs(wcs)
    np.testing.assert_allclose(avm.Spatial.Scale, [-1.5, 2.5])
    np.testing.assert_allclose(avm.Spatial.Rotation, 60)


def test_controlled_vocabulary_dash_placeholder():
    """Test that dash '-' is accepted as a placeholder in controlled vocabulary lists.

    This is a regression test for issue #40.
    """
    avm = AVM()
    # Dash should be accepted as a placeholder for unknown values
    avm.Spectral.ColorAssignment = ["Blue", "Green", "-", "Red", "-"]
    assert avm.Spectral.ColorAssignment == ["Blue", "Green", "-", "Red", "-"]

    avm.Spectral.Band = ["Optical", "-", "Infrared"]
    assert avm.Spectral.Band == ["Optical", "-", "Infrared"]


def test_from_wcs_sip():
    """Test that WCS with SIP distortion extensions are handled correctly.

    This is a regression test for issue #26.
    """
    pytest.importorskip("astropy")
    from astropy.wcs import WCS

    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ["RA---TAN-SIP", "DEC--TAN-SIP"]
    wcs.wcs.crpix = [100, 100]
    wcs.wcs.crval = [180, 45]
    wcs.wcs.cdelt = [-0.001, 0.001]

    avm = AVM.from_wcs(wcs)
    assert avm.Spatial.CoordsystemProjection == "TAN"


def test_nested_attribute_verification():
    """Test that nested attributes are validated against specs.

    This is a regression test for issue #38.
    """
    avm = AVM()

    # Valid nested attribute assignment should work
    avm.Spatial.ReferencePixel = [100.0, 200.0]
    assert avm.Spatial.ReferencePixel == [100.0, 200.0]

    # Invalid type should raise an error
    with pytest.raises(TypeError):
        avm.Spatial.ReferencePixel = "hello world"

    # Invalid attribute name should raise AttributeError
    with pytest.raises(AttributeError):
        avm.Spatial.InvalidAttribute = "test"


def test_avm_iteration():
    """Test that AVM objects can be iterated over.

    This is a regression test for issue #25.
    """
    avm = AVM()
    avm.Title = "Test Image"
    avm.Publisher = "Test Publisher"
    avm.Spatial.Equinox = "J2000"
    avm.Spatial.CoordinateFrame = "ICRS"

    # Test iteration
    tags = dict(avm)
    assert "Title" in tags
    assert tags["Title"] == "Test Image"
    assert "Publisher" in tags
    assert tags["Publisher"] == "Test Publisher"
    assert "Spatial.Equinox" in tags
    assert tags["Spatial.Equinox"] == "J2000"
    assert "Spatial.CoordinateFrame" in tags
    assert tags["Spatial.CoordinateFrame"] == "ICRS"

    # Test len()
    assert len(avm) >= 4  # At least the 4 tags we set

    # Test items()
    items = list(avm.items())
    tag_names = [name for name, value in items]
    assert "Title" in tag_names
    assert "Spatial.Equinox" in tag_names
