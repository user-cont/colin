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
import logging

from dockerfile_parse import DockerfileParser

from colin.utils.cont import Image
from .checks.dockerfile import DockerfileAbstractCheck
from .checks.images import ImageAbstractCheck
from ..core.exceptions import ColinException

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
    - an image (specified by name, ostree or dockertar)
    - dockerfile (specified by path or file-like object)
    """

    def __init__(self):
        self._labels = None
        self.instance = None

    @staticmethod
    def get_instance(target_type, **kwargs):
        """
        :param target_type: string, either image, dockertar, ostree or dockerfile
        """
        if target_type in TARGET_TYPES:
            cls = TARGET_TYPES[target_type]
            try:
                return cls(**kwargs)
            except Exception:
                logger.error("Please make sure that you picked the correct target type: "
                             "--target-type CLI option.")
                raise

        raise ColinException(
            "Unknown target type '{}'. Please make sure that you picked the correct target type: "
            "--target-type CLI option.".format(target_type))

    def clean_up(self):
        """
        Perform clean up on the low level objects: atm atomic and skopeo mountpoints
        and data are being cleaned up.
        """
        if hasattr(self.instance, "clean_up"):
            self.instance.clean_up()

    @classmethod
    def get_compatible_check_class(cls):
        """
        Get the compatible abstract check class.
        :return: cls
        """
        return None

    @property
    def config_metadata(self):
        """ metadata from "Config" key """
        # FIXME: unfortunately skopeo doesn't provide these; we need to wait for podman
        return {}

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        return None

    def get_output(self, cmd):
        raise RuntimeError("Unsupported right now.")


class DockerfileTarget(Target):

    def __init__(self, target, **kwargs):
        super().__init__()
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


class ImageTarget(Target):

    def __init__(self, target, pull, insecure=False, **kwargs):
        super().__init__()
        logger.debug("Target is an image.")
        self.instance = Image(target, pull=pull, insecure=insecure)

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
        return ImageAbstractCheck


class DockerTarTarget(Target):

    def __init__(self, target, **kwargs):
        super().__init__()
        logger.debug("Target is a docker tarball image.")
        self.instance = Image(target, pull=False, iz_dockertar=True)

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
        return ImageAbstractCheck


class OstreeTarget(Target):

    def __init__(self, target, **kwargs):
        super().__init__()
        logger.debug("Target is a ostree repository.")
        self.instance = Image(target, pull=False, iz_ostree=True)

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
        return ImageAbstractCheck


TARGET_TYPES = {
    "image": ImageTarget,
    "dockerfile": DockerfileTarget,
    "dockertar": DockerTarTarget,
    "ostree": OstreeTarget
}
