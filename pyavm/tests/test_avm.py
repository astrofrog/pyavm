import os
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
