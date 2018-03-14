import enum

from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.dockerfile import DockerfileCheck
from colin.checks.abstract.images import ImageCheck


class Target(object):

    def __init__(self, name):
        self.name = name

    @property
    def target_type(self):
        return None


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER_IMAGE = 1
    IMAGE = 2


def is_compatible(target_type, check_class, severity, tags):
    # TODO take severity and tags into consideration
    return (target_type == TargetType.DOCKERFILE and isinstance(check_class, DockerfileCheck)) \
           or (target_type == TargetType.CONTAINER_IMAGE and isinstance(check_class, ContainerCheck)) \
           or (target_type == TargetType.IMAGE and isinstance(check_class, ImageCheck))
