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

import enum
import io
import logging

import six
from conu import DockerBackend
from conu.apidefs.container import Container
from dockerfile_parse import DockerfileParser

from colin.utils.cont import Image
from .checks.containers import ContainerAbstractCheck
from .checks.dockerfile import DockerfileAbstractCheck
from .checks.images import ImageAbstractCheck
from ..core.exceptions import ColinException

logger = logging.getLogger(__name__)


def is_compatible(target_type, check_instance):
    """
    Check the target compatibility with the check instance.

    :param target_type: TargetType enum, if None, returns True
    :param check_instance: instance of some Check class
    :return: True if the target is None or compatible with the check instance
    """
    if not target_type:
        return True
    return (
        (
            target_type == TargetType.DOCKERFILE and
            isinstance(check_instance, DockerfileAbstractCheck)
        )
        or (
            target_type == TargetType.CONTAINER and
            isinstance(check_instance, ContainerAbstractCheck)
        )
        or (
            # docker image tarballs are also images
            target_type in [TargetType.IMAGE, TargetType.DOCKER_TAR, TargetType.OSTREE]
            and isinstance(check_instance, ImageAbstractCheck)
        )
    )


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
    Target is the thing we are going to check; it can be an image, container or a dockerfile
    """

    def __init__(self, target, logging_level, target_type, pull=None, insecure=False):
        """
        :param target: str, identifier of the target (specified via CLI)
        :param logging_level: int, log level passed to conu
        :param target_type: string, either image, container or dockerfile
        :param pull: bool, if the target is an image, pull it if set to true
        :param insecure: bool, pull from an insecure registry (HTTP/invalid TLS)
        """
        # this is the thing which user passed
        self.target_identifier = target
        self._target_type_str = target_type
        self._labels = None
        self.instance = self._get_target_instance(target, logging_level, pull, insecure)

    def clean_up(self):
        """
        Perform clean up on the low level objects: atm atomic and skopeo mountpoints
        and data are being cleaned up.
        """
        if hasattr(self.instance, "clean_up"):
            self.instance.clean_up()

    def _get_target_instance(self, target, logging_level, pull, insecure):
        """
        Get the Container/Image instance for the given name.
        (Container is the first choice.)
        or DockerfileParser instance if the target is path or file-like object.

        :param target: str
                        or instance of Image/Container
                        or file-like object as Dockerfile
        :param logging_level: int, logging level passed to conu
        :param pull: bool, should the image be pulled?
        :param insecure: bool, pull from an insecure registry (HTTP/invalid TLS)
        :return: Target object
        """
        logger.debug("Identifying target '{}'.".format(target))

        # FIXME: simplify this: create target classes for each type
        # FIXME: remove support for containers: no one uses it

        if isinstance(target, Container):
            logger.debug("Target is a conu container.")
            return target
        if isinstance(target, io.IOBase):
            logger.debug("Target is a dockerfile loaded from the file-like object.")
            return DockerfileParser(fileobj=target)
        if isinstance(target, six.string_types):
            # user passed a string
            try:
                if self.target_type == TargetType.IMAGE:
                    logger.debug("Target is an image.")
                    return Image(target, pull=pull, insecure=insecure)
                if self.target_type == TargetType.DOCKER_TAR:
                    logger.debug("Target is a docker tarball image.")
                    return Image(target, pull=False, iz_dockertar=True)
                if self.target_type == TargetType.OSTREE:
                    logger.debug("Target is a ostree repository.")
                    return Image(target, pull=False, iz_ostree=True)
                elif self.target_type == TargetType.DOCKERFILE:
                    logger.debug("Target is a dockerfile.")
                    return DockerfileParser(fileobj=open(target))
                elif self.target_type == TargetType.CONTAINER:
                    with DockerBackend(logging_level=logging_level) as backend:
                        cont = backend.ContainerClass(image=None,
                                                      container_id=target)
                        logger.debug("Target is a container.")
                        return cont
            except Exception:
                logger.error("Please make sure that you picked the correct target type: "
                             "--target-type CLI option.")
                raise

    @property
    def target_type(self):
        """
        Type of the target (image/container/dockerfile)

        :return: TargetType enum
        """
        if self._target_type_str == "image":
            return TargetType.IMAGE
        elif self._target_type_str == "dockertar":
            return TargetType.DOCKER_TAR
        elif self._target_type_str == "ostree":
            return TargetType.OSTREE
        elif self._target_type_str == "container":
            return TargetType.CONTAINER
        elif self._target_type_str == "dockerfile":
            return TargetType.DOCKERFILE
        logger.debug("Unknown target type; should be one of: container, image or dockerfile.")
        raise ColinException(
            "Unknown target type; should be one of: container, image or dockerfile.")

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
        if self._labels is None:
            if self.target_type == TargetType.DOCKERFILE:
                self._labels = self.instance.labels
            elif self.target_type in [TargetType.IMAGE, TargetType.DOCKER_TAR, TargetType.OSTREE]:
                self._labels = self.instance.labels
            elif self.target_type == TargetType.CONTAINER:
                self._labels = inspect_object(self.instance, refresh=True)["Config"]["Labels"]
        return self._labels

    def get_output(self, cmd):
        if isinstance(cmd, six.string_types):
            cmd = [cmd]
        if self.target_type == TargetType.CONTAINER:
            if not self.instance.is_running():
                raise ColinException("Cannot get output for a stopped container.")
            output = "".join([o.decode() for o in self.instance.execute(command=cmd)])
            exit_code = inspect_object(self.instance, refresh=True)["State"]["ExitCode"]

            if exit_code != 0:
                raise ColinException(
                    "Container exited with the code {}. Output:\n{}".format(exit_code, output))

        elif self.target_type == TargetType.IMAGE:
            raise RuntimeError("Unsupported right now.")
            # container = self.instance.run_via_binary(command=cmd)
            # container.wait()
            # output = "".join([o.decode() for o in container.logs()])
            # exit_code = inspect_object(container, refresh=True)["State"]["ExitCode"]
            # container.delete(force=True)

            # if exit_code != 0:
            #     raise ColinException(
            #         "Container exited with the code {}. Output:\n{}".format(exit_code, output))
            # return output
        else:
            raise ColinException("Cannot get command output for given target type.")


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER = 1
    IMAGE = 2
    DOCKER_TAR = 3  # a tarball with all the layers (can be generated by `docker save`)
    OSTREE = 4      # a directory with an ostree repo (skopeo copy ostree:/...)
