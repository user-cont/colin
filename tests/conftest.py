import logging
import os
import subprocess

import pytest

from colin.core.colin import _set_logging

_set_logging(level=logging.DEBUG)

BASH_IMAGE = "colin-test-bash"
LS_IMAGE = "colin-test-ls"
BUSYBOX_IMAGE = "docker.io/library/busybox"
LABELS_IMAGE = "colin-labels:latest"
IMAGES = {
    BASH_IMAGE: {
        "dockerfile_path": "Dockerfile-bash"
    },
    LS_IMAGE: {
        "dockerfile_path": "Dockerfile-ls"
    },
    LABELS_IMAGE: {
        "dockerfile_path": "Dockerfile"
    }
}


def build_images():
    """ build container images we need for testing """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(this_dir, "data")
    for image_name, image_data in IMAGES.items():
        cmd_create = ["podman", "build", "-t", image_name, "-f",
                      image_data["dockerfile_path"], data_dir]
        output = subprocess.check_output(cmd_create)
        assert output


@pytest.fixture(autouse=True, scope='session')
def setup_test_session():
    """ set up environment before testing """
    for image_name in IMAGES:
        try:
            subprocess.check_call(["podman", "image", "inspect", image_name],
                                  stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            break
    # executed if break was not reached
    else:
        # all images were found, we're good
        return
    # the loop ended with break, create images
    build_images()
