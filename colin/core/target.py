import enum

from conu import DockerBackend, DockerImagePullPolicy
from conu.apidefs.container import Container
from conu.apidefs.image import Image
from docker.errors import NotFound

from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.dockerfile import DockerfileCheck
from colin.checks.abstract.images import ImageCheck


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
        with DockerBackend() as backend:

            try:
                cont = backend.ContainerClass(image=None,
                                              container_id=target_name)
                return cont
            except NotFound:
                name_split = target_name.split(':')
                if len(name_split) == 2:
                    name, tag = name_split
                else:
                    name, tag = target_name, None

                image = backend.ImageClass(repository=name,
                                           tag=tag,
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
        raise Exception("Target not found.")


class TargetType(enum.Enum):
    DOCKERFILE = 0
    CONTAINER = 1
    CONTAINER_IMAGE = 2


def is_compatible(target_type, check_class, severity, tags):
    # TODO take severity and tags into consideration
    return (target_type == TargetType.DOCKERFILE and isinstance(check_class, DockerfileCheck)) \
           or (target_type == TargetType.CONTAINER and isinstance(check_class, ContainerCheck)) \
           or (target_type == TargetType.CONTAINER_IMAGE and isinstance(check_class, ImageCheck))
