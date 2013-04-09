from __future__ import print_function, division

import os
import glob
import warnings

import pytest

try:
    from PIL import Image
except ImportError:
    try:
        import Image
    except ImportError:
        pytest.skip()

try:
    import numpy as np
except ImportError:
    pytest.skip()

from .. import AVM

ROOT = os.path.dirname(os.path.abspath(__file__))

XML_FILES = glob.glob(os.path.join(ROOT, 'data', '*.xml'))


@pytest.mark.parametrize('xml_file', XML_FILES)
def test_io_png(tmpdir, xml_file):
    avm = AVM.from_xml_file(xml_file)
    filename_in = tmpdir.join('test_in.png').strpath
    filename_out = tmpdir.join('test_out.png').strpath
    i = Image.fromarray(np.ones((16, 16), dtype=np.uint8))
    i.save(filename_in)
    avm.embed(filename_in, filename_out, verify=True)


@pytest.mark.parametrize('xml_file', XML_FILES)
def test_io_jpeg(tmpdir, xml_file):
    avm = AVM.from_xml_file(xml_file)
    filename_in = tmpdir.join('test_in.jpg').strpath
    filename_out = tmpdir.join('test_out.jpg').strpath
    i = Image.fromarray(np.ones((16, 16), dtype=np.uint8))
    i.save(filename_in)
    avm.embed(filename_in, filename_out, verify=True)


@pytest.mark.parametrize('xml_file', XML_FILES)
def test_io_png_repeat(tmpdir, xml_file):
    warnings.simplefilter('always')
    avm = AVM.from_xml_file(xml_file)
    filename_in = tmpdir.join('test_in.png').strpath
    filename_out_1 = tmpdir.join('test_out_1.png').strpath
    filename_out_2 = tmpdir.join('test_out_2.png').strpath
    i = Image.fromarray(np.ones((16, 16), dtype=np.uint8))
    i.save(filename_in)
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_in, filename_out_1, verify=True)
        assert w == []
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_out_1, filename_out_2, verify=True)
        assert len(w) == 1
        assert str(w[0].message) == 'Discarding existing XMP packet from PNG file'


@pytest.mark.parametrize('xml_file', XML_FILES)
def test_io_jpeg_repeat(tmpdir, xml_file):
    warnings.simplefilter('always')
    avm = AVM.from_xml_file(xml_file)
    filename_in = tmpdir.join('test_in.jpg').strpath
    filename_out_1 = tmpdir.join('test_out_1.jpg').strpath
    filename_out_2 = tmpdir.join('test_out_2.jpg').strpath
    i = Image.fromarray(np.ones((16, 16), dtype=np.uint8))
    i.save(filename_in)
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_in, filename_out_1, verify=True)
        assert w == []
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_out_1, filename_out_2, verify=True)
        assert len(w) == 1
        assert str(w[0].message) == 'Discarding existing XMP packet from JPEG file'
