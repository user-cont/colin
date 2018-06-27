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
import os

import six
from conu import DockerBackend, DockerImagePullPolicy
from conu.apidefs.container import Container
from conu.apidefs.image import Image
from docker.errors import NotFound
from dockerfile_parse import DockerfileParser

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
    return \
        (
                target_type == TargetType.DOCKERFILE and
                isinstance(check_instance, DockerfileAbstractCheck)
        ) \
        or (
                target_type == TargetType.CONTAINER and
                isinstance(check_instance, ContainerAbstractCheck)
        ) \
        or (target_type == TargetType.IMAGE and isinstance(check_instance, ImageAbstractCheck))


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

    def __init__(self, target, logging_level):
        self.instance = Target._get_target_instance(target, logging_level=logging_level)
        self.logging_level = logging_level
        self._base_image = None

    @staticmethod
    def _get_target_instance(target, logging_level):
        """
        Get the Container/Image instance for the given name.
        (Container is the first choice.)
        or DockerfileParser instance if the target is path or file-like object.

        :param target: str
                        or instance of Image/Container
                        or file-like object as Dockerfile
        :return: Target object
        """
        logger.debug("Finding target '{}'.".format(target))

        if isinstance(target, (Image, Container)):
            logger.debug("Target is a conu object.")
            return target
        if isinstance(target, io.IOBase):
            logger.debug("Target is a dockerfile loaded from the file-like object.")
            return DockerfileParser(fileobj=target)
        if os.path.isfile(target):
            logger.debug("Target is a dockerfile.")
            return DockerfileParser(fileobj=open(target))

        with DockerBackend(logging_level=logging_level) as backend:

            try:
                cont = backend.ContainerClass(image=None,
                                              container_id=target)
                logger.debug("Target is a container.")
                return cont
            except NotFound:

                image = Target._create_image_instance(backend=backend, name=target)
                if image:
                    return image
        logger.error("Target is neither image nor container.")
        raise ColinException("Target not found.")

    @staticmethod
    def _create_image_instance(backend, name):
        image_name = ImageName.parse(name)
        logger.debug(
            "Finding image '{}' with tag '{}'.".format(image_name.name, image_name.tag))

        if image_name.tag:
            image = backend.ImageClass(repository=image_name.name,
                                       tag=image_name.tag,
                                       pull_policy=DockerImagePullPolicy.NEVER)
        else:
            image = backend.ImageClass(repository=image_name.name,
                                       pull_policy=DockerImagePullPolicy.NEVER)

        if image.is_present():
            logger.debug("Target is an image.")
            return image

        return None

    @property
    def target_type(self):
        """
        Type of the target (image/container/dockerfile)

        :return: TargetType enum
        """
        if isinstance(self.instance, Image):
            return TargetType.IMAGE
        elif isinstance(self.instance, Container):
            return TargetType.CONTAINER
        elif isinstance(self.instance, DockerfileParser):
            return TargetType.DOCKERFILE
        logger.debug("Target type not found.")
        raise ColinException("Target type not found.")

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        if self.target_type == TargetType.DOCKERFILE:
            return self.instance.labels
        # labels won't change, hence refresh=false
        return inspect_object(self.instance, refresh=False)["Config"]["Labels"]

    @property
    def base_image(self):
        """
        Get a following image:
        Dockerfile -> FROM
        Image -> Parent
        Container -> Image

        :return: Image
        """
        if self._base_image:
            return self._base_image

        if self.target_type == TargetType.DOCKERFILE:
            base_image = self.instance.parent_images
        elif self.target_type == TargetType.CONTAINER:
            base_image = inspect_object(self.instance, refresh=False)["Image"]
        else:
            base_image = inspect_object(self.instance, refresh=False)["Parent"]
            if not base_image:
                with DockerBackend(logging_level=self.logging_level) as backend:

                    layers = self.instance.layers()
                    if len(layers) >= 2 and layers[1].get_id() != '<missing>':
                        self._base_image = layers[1]
                        return layers[1]

                    instance_layers \
                        = inspect_object(self.instance, refresh=False)["RootFS"]["Layers"]
                    for i in backend.list_images():
                        i_layers = inspect_object(i, refresh=False)["RootFS"]["Layers"]
                        if set(i_layers) < set(instance_layers):
                            self._base_image = i
                            return i

        if not base_image:
            return None

        with DockerBackend(logging_level=self.logging_level) as backend:
            self._base_image = self._create_image_instance(backend=backend, name=base_image)

        return self._base_image

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
            container = self.instance.run_via_binary(command=cmd)
            container.wait()
            output = "".join([o.decode() for o in container.logs()])
            exit_code = inspect_object(container, refresh=True)["State"]["ExitCode"]
            container.delete(force=True)

            if exit_code != 0:
                raise ColinException(
                    "Container exited with the code {}. Output:\n{}".format(exit_code, output))
            return output
        else:
            raise ColinException("Cannot get command output for given target type.")


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER = 1
    IMAGE = 2


class ImageName(object):
    def __init__(self, registry=None, namespace=None, repository=None, tag=None, digest=None):
        self.registry = registry
        self.namespace = namespace
        self.repository = repository
        self.tag = tag
        self.digest = digest

    @classmethod
    def parse(cls, image_name):
        """
        Get the instance of ImageName from the string representation.

        :param image_name: str (any possible form of image name)
        :return: ImageName instance
        """
        result = cls()

        # registry.org/namespace/repo:tag
        s = image_name.split('/', 2)

        if len(s) == 2:
            if '.' in s[0] or ':' in s[0]:
                result.registry = s[0]
            else:
                result.namespace = s[0]
        elif len(s) == 3:
            result.registry = s[0]
            result.namespace = s[1]
        result.repository = s[-1]

        try:
            result.repository, result.digest = result.repository.rsplit("@", 1)
        except ValueError:
            pass

        try:
            result.repository, result.tag = result.repository.rsplit(":", 1)
        except ValueError:
            pass

        return result

    def __str__(self):
        return "Image: registry='{}' namespace='{}' " \
               "repository='{}' tag='{}' digest='{}'".format(self.registry,
                                                             self.namespace,
                                                             self.repository,
                                                             self.tag,
                                                             self.digest)

    @property
    def name(self):
        """
        Get the string representation of the image
        (registry, namespace, repository and digest together).

        :return: str
        """
        name_parts = []
        if self.registry:
            name_parts.append(self.registry)

        if self.namespace:
            name_parts.append(self.namespace)

        if self.repository:
            name_parts.append(self.repository)
        name = "/".join(name_parts)

        if self.digest:
            name += "@{}".format(self.digest)

        return name
