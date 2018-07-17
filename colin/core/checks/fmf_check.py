"""
Module handling FMF stored metadata for classes
"""

import copy
import re
import logging

from fmf import Tree
from .abstract_check import AbstractCheck
from ..ruleset.ruleset import get_checks_path


logger = logging.getLogger(__name__)


class ExtendedTree(Tree):
    """
    FMF Extension. Allows to use references via @ to another items -> usefull for rulesets
    """

    def __remove_append_items(self, whole=False):
        """
        internal method, delete all append items (ends with +)
        :param whole: pass thru 'whole' param to climb
        :return: None
        """
        for node in self.climb(whole=whole):
            for key in sorted(node.data.keys()):
                if key.endswith('+'):
                    del node.data[key]

    def references(self, patterntree, whole=False):
        """
        resolve references in names like /a/b/c/d@.x.y or /a/b/c/@y
        it uses simple references schema, do not use references to another references
        avoid usind / in reference because actual solution creates also this tree items.

        :param whole: pass thru 'whole' param to climb
        :param patterntree: original tree with testcases to contain parent nodes
        :return: None
        """
        reference_nodes = self.prune(whole=whole, names=["@"])
        for node in reference_nodes:
            node.data = node.original_data
            ref_item_name = node.name.rsplit("@", 1)[1]
            # match item what does not contain @ before name, otherwise it
            # match same item
            reference_node = patterntree.search("[^@]%s" % ref_item_name)
            logger.debug("MERGING: %s @ %s", node.name, reference_node.name)
            if not reference_node:
                raise ValueError("Unable to find reference for node: %s  via name search: %s" %
                                 (node.name, ref_item_name))
            node.merge(parent=reference_node)

        self.__remove_append_items(whole=whole)

    def search(self, name):
        """ Search node with given name based on regexp, basic method (find) uses equality"""
        for node in self.climb():
            if re.search(name, node.name):
                return node
        return None


class FMFCaseLoader(object):
    """
    search and load FMF metadata
    """

    def __init__(self, name_id, path=None):
        """
        Case loader metatada init, it try to gather metadata form FMF based on name identifier
        :param name_id:
        :param path:
        """
        self.metadata = self.__receive_fmf_metadata(
            path or get_checks_path(), name=name_id)
        self.name = self.get_name()

    def __receive_fmf_metadata(self, fmfpath, name=None, object_list=False):
        """
        internal method, search name in metadata in fmfpath

        :param fmfpath: path to filesystem
        :param name: str - name as pattern to search (substring)
        :param object_list: bool, if true, return whole list of found items
        :return: Tree Object or list
        """
        output = {}
        fmf_tree = ExtendedTree(fmfpath)
        logger.debug("get FMF metadata for test (path:%s name=%s)", fmfpath, name)
        items = [x for x in fmf_tree.climb(
        ) if name in x.name and "@" not in x.name]
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

    def get_name(self, full=False):
        """
        return FMF Name of item
        :param full: if True return full path identifier
        :return: str - name identifier
        """
        out = self.metadata.name
        if not full:
            out = self.metadata.name.rsplit("/", 1)[-1]
        return out


class FMFAbstractCheck(AbstractCheck):
    """
    Abstract class for checks and loading metadata from FMF format
    """
    metadata = None
    name = None

    @classmethod
    def get_metadata(cls, name, path=None):
        """
        Returns tuple for AbstractCheck objects initialization
        COLIN tool expects to have class attribute: name to be able to find cases

        :param name: str, identifier of name in FMF
        :param path: where to look for metadata
        :return: tuple, name, FMF metadata Tree
        """
        item = FMFCaseLoader(name_id=name, path=path)
        return item.name, item.metadata

    def __init__(self):
        """
        wraps parameters to COLIN __init__ method format
        """
        kwargs = copy.deepcopy(self.metadata.data)
        if "class" in kwargs:
            del kwargs["class"]
        if "test" in kwargs:
            del kwargs["test"]
        super(FMFAbstractCheck, self).__init__(**kwargs)
