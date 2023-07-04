"""
This is a temporary module to support unpriv way of interacting with container images.

"""
import logging

logger = logging.getLogger(__name__)


class ImageName:
    """parse image references and access their components easily"""

    def __init__(
        self, registry=None, namespace=None, repository=None, tag=None, digest=None
    ):
        self.registry = registry
        self.namespace = namespace
        self.repository = repository
        self.digest = digest
        self.tag = tag

    @classmethod
    def parse(cls, image_name):
        """
        Get the instance of ImageName from the string representation.

        :param image_name: str (any possible form of image name)
        :return: ImageName instance
        """
        result = cls()

        # registry.org/namespace/repo:tag
        s = image_name.split("/", 2)

        if len(s) == 2:
            if "." in s[0] or ":" in s[0]:
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
            try:
                result.repository, result.tag = result.repository.rsplit(":", 1)
            except ValueError:
                result.tag = "latest"

        return result

    def __str__(self):
        return (
            f"Image: registry='{self.registry}' namespace='{self.namespace}' "
            f"repository='{self.repository}' tag='{self.tag}' digest='{self.digest}'"
        )

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
            name += f"@{self.digest}"
        elif self.tag:
            name += f":{self.tag}"

        return name
