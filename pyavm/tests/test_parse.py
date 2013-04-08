import os
import glob

import pytest

from .. import AVM

@pytest.mark.parametrize('filename', glob.glob(os.path.join('data', '*.xml')))
def test_parse(filename):
    a = AVM()
    a.from_xml_file(filename)
