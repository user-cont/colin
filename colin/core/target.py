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
from conu.apidefs.container import Container
from conu.apidefs.image import Image
from docker.errors import NotFound

from ..core.exceptions import ColinException
from ..checks.abstract.containers import ContainerCheck
from ..checks.abstract.dockerfile import DockerfileCheck
from ..checks.abstract.images import ImageCheck

logger = logging.getLogger(__name__)


class Target(object):

    def __init__(self, name, logging_level):
        self.name = name
        self.instance = Target._get_target_instance(name, logging_level=logging_level)

    @staticmethod
    def _get_target_instance(target_name, logging_level):
        """
        Get the Container/Image instance for the given name.
        (Container is the first choice.)

        :param target_name: str
        :return: Container/Image
        """
        logger.debug("Finding target '{}'.".format(target_name))

        with DockerBackend(logging_level=logging_level) as backend:

            try:
                cont = backend.ContainerClass(image=None,
                                              container_id=target_name)
                logger.debug("Target is a container.")
                return cont
            except NotFound:
                name_split = target_name.split(':')
                if len(name_split) == 2:
                    name, tag = name_split
                    image = backend.ImageClass(repository=name,
                                               tag=tag,
                                               pull_policy=DockerImagePullPolicy.NEVER)
                else:
                    image = backend.ImageClass(repository=target_name,
                                               pull_policy=DockerImagePullPolicy.NEVER)

                if image.is_present():
                    logger.debug("Target is an image.")
                    return image
        logger.warning("Target is neither image nor container.")
        return None

    @property
    def target_type(self):
        if isinstance(self.instance, Image):
            return TargetType.CONTAINER_IMAGE
        elif isinstance(self.instance, Container):
            return TargetType.CONTAINER
        raise ColinException("Target not found.")


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER = 1
    CONTAINER_IMAGE = 2


def is_compatible(target_type, check_class, severity, tags):
    # TODO take severity and tags into consideration
    return (target_type == TargetType.DOCKERFILE and isinstance(check_class, DockerfileCheck)) \
           or (target_type == TargetType.CONTAINER and isinstance(check_class, ContainerCheck)) \
           or (target_type == TargetType.CONTAINER_IMAGE and isinstance(check_class, ImageCheck))
