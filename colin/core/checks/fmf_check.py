"""
Module with FMF abstract check class
"""

import copy
import logging
import inspect

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
        master_class = super(FMFAbstractCheck, self)
        kwargs = {}
        try:
            # this is not available in python2, but second function is deprecated
            args_names = [argument for argument in inspect.signature(master_class.__init__).parameters]
        except NameError:
            args_names = inspect.getargspec(master_class.__init__).args
        for arg in args_names:
            # copy all arguments from metadata.data to class __init__  kwargs
            try:
                kwargs[arg] = self.metadata.data[arg]
            except KeyError:
                pass
        try:
            master_class.__init__(**kwargs)
        except TypeError as error:
            logger.debug("missing argument (%s) in FMF metadata key (%s): %s",
                         error,
                         self.metadata.name,
                         self.metadata.data)
