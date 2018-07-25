"""
Module with FMF abstract check class
"""

import copy
import logging

from .abstract_check import AbstractCheck
from ..fmf_extension import ExtendedTree

logger = logging.getLogger(__name__)


def receive_fmf_metadata(name, path, object_list=False):
    """
    search node identified by name fmfpath

    :param path: path to filesystem
    :param name: str - name as pattern to search (substring)
    :param object_list: bool, if true, return whole list of found items
    :return: Tree Object or list
    """
    output = {}
    fmf_tree = ExtendedTree(path)
    logger.debug("get FMF metadata for test (path:%s name=%s)", path, name)
    # ignore items with @ in names, to avoid using unreferenced items
    items = [x for x in fmf_tree.climb() if name in x.name and "@" not in x.name]
    if object_list:
        return items
    if len(items) == 1:
        output = items[0]
    elif len(items) > 1:
        raise Exception("There is more FMF test metadata for item by name:{}({}) {}".format(
            name, len(items), [x.name for x in items]))
    elif not items:
        raise Exception("Unable to get FMF metadata for: {}".format(name))
    return output


class FMFAbstractCheck(AbstractCheck):
    """
    Abstract class for checks and loading metadata from FMF format
    """
    metadata = None
    name = None
    fmf_metadata_path = None

    def __init__(self):
        """
        wraps parameters to COLIN __init__ method format
        """
        if not self.metadata:
            self.metadata = receive_fmf_metadata(name=self.name, path=self.fmf_metadata_path)
        kwargs = copy.deepcopy(self.metadata.data)
        if "class" in kwargs:
            del kwargs["class"]
        if "test" in kwargs:
            del kwargs["test"]
        super(FMFAbstractCheck, self).__init__(**kwargs)
