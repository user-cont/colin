"""
Testing of low level interaction with images.
"""
import pytest


def test_file_is_present(target_busybox):
    assert target_busybox.file_is_present("/etc/passwd")
    assert not target_busybox.file_is_present("/oglogoblogologlo")
    with pytest.raises(IOError):
        target_busybox.file_is_present("/etc")


def test_labels_are_present(target_label):
    assert isinstance(target_label.labels, dict)
