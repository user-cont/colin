"""
Module handling FMF stored metadata for classes
"""

import logging
import re

from fmf import Tree

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

    def references(self, datatree, whole=False):
        """
        Reference name resolver (eg. /a/b/c/d@.x.y or /a/b/c/@y will search data in .x.y or y nodes)
        there are used regular expressions (re.search) to match names
        it uses simple references schema, do not use references to another references,
        avoid usind / in reference because actual solution creates also these tree items.

        datatree contains for example data like (original check data)
        /dockerfile/maintainer_check:
          class: SomeClass
          tags: [dockerfile]

        and reference could be like (ruleset)
        /default/check1@maintainer_check:
           tags+: [required]

        will produce output (output ruleset tree):
        /default/check1@maintainer_check:
          class: SomeClass
          tags: [dockerfile, required]


        :param whole: 'whole' param of original climb method, in colin this is not used anyhow now
                      iterate over all items not only leaves if True
        :param datatree: original tree with testcases to contain parent nodes
        :return: None
        """
        reference_nodes = self.prune(whole=whole, names=["@"])
        for node in reference_nodes:
            node.data = node.original_data
            ref_item_name = node.name.rsplit("@", 1)[1]
            # match item what does not contain @ before name, otherwise it
            # match same item
            reference_node = datatree.search("[^@]%s" % ref_item_name)
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
