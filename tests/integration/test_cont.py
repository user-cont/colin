"""
Testing of low level interaction with images.
"""
import pytest

from colin.core.target import ImageTarget
from tests.conftest import BUSYBOX_IMAGE, LABELS_IMAGE


def test_file_is_present():
    image = ImageTarget(target=BUSYBOX_IMAGE, pull=True)
    assert image.file_is_present("/etc/passwd")
    assert not image.file_is_present("/oglogoblogologlo")
    with pytest.raises(IOError):
        image.file_is_present("/etc")


def test_labels_are_present():
    image = ImageTarget(target=LABELS_IMAGE, pull=False)
    assert isinstance(image.labels, dict)
