import os
from ..avm import AVM

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def test_from_image():
    AVM.from_image(os.path.join(ROOT, 'eso_eso1723a_320.jpg'))
