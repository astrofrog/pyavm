from __future__ import print_function, division

import os
import glob
import warnings

import pytest

pytest.importorskip('PIL')
pytest.importorskip('numpy')

from PIL import Image
import numpy as np

from .. import AVM

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

XML_FILES = glob.glob(os.path.join(ROOT, '*.xml'))


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
        messages = [str(x.message) for x in w]
        assert 'Discarding existing XMP packet from PNG file' not in messages
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_out_1, filename_out_2, verify=True)
        messages = [str(x.message) for x in w]
        assert 'Discarding existing XMP packet from PNG file' in messages


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
        messages = [str(x.message) for x in w]
        assert 'Discarding existing XMP packet from JPEG file' not in messages
    with warnings.catch_warnings(record=True) as w:
        avm.embed(filename_out_1, filename_out_2, verify=True)
        messages = [str(x.message) for x in w]
        assert 'Discarding existing XMP packet from JPEG file' in messages
