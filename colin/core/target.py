# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import io
import json
import logging
import os
import shutil
import subprocess
from tempfile import mkdtemp

from dockerfile_parse import DockerfileParser

from .checks.abstract_check import ImageAbstractCheck, DockerfileAbstractCheck
from ..core.exceptions import ColinException
from ..utils.cont import ImageName

logger = logging.getLogger(__name__)


def is_compatible(target_type, check_instance):
    """
    Check the target compatibility with the check instance.

    :param target_type: Target subclass, if None, returns True
    :param check_instance: instance of some Check class
    :return: True if the target is None or compatible with the check instance
    """
    if not target_type:
        return True
    return isinstance(check_instance, target_type.get_compatible_check_class())


# we've introduced an API-breaking change in conu, we need to solve this at conu level:
# https://github.com/user-cont/conu/issues/220
# in the meantime, let's workaround here
def inspect_object(obj, refresh=True):
    """
    inspect provided object (container, image) and return raw dict with the metadata

    :param obj: instance of Container or an Image
    :param refresh: bool, refresh the metadata or return cached?
    :return: dict
    """
    if hasattr(obj, "inspect"):
        return obj.inspect(refresh=refresh)
    return obj.get_metadata(refresh=refresh)


class Target(object):
    """
    Target is the thing we are going to check; it can be
    - an image (specified by name, oci or dockertar)
    - dockerfile (specified by path or file-like object)
    """

    def __init__(self):
        self._labels = None
        self.target_name = None
        self.parent_target = None

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        return None

    def clean_up(self):
        """
        Perform clean up on the low level objects: atm oci and skopeo mountpoints
        and data are being cleaned up.
        """
        pass

    @classmethod
    def get_compatible_check_class(cls):
        """
        Get the compatible abstract check class.
        :return: cls
        """
        return None

    @staticmethod
    def get_instance(target_type, **kwargs):
        """
        :param target_type: string, either image, dockertar, oci or dockerfile
        """
        if target_type in TARGET_TYPES:
            cls = TARGET_TYPES[target_type]
            try:
                return cls(**kwargs)
            except Exception:
                logger.error(
                    "Please make sure that you picked the correct target type: "
                    "--target-type CLI option."
                )
                raise

        raise ColinException(
            f"Unknown target type '{target_type}'. "
            "Please make sure that you picked the correct target type: "
            "--target-type CLI option."
        )


class DockerfileTarget(Target):
    target_type = "dockerfile"

    def __init__(self, target, **_):
        super().__init__()
        self.target_name = target
        logger.debug("Target is a dockerfile.")
        if isinstance(target, io.IOBase):
            logger.debug("Target is a dockerfile loaded from the file-like object.")
            self.instance = DockerfileParser(fileobj=target)
        else:
            self.instance = DockerfileParser(fileobj=open(target))

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        if self._labels is None:
            self._labels = self.instance.labels
        return self._labels

    @classmethod
    def get_compatible_check_class(cls):
        return DockerfileAbstractCheck


class AbstractImageTarget(Target):
    """
    Abstract predecessor for the image-target classes. (e.g. oci and podman image)
    """

    @property
    def config_metadata(self):
        """metadata from "Config" key"""
        raise NotImplementedError("Unsupported right now.")

    @property
    def mount_point(self):
        """real filesystem"""
        raise NotImplementedError("Unsupported right now.")

    def get_output(self, cmd):
        """
        Get output of the command from the container based on this image.
        :param cmd: [str]
        :return: str
        """
        raise NotImplementedError("Unsupported right now.")

    def read_file(self, file_path):
        """
        read file specified via 'file_path' and return its content - raises an ConuException if
        there is an issue accessing the file
        :param file_path: str, path to the file to read
        :return: str (not bytes), content of the file
        """
        try:
            with open(self.cont_path(file_path)) as fd:
                return fd.read()
        except IOError as ex:
            logger.error("error while accessing file %s: %r", file_path, ex)
            raise ColinException(
                f"There was an error while accessing file {file_path}: {ex!r}"
            )

    def get_file(self, file_path, mode="r"):
        """
        provide File object specified via 'file_path'
        :param file_path: str, path to the file
        :param mode: str, mode used when opening the file
        :return: File instance
        """
        return open(self.cont_path(file_path), mode=mode)

    def file_is_present(self, file_path):
        """
        check if file 'file_path' is present, raises IOError if file_path
        is not a file
        :param file_path: str, path to the file
        :return: True if file exists, False if file does not exist
        """
        real_path = self.cont_path(file_path)
        if not os.path.exists(real_path):
            return False
        if not os.path.isfile(real_path):
            raise IOError(f"{file_path} is not a file")
        return True

    def cont_path(self, path):
        """
        provide absolute path within the container

        :param path: path with container
        :return: str
        """
        if path.startswith("/"):
            path = path[1:]
        real_path = os.path.join(self.mount_point, path)
        logger.debug("path = %s", real_path)
        return real_path

    @classmethod
    def get_compatible_check_class(cls):
        return ImageAbstractCheck


class ImageTarget(AbstractImageTarget):
    """
    Represents the podman image as a target.
    """

    target_type = "image"

    def __init__(self, target, pull, parent_target=None, insecure=False, **_):
        super().__init__()
        logger.debug("Target is an image.")
        self.pull = pull
        self.insecure = insecure
        self.image_name_obj = ImageName.parse(target)
        self.target_name = self.image_name_obj.name
        self.parent_target = parent_target

        self._config_metadata = None
        self._mount_point = None
        self._mounted_container_id = None
        self.image_id = None

        self._try_image()

    @property
    def config_metadata(self):
        if not self._config_metadata:
            cmd = ["podman", "inspect", self.target_name]
            loaded_config = json.loads(subprocess.check_output(cmd))
            if loaded_config and isinstance(loaded_config, list):
                self._config_metadata = loaded_config[0]
                # FIXME: Better validation.
            else:
                raise ColinException("Cannot load config for the image.")

        return self._config_metadata

    @property
    def labels(self):
        return self.config_metadata["Labels"] or {}

    @property
    def mount_point(self):
        """podman mount -- real filesystem"""
        if self._mount_point is None:
            cmd_create = ["podman", "create", self.target_name, "some-cmd"]
            self._mounted_container_id = (
                subprocess.check_output(cmd_create).decode().rstrip()
            )
            cmd_mount = ["podman", "mount", self._mounted_container_id]
            self._mount_point = subprocess.check_output(cmd_mount).decode().rstrip()
        return self._mount_point

    def _try_image(self):
        logger.debug("Trying to find an image.")
        cmd = ["podman", "images", "--quiet", self.target_name]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            self.image_id = result.stdout.decode().rstrip()
            logger.debug("Image found with id: '%s'.", self.image_id)
        else:
            if "unable to find" in result.stderr.decode():
                if self.pull:
                    logger.debug("Pulling an image.")
                    cmd_pull = ["podman", "pull", "--quiet", self.target_name]
                    result_pull = subprocess.run(
                        cmd_pull, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    if result_pull.returncode == 0:
                        self.image_id = result_pull.stdout.decode().rstrip()
                        logger.debug("Image pulled with id: '%s'.", self.image_id)
                    else:
                        raise ColinException(
                            f"Cannot pull an image: '{self.target_name}'."
                        )

                else:
                    raise ColinException(f"Image '{self.target_name}' not found.")
            else:
                raise ColinException(f"Podman error: {result.stderr}")

    def clean_up(self):
        if self._mount_point:
            cmd = ["podman", "umount", self._mounted_container_id]
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
            self._mount_point = None
        if self._mounted_container_id:
            cmd = ["podman", "rm", self._mounted_container_id]
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
            self._mounted_container_id = None

    def get_output(self, cmd):
        raise NotImplementedError("Unsupported right now.")


class OciTarget(AbstractImageTarget):
    """
    Represents the oci repository as an image target.
    """

    target_type = "oci"

    def __init__(self, target, parent_target=None, **_):
        super().__init__()
        logger.debug("Target is an oci repository.")

        self.target_name = target
        if self.target_name.startswith("oci:"):
            self.target_name = self.target_name[4:]

        try:
            self._oci_path, self.ref_image_name = self.target_name.split(":", 1)
        except ValueError:
            raise RuntimeError("Invalid oci target: should be 'path:image'.")

        self.parent_target = parent_target
        self._tmpdir = None
        self._mount_point = None
        self._layers_path = None
        self._labels = None

    @property
    def labels(self):
        """
        Provide labels without the need of dockerd. Instead skopeo is being used.

        :return: dict
        """
        if self._labels is None:
            cmd = ["skopeo", "inspect", self.skopeo_target]
            self._labels = json.loads(subprocess.check_output(cmd))["Labels"]
        return self._labels

    @property
    def layers_path(self):
        """Directory with all the layers (docker save)."""
        if self._layers_path is None:
            self._layers_path = os.path.join(self.tmpdir, "layers")
        return self._layers_path

    @property
    def mount_point(self):
        """oci checkout -- real filesystem"""
        if self._mount_point is None:
            checkout_dir = os.path.join(self.tmpdir, "checkout")
            os.makedirs(checkout_dir)
            # root filesystem is unpacked in rootfs subdirectory
            self._mount_point = os.path.join(checkout_dir, "rootfs")
            self._checkout(checkout_dir)
        return self._mount_point

    @property
    def oci_path(self):
        """oci repository -- content"""
        if self._oci_path is None:
            self._oci_path = os.path.join(self.tmpdir, "oci")
        return self._oci_path

    @property
    def skopeo_target(self):
        """Skopeo format for the oci repository."""
        return f"oci:{self.oci_path}:{self.ref_image_name}"

    @property
    def tmpdir(self):
        """Temporary directory holding all the runtime data."""
        if self._tmpdir is None:
            self._tmpdir = mkdtemp(prefix="colin-", dir="/var/tmp")
        return self._tmpdir

    def clean_up(self):
        shutil.rmtree(self.tmpdir)

    def _checkout(self, checkout_dir):
        """check out the image filesystem on self.mount_point"""
        cmd = [
            "umoci",
            "unpack",
            "--rootless",
            "--image",
            f"{self.oci_path}:{self.ref_image_name}",
            checkout_dir,
        ]
        self._run_and_log(cmd, "Failed to mount selected image as an oci repo.")

    @staticmethod
    def _run_and_log(cmd, error_msg):
        """run provided command and log all of its output"""
        logger.debug("running command %s", cmd)
        kwargs = {
            "stderr": subprocess.STDOUT,
            "env": os.environ.copy(),
        }
        try:
            out = subprocess.check_output(cmd, **kwargs)
        except subprocess.CalledProcessError as ex:
            logger.error(ex.output)
            logger.error(error_msg)
            raise
        logger.debug("%s", out)

    @property
    def config_metadata(self):
        """metadata from "Config" key"""
        raise NotImplementedError("Skopeo does not provide metadata yet.")

    def get_output(self, cmd):
        raise NotImplementedError("Unsupported right now.")


TARGET_TYPES = {
    "image": ImageTarget,
    "dockerfile": DockerfileTarget,
    "oci": OciTarget,
}
