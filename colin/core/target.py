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


class Target(object):

    def __init__(self, name):
        self.name = name
        self.instance = Target._get_target_instance(name)

    @staticmethod
    def _get_target_instance(target_name):
        """
        Get the Container/Image instance for the given name.
        (Container is the first choice.)

        :param target_name: str
        :return: Container/Image
        """
        with DockerBackend(logging_level=logging.NOTSET) as backend:

            try:
                cont = backend.ContainerClass(image=None,
                                              container_id=target_name)
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
                    return image
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
