from __future__ import print_function, division

import os
import glob

import pytest

from ..avm import AVM, NoSpatialInformation

ROOT = os.path.dirname(os.path.abspath(__file__))

XML_FILES = glob.glob(os.path.join(ROOT, 'data', '*.xml'))


@pytest.mark.parametrize('filename', XML_FILES)
def test_parse(filename):
    AVM.from_xml_file(filename)


@pytest.mark.parametrize('filename', XML_FILES)
def test_to_xml(filename):
    a = AVM.from_xml_file(filename)
    a.to_xml()


@pytest.mark.parametrize('filename', XML_FILES)
def test_to_xmp(filename):
    a = AVM.from_xml_file(filename)
    a.to_xmp()


NO_WCS = [os.path.join(ROOT, 'data', 'heic0409a.xml'),
          os.path.join(ROOT, 'data', 'sig05-021-alpha.xml'),
          os.path.join(ROOT, 'data', 'ssc2004-06a1-alpha.xml'),
          os.path.join(ROOT, 'data', 'ssc2004-06b1-alpha.xml')]

XML_FILES_WCS = [x for x in XML_FILES if x not in NO_WCS]


@pytest.mark.parametrize('filename', XML_FILES_WCS)
def test_to_wcs(filename):
    pytest.importorskip('astropy')
    a = AVM.from_xml_file(filename)
    a.to_wcs()


@pytest.mark.parametrize('filename', XML_FILES_WCS)
def test_to_wcs_target_image(filename, tmpdir):
    pytest.importorskip('PIL')
    pytest.importorskip('astropy')
    from PIL import Image
    image = Image.frombytes(data=b"1111", size=(2, 2), mode="L")
    image_file = tmpdir.join('test.png').strpath
    image.save(image_file)
    image.close()
    a = AVM.from_xml_file(filename)
    a.Spatial.ReferenceDimension = (30, 30)
    a.to_wcs(target_image=image_file)


@pytest.mark.parametrize('filename', XML_FILES_WCS)
def test_to_wcs_target_shape(filename, tmpdir):
    pytest.importorskip('PIL')
    pytest.importorskip('astropy')
    a = AVM.from_xml_file(filename)
    a.Spatial.ReferenceDimension = (30, 30)
    a.to_wcs(target_shape=(2, 2))


@pytest.mark.parametrize('filename', NO_WCS)
def test_to_wcs_nowcs(filename):
    pytest.importorskip('astropy')
    a = AVM.from_xml_file(filename)
    with pytest.raises(NoSpatialInformation):
        a.to_wcs()
