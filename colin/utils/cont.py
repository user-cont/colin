"""
This is a temporary module to support unpriv way of interacting with container images.

It will be migrated to conu sooner or later.
"""
import json
import os
import logging
import shutil
import subprocess
from tempfile import mkdtemp

from colin.core.exceptions import ColinException


logger = logging.getLogger(__name__)


def extract_file_from_tarball(tarball_path, file_path, wd):
    """
    Extract selected file (file_path) from tarball (tarball_path) within a selected
    directory (wd).
    """
    tar_cmd = ["tar", "-xf", tarball_path, file_path]
    out = subprocess.check_output(tar_cmd, cwd=wd)
    if out:
        logger.debug("output of tar command:")
        logger.debug(out)


class Image(object):
    """ Image representation using skopeo, ostree and atomic tool """

    def __init__(self, image_name, pull):
        """
        :param image_name: str, name of the image to access
        :param pull: bool, pull the image from registry or from local dockerd
        """
        self.image_name = image_name
        self.pull = pull
        self._tmpdir = None
        self._mount_point = None
        self._ostree_path = None
        self._layers_path = None

        self.metadata = None
        self._labels = None

        self._pull_image()


    @property
    def tmpdir(self):
        """ Temporary directory holding all the runtime data. """
        if self._tmpdir is None:
            self._tmpdir = mkdtemp(prefix="colin-", dir="/var/tmp")
        return self._tmpdir

    @property
    def ostree_path(self):
        """ ostree repository -- content """
        if self._ostree_path is None:
            self._ostree_path = os.path.join(self.tmpdir, "ostree-repo")
        return self._ostree_path

    @property
    def mount_point(self):
        """ ostree checkout -- real filesystem """
        if self._mount_point is None:
            self._mount_point = os.path.join(self.tmpdir, "checkout")
            os.makedirs(self._mount_point)
            self._checkout()
        return self._mount_point

    @property
    def layers_path(self):
        """ Directory with all the layers (docker save). """
        if self._layers_path is None:
            self._layers_path = os.path.join(self.tmpdir, "layers")
        return self._layers_path

    def _pull_image(self):
        """ pull the image using atomic --storage ostree """
        image_name = ImageName.parse(self.image_name)

        if self.pull:
            skopeo_source = "docker://" + image_name.name
            atomic_source = image_name.name
        else:
            skopeo_source = "docker-daemon:" + image_name.name
            atomic_source = "docker:" + image_name.name

        e = os.environ.copy()
        e["ATOMIC_OSTREE_REPO"] = self.ostree_path
        # must not exist, ostree will create it
        out = subprocess.check_output(
            ["atomic", "--debug", "pull", "--storage", "ostree", atomic_source],
            env=e)
        logger.debug("output of atomic command:")
        logger.debug(out)

        archive_file_name = "archive.tar"
        archive_path = os.path.join(self.tmpdir, archive_file_name)
        skopeo_target = "docker-archive:" + archive_path
        skopeo_cmd = ["skopeo", "copy", skopeo_source, skopeo_target]
        out = subprocess.check_output(skopeo_cmd)
        logger.debug("output of skopeo command:")
        logger.debug(out)

        manifest_file_name = "manifest.json"

        # first extract manifest
        extract_file_from_tarball(archive_file_name, manifest_file_name, self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, manifest_file_name)
        with open(manifest_path) as fd:
            j = json.load(fd)

        # figure out name of the metadata file
        metadata_file_name = j[0]["Config"]

        # then extract the metadata
        extract_file_from_tarball(archive_file_name, metadata_file_name, self.tmpdir)
        metadata_file_path = os.path.join(self.tmpdir, metadata_file_name)
        with open(metadata_file_path) as fd:
            self.metadata = json.load(fd)

    def _checkout(self):
        """ check out the image filesystem on self.mount_point """
        e = os.environ.copy()
        e["ATOMIC_OSTREE_REPO"] = self.ostree_path
        # self.mount_point has to be created by us
        out = subprocess.check_output(
            ["atomic", "--debug", "mount", "--storage", "ostree", self.image_name, self.mount_point],
            env=e)
        logger.debug("output of atomic command:")
        logger.debug(out)

    def clean_up(self):
        shutil.rmtree(self.tmpdir)

    def p(self, path):
        """
        provide absolute path within the container
        :param path: path with container
        :return: str
        """
        if path.startswith("/"):
            path = path[1:]
        p = os.path.join(self.mount_point, path)
        logger.debug("path = %s", p)
        return p

    def read_file(self, file_path):
        """
        read file specified via 'file_path' and return its content - raises an ConuException if
        there is an issue accessing the file
        :param file_path: str, path to the file to read
        :return: str (not bytes), content of the file
        """
        try:
            with open(self.p(file_path)) as fd:
                return fd.read()
        except IOError as ex:
            logger.error("error while accessing file %s: %r", file_path, ex)
            raise ColinException("There was an error while accessing file %s: %r" % (file_path, ex))

    def get_file(self, file_path, mode="r"):
        """
        provide File object specified via 'file_path'
        :param file_path: str, path to the file
        :param mode: str, mode used when opening the file
        :return: File instance
        """
        return open(self.p(file_path), mode=mode)

    def file_is_present(self, file_path):
        """
        check if file 'file_path' is present, raises IOError if file_path
        is not a file
        :param file_path: str, path to the file
        :return: True if file exists, False if file does not exist
        """
        p = self.p(file_path)
        if not os.path.exists(p):
            return False
        if not os.path.isfile(p):
            raise IOError("%s is not a file" % file_path)
        return True

    @property
    def labels(self):
        """
        Provide labels without the need of dockerd. Instead skopeo and tar are being used.

        :return: dict
        """
        if self._labels is None:
            self._labels = self.metadata["config"]["Labels"]
        return self._labels


class ImageName(object):
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
