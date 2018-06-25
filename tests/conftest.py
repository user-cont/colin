import logging
import os
import subprocess

import pytest
from conu import DockerBackend

from colin.core.colin import _set_logging


_set_logging(level=logging.DEBUG)


BASH_IMAGE = "colin-test-bash"
LS_IMAGE = "colin-test-ls"
BUSYBOX_IMAGE = "docker.io/library/busybox"
LABELS_IMAGE = "colin-labels"
IMAGES = {
    BASH_IMAGE: {
        "dockerfile_path": "Dockerfile-bash"
    },
    LS_IMAGE: {
        "dockerfile_path": "Dockerfile-ls"
    }
}


def build_images():
    """ build container images we need for testing """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(this_dir, "data")
    with DockerBackend() as backend:
        for image_name, image_data in IMAGES.items():
            backend.ImageClass.build(data_dir, tag=image_name,
                                     dockerfile=image_data["dockerfile_path"])


@pytest.fixture(autouse=True, scope='session')
def setup_test_session():
    """ set up environment before testing """
    for image_name in IMAGES:
        try:
            subprocess.check_call(["docker", "image", "inspect", image_name],
                                  stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            break
    # executed if break was not reached
    else:
        # all images were found, we're good
        return
    # the loop ended with break, create images
    build_images()
