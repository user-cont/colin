import logging
import os
import shutil
import subprocess
import tempfile

import pytest

from colin.core.colin import _set_logging
from colin.core.target import ImageTarget, OciTarget, DockerfileTarget

_set_logging(level=logging.DEBUG)

BASH_IMAGE = "colin-test-bash"
LS_IMAGE = "colin-test-ls"
BUSYBOX_IMAGE = "busybox:latest"
LABELS_IMAGE = "colin-labels"
LABELS_IMAGE_PARENT = "colin-labels-parent"
IMAGES = {
    BASH_IMAGE: {"dockerfile_path": "Dockerfile-bash"},
    LS_IMAGE: {"dockerfile_path": "Dockerfile-ls"},
    LABELS_IMAGE: {"dockerfile_path": "Dockerfile"},
    LABELS_IMAGE_PARENT: {"dockerfile_path": "Dockerfile-parent"},
}


def build_image_if_not_exists(image_name):
    try:
        subprocess.check_call(["podman", "image", "exists", image_name])
    except subprocess.CalledProcessError:
        this_dir = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(this_dir, "data")

        dockerfile_path = IMAGES[image_name]["dockerfile_path"]
        cmd_create = [
            "podman",
            "build",
            "-t",
            image_name,
            "-f",
            dockerfile_path,
            data_dir,
        ]
        subprocess.check_call(cmd_create)


def pull_image_if_not_exists(image_name):
    try:
        subprocess.check_call(["podman", "image", "exists", image_name])
    except subprocess.CalledProcessError:
        subprocess.check_call(["podman", "pull", image_name])


def convert_image_to_oci(image_name):
    tmpdir_path = tempfile.mkdtemp(prefix="pytest-", dir="/var/tmp")
    oci_path = os.path.join(tmpdir_path, "oci")
    os.makedirs(oci_path)
    skopeo_target = get_skopeo_oci_target(image_name=image_name, oci_path=oci_path)

    cmd = ["podman", "push", image_name, skopeo_target]
    subprocess.check_call(cmd)
    return oci_path


def get_target(name, type):
    if type == "image":

        target = ImageTarget(target=name, pull=False)
        yield target
        target.clean_up()

    elif type == "oci":

        oci_path = convert_image_to_oci(name)
        skopeo_target = get_skopeo_oci_target(image_name=name, oci_path=oci_path)

        oci_target = OciTarget(target=skopeo_target)
        yield oci_target
        oci_target.clean_up()
        shutil.rmtree(oci_path)

    elif type == "dockerfile":

        this_dir = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(this_dir, "data")
        dockerfile_path = os.path.join(data_dir, IMAGES[name]["dockerfile_path"])

        yield DockerfileTarget(target=dockerfile_path)


def get_skopeo_oci_target(image_name, oci_path):
    return f"oci:{oci_path}:{image_name}"


@pytest.fixture(scope="session", autouse=True)
def label_image():
    build_image_if_not_exists(LABELS_IMAGE)


@pytest.fixture(scope="session", params=["image", "oci", "dockerfile"])
def target_label(request, label_image):
    yield from get_target(name=LABELS_IMAGE, type=request.param)


@pytest.fixture(scope="session", params=["image", "oci", "dockerfile"])
def target_label_image_and_dockerfile(request, label_image):
    yield from get_target(name=LABELS_IMAGE, type=request.param)


@pytest.fixture(scope="session", autouse=True)
def target_bash_image():
    build_image_if_not_exists(BASH_IMAGE)


@pytest.fixture(scope="session", params=["image", "oci"])
def target_bash(request, target_bash_image):
    yield from get_target(name=BASH_IMAGE, type=request.param)


@pytest.fixture(scope="session", autouse=True)
def target_ls_image():
    build_image_if_not_exists(LS_IMAGE)


@pytest.fixture(scope="session", params=["image", "oci"])
def target_ls(request, target_ls_image):
    yield from get_target(name=LS_IMAGE, type=request.param)


@pytest.fixture(scope="session", params=[LS_IMAGE, BASH_IMAGE])
def target_help_file(request, target_ls, target_bash):
    if request.param == LS_IMAGE:
        return target_ls, False
    if request.param == BASH_IMAGE:
        return target_bash, True


@pytest.fixture(scope="session", autouse=True)
def target_busybox_image():
    pull_image_if_not_exists(image_name=BUSYBOX_IMAGE)


@pytest.fixture(scope="session", params=["image", "oci"])
def target_busybox(request, target_busybox_image):
    yield from get_target(name=BUSYBOX_IMAGE, type=request.param)
