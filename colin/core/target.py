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
import logging

from conu import DockerBackend, DockerImagePullPolicy
from conu.apidefs.container import Container, Image
from conu.apidefs.image import Image
from docker.errors import NotFound

from ..core.exceptions import ColinException
from ..checks.abstract.containers import ContainerCheck
from ..checks.abstract.dockerfile import DockerfileCheck
from ..checks.abstract.images import ImageCheck

logger = logging.getLogger(__name__)


class Target(object):

    def __init__(self, target, logging_level):
        self.instance = Target._get_target_instance(target, logging_level=logging_level)

    @staticmethod
    def _get_target_instance(target, logging_level):
        """
        Get the Container/Image instance for the given name.
        (Container is the first choice.)

        :param target: str or instance of Image/Container
        :return: Container/Image
        """
        logger.debug("Finding target '{}'.".format(target))

        if isinstance(target, Image):
            return target
        if isinstance(target, Container):
            return target

        with DockerBackend(logging_level=logging_level) as backend:

            try:
                cont = backend.ContainerClass(image=None,
                                              container_id=target)
                logger.debug("Target is a container.")
                return cont
            except NotFound:

                image_name = ImageName.parse(target)
                logger.debug(str(image_name))

                logger.debug("Finding image '{}' with tag '{}'.".format(image_name.name, image_name.tag))
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
        logger.error("Target is neither image nor container.")
        raise ColinException("Target not found.")

    @property
    def target_type(self):
        if isinstance(self.instance, Image):
            return TargetType.CONTAINER_IMAGE
        elif isinstance(self.instance, Container):
            return TargetType.CONTAINER
        logger.debug("Target type not found.")
        raise ColinException("Target type not found.")


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER = 1
    CONTAINER_IMAGE = 2


def is_compatible(target_type, check_class, severity, tags):
    # TODO take severity and tags into consideration
    return (target_type == TargetType.DOCKERFILE and isinstance(check_class, DockerfileCheck)) \
           or (target_type == TargetType.CONTAINER and isinstance(check_class, ContainerCheck)) \
           or (target_type == TargetType.CONTAINER_IMAGE and isinstance(check_class, ImageCheck))


class ImageName(object):
    def __init__(self, registry=None, namespace=None, repository=None, tag=None, image_id=None):
        self.registry = registry
        self.namespace = namespace
        self.repository = repository
        self.tag = tag
        self.image_id = image_id

    @classmethod
    def parse(cls, image_name):
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

        for sep in '@:':
            try:
                result.repository, result.tag = result.repository.rsplit(sep, 1)
            except ValueError:
                continue
            break

        return result

    def __str__(self):
        return "Image: registry='{}' namespace='{}' repository='{}' tag='{}'".format(self.registry,
                                                                                     self.namespace,
                                                                                     self.repository,
                                                                                     self.tag)

    @property
    def name(self):
        name_parts = []
        if self.registry:
            name_parts.append(self.registry)

        if self.namespace:
            name_parts.append(self.namespace)

        if self.repository:
            name_parts.append(self.repository)
        name = "/".join(name_parts)
        return name
