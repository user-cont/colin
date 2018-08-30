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


def extract_file_from_tarball(tarball_path, file_path, wd):
    """
    Extract selected file (file_path) from tarball (tarball_path) within a selected
    directory (wd).
    """
    tar_cmd = ["tar", "-xf", tarball_path, file_path]
    run_and_log(tar_cmd, None, "Failed to extract selected tarball.", wd)


class Image(object):
    """ Image representation using skopeo, ostree and atomic tool """

    def __init__(self, image_name, pull, insecure=False, iz_dockertar=False, iz_ostree=False):
        """
        :param image_name: str, name of the image to access
        :param pull: bool, pull the image from registry or from local dockerd
        :param insecure: bool, pull from an insecure registry (HTTP/invalid TLS)
        :param iz_dockertar: bool, is the target a path to docker tarball?
        :param iz_ostree: bool, is the target a directory with an ostree repo?
        """
        self.image_name = image_name
        self.ref_image_name = None  # we'll use this one when using skopeo or atomic
        self.pull = pull
        self.iz_dockertar = iz_dockertar
        self.iz_ostree = iz_ostree
        self._tmpdir = None
        self._mount_point = None
        self._ostree_path = None
        self._layers_path = None
        self.insecure = insecure

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
            subprocess.check_call(["ostree", "init", "--mode", "bare-user-only",
                                   "--repo", self._ostree_path])
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
        # FIXME: this code is absolutely horrid and should be cut to separate classes and
        #        moved to conu; I just wanted to prototype it over here and once proven working
        #        figure out how to move it to conu
        skopeo_extra_args = []
        if self.iz_dockertar:
            skopeo_source = "docker-archive:" + self.image_name
            self.ref_image_name = os.path.splitext(os.path.basename(self.image_name))[0]
        elif self.iz_ostree:
            skopeo_source = None
            if self.image_name.startswith("ostree:"):
                self.image_name = self.image_name[7:]
            try:
                self.ref_image_name, self._ostree_path = self.image_name.split("@", 1)
            except ValueError:
                raise RuntimeError("Invalid ostree target: should be 'image@path'.")
        else:
            image_name = ImageName.parse(self.image_name)
            # atomic is confused when the image lives in multiple storages, or what
            self.ref_image_name = 'colin-' + image_name.repository
            if self.pull:
                skopeo_source = "docker://" + image_name.name
                if self.insecure:
                    skopeo_extra_args.append("--src-tls-verify=false")
            else:
                skopeo_source = "docker-daemon:" + image_name.name

        skopeo_target = "ostree:%s@%s" % (self.ref_image_name, self.ostree_path)
        if skopeo_source:
            cmd = ["skopeo", "copy"] + skopeo_extra_args + [skopeo_source, skopeo_target]
            run_and_log(cmd, None,
                        "Failed to pull selected container image. Does it exist?")

        cmd = ["skopeo", "inspect", skopeo_target]
        self._labels = json.loads(subprocess.check_output(cmd))["Labels"]

    def _checkout(self):
        """ check out the image filesystem on self.mount_point """
        if self.insecure:
            image_name = 'http:' + self.ref_image_name
        else:
            image_name = self.ref_image_name
        cmd = ["atomic", "mount", "--storage", "ostree", image_name, self.mount_point]
        # self.mount_point has to be created by us
        run_and_log(cmd, self.ostree_path, "Failed to mount selected image as an ostree repo.")

    def clean_up(self):
        cmd = ["atomic", "unmount", self.mount_point]
        run_and_log(cmd, self.ostree_path, "Failed to unmount ostree checkout.")
        shutil.rmtree(self.tmpdir)

    def cont_path(self, path):
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
            with open(self.cont_path(file_path)) as fd:
                return fd.read()
        except IOError as ex:
            logger.error("error while accessing file %s: %r", file_path, ex)
            raise ColinException(
                "There was an error while accessing file %s: %r" % (file_path, ex))

    def get_file(self, file_path, mode="r"):
        """
        provide File object specified via 'file_path'
        :param file_path: str, path to the file
        :param mode: str, mode used when opening the file
        :return: File instance
        """
        return open(self.cont_path(file_path), mode=mode)

    def file_is_present(self, file_path):
        """
        check if file 'file_path' is present, raises IOError if file_path
        is not a file
        :param file_path: str, path to the file
        :return: True if file exists, False if file does not exist
        """
        p = self.cont_path(file_path)
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
