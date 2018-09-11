"""
This is a temporary module to support unpriv way of interacting with container images.

It will be migrated to conu sooner or later.
"""
import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def run_and_log(cmd, ostree_repo_path, error_msg, wd=None):
    """ run provided command and log all of its output; set path to ostree repo """
    logger.debug("running command %s", cmd)
    kwargs = {
        "stderr": subprocess.STDOUT,
        "env": os.environ.copy(),
    }
    if ostree_repo_path:
        # must not exist, ostree will create it
        kwargs["env"]["ATOMIC_OSTREE_REPO"] = ostree_repo_path
    if wd:
        kwargs["cwd"] = wd
    try:
        subprocess.check_call(cmd, **kwargs)
    except subprocess.CalledProcessError as ex:
        logger.error(error_msg)
        raise


class ImageName(object):
    """ parse image references and access their components easily """

    def __init__(self, registry=None, namespace=None, repository=None, tag=None, digest=None):
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
            try:
                result.repository, result.tag = result.repository.rsplit(":", 1)
            except ValueError:
                result.tag = "latest"

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
        elif self.tag:
            name += ":{}".format(self.tag)

        return name
