"""
Testing of low level interaction with images.
"""
from colin.utils.cont import Image

from tests.conftest import BUSYBOX_IMAGE, LABELS_IMAGE

import pytest


def test_file_is_present():
    im = Image(BUSYBOX_IMAGE, True)
    assert im.file_is_present("/etc/passwd")
    assert not im.file_is_present("/oglogoblogologlo")
    with pytest.raises(IOError):
        im.file_is_present("/etc")


def test_labels_are_present():
    im = Image(LABELS_IMAGE, False)
    assert isinstance(im.labels, dict)
