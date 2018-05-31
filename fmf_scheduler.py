import os
import sys
import imp
import re
import logging
import unittest

from fmf import Tree
from colin.core.target import Target, is_compatible

LOG_LEVEL = 3
TARGET = Target(os.environ.get("TARGET"), LOG_LEVEL)
CHECKS = ["colin/checks"]

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)

class ExtendedTree(Tree):
    def __init__(self, *args, **kwargs):
        super(ExtendedTree, self).__init__(*args, **kwargs)

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
        avoid usind / in reference because actual solution creates also this tree items
        it is bug or feature, who knows :-)
        :param whole: pass thru 'whole' param to climb
        :param patterntree: original tree with testcases to contain parent nodes
        :return: None
        """
        reference_nodes = self.prune(whole=whole, names=["@"])
        for node in reference_nodes:
            node.data = node.original_data
            ref_item_name =  node.name.rsplit("@", 1)[1]
            # match item what does not contain @ before nema, otherwise it match same item
            reference_node = patterntree.search("[^@]%s" % ref_item_name)
            logger.debug("MERGING: {} @ {}".format(node.name, reference_node.name))
            if not reference_node:
                raise ValueError("Unable to find reference for node: %s  via name search: %s" %
                                 (node.name, ref_item_name))
            node.merge(parent=reference_node)

        self.__remove_append_items(whole=whole)

    def search(self, name):
        """ Search node with given name based on reqexp"""
        for node in self.climb():
            if re.search(name, node.name):
                return node
        return None

# COPYied from: https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class DynamicClassBase(unittest.TestCase):
    longMessage = True


def make_check_function():
    """
    rename check function to test, to be able to find this function via testing frameworks
    :return: function
    """
    def test(self):
        self.backendclass().check(TARGET)
    return test


def class_fmf_generator(fmfpaths):
    """
    generates dynamic test classes for nosetest or unittest scheduler based on FMF metadata.
    :param fmfpaths:
    :return:
    """
    test_classes = {}
    for fmfpath in fmfpaths:
        metadatatree = ExtendedTree(fmfpath)
        metadatatree.references(metadatatree)
        for node in metadatatree.climb():
            if node.data.get("class") or node.data.get("test"):

                first_class_name = node.name.rsplit("/", 1)[1]
                second_class_name = node.data.get("class")
                logger.debug("searching for {}".format(node.name))
                modulepath = os.path.join(os.path.dirname(node.sources[-1]), node.data["test"])
                modulename = os.path.basename(node.sources[-1]).split(".", 1)[0]
                # in case of referencing  use original data tree for info
                if "@" in node.name and not os.path.exists(modulepath):
                    modulepath = os.path.join(os.path.dirname(node.sources[-2]), node.data["test"])
                    modulename = os.path.basename(node.sources[-2]).split(".", 1)[0]
                test_func = make_check_function()
                moduleimp = imp.load_source(modulename, modulepath)
                inernalclass = getattr(moduleimp, second_class_name)
                if is_compatible(target_type=TARGET.target_type, check_instance=inernalclass()):
                    # more verbose output
                    #full_class_name = '{0}_{1}'.format(first_class_name, second_class_name)
                    full_class_name = '{0}'.format(first_class_name)
                    oneclass = type(full_class_name, (DynamicClassBase,), {'test': test_func})
                    oneclass.backendclass = inernalclass
                    test_classes[full_class_name] = oneclass
                    logger.info("Test added: {}".format(node.name))
                else:
                    logger.info("Test (not target): {}".format(node.name))
    return test_classes


classes = class_fmf_generator(CHECKS)
logger.info("number of test classes: {}".format(len(classes)))

for item in classes:
    globals()[item] = classes[item]


