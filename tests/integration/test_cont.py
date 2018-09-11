"""
Testing of low level interaction with images.
"""
import pytest

from colin.core.target import ImageTarget
from tests.conftest import BUSYBOX_IMAGE, LABELS_IMAGE


def test_file_is_present():
    im = ImageTarget(target=BUSYBOX_IMAGE, pull=True)
    assert im.file_is_present("/etc/passwd")
    assert not im.file_is_present("/oglogoblogologlo")
    with pytest.raises(IOError):
        im.file_is_present("/etc")


def test_labels_are_present():
    im = ImageTarget(target=LABELS_IMAGE, pull=False)
    assert isinstance(im.labels, dict)
