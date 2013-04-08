import os
import glob

import pytest

from ..avm import AVM, NoSpatialInformation

ROOT = os.path.dirname(os.path.abspath(__file__))

XML_FILES = glob.glob(os.path.join(ROOT, 'data', '*.xml'))


@pytest.mark.parametrize('filename', XML_FILES)
def test_parse(filename):
    a = AVM()
    a.from_xml_file(filename)


@pytest.mark.parametrize('filename', XML_FILES)
def test_to_xml(filename):
    a = AVM()
    a.from_xml_file(filename)
    a.to_xml()


@pytest.mark.parametrize('filename', XML_FILES)
def test_to_xmp(filename):
    a = AVM()
    a.from_xml_file(filename)
    a.to_xmp()


NO_WCS = [os.path.join(ROOT, 'data', 'heic0409a.xml'),
          os.path.join(ROOT, 'data', 'sig05-021-alpha.xml'),
          os.path.join(ROOT, 'data', 'ssc2004-06a1-alpha.xml'),
          os.path.join(ROOT, 'data', 'ssc2004-06b1-alpha.xml')]

XML_FILES_WCS = [x for x in XML_FILES if x not in NO_WCS]


@pytest.mark.parametrize('filename', XML_FILES_WCS)
def test_to_wcs(filename):
    a = AVM()
    a.from_xml_file(filename)
    a.to_wcs()


@pytest.mark.parametrize('filename', NO_WCS)
def test_to_wcs_nowcs(filename):
    a = AVM()
    a.from_xml_file(filename)
    with pytest.raises(NoSpatialInformation):
        a.to_wcs()
