#!/usr/bin/python3
"""
FMF scheduler for nosetests
Found test via fmf files and creates dynamic testclassed based on that.
"""


import os
import sys
import imp
import logging
import unittest

from colin.core.target import Target, is_compatible
from colin.core.checks.fmf_check import ExtendedTree

LOG_LEVEL = 3
CHECKS = ["colin/checks"]
logger = logging.getLogger(__name__)


# COPYied from:
# https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class DynamicClassBase(unittest.TestCase):
    """
    Basic Derived test Class
    """
    longMessage = True


def make_check_function(target):
    """
    rename check function to test, to be able to find this function via testing frameworks
    :return: function
    """

    def test(self):
        """
        Generic test function wrapper, it calls self.check(target)

        :param self: it is function what will be incorporated to class
        :return:
        """
        self.backendclass().check(target)
    return test


def class_fmf_generator(fmfpaths, target_name, log_level=LOG_LEVEL):
    """
    generates dynamic test classes for nosetest or unittest scheduler based on FMF metadata.
    :param fmfpaths:
    :return:
    """
    target = Target(target_name, log_level)
    test_classes = {}
    for fmfpath in fmfpaths:
        metadatatree = ExtendedTree(fmfpath)
        metadatatree.references(metadatatree)
        for node in metadatatree.climb():
            logger.debug("look at node: %s ", node)
            if node.data.get("class") or node.data.get("test"):
                logger.debug("node (%s) contains test and class item", node)
                first_class_name = node.name.rsplit("/", 1)[-1]
                second_class_name = node.data.get("class")
                logger.debug("searching for %s", first_class_name)
                modulepath = os.path.join(os.path.dirname(
                    node.sources[-1]), node.data["test"])
                modulename = os.path.basename(
                    node.sources[-1]).split(".", 1)[0]
                # in case of referencing  use original data tree for info
                if "@" in node.name and not os.path.exists(modulepath):
                    modulepath = os.path.join(os.path.dirname(
                        node.sources[-2]), node.data["test"])
                    modulename = os.path.basename(
                        node.sources[-2]).split(".", 1)[0]
                test_func = make_check_function(target=target)
                logger.info("Try to import: %s from path %s", modulename, modulepath)
                moduleimp = imp.load_source(modulename, modulepath)
                inernalclass = getattr(moduleimp, second_class_name)
                if is_compatible(target_type=target.target_type, check_instance=inernalclass()):
                    # more verbose output
                    #full_class_name = '{0}_{1}'.format(first_class_name, second_class_name)
                    full_class_name = '{0}'.format(first_class_name)
                    oneclass = type(full_class_name, (DynamicClassBase,), {'test': test_func})
                    oneclass.backendclass = inernalclass
                    test_classes[full_class_name] = oneclass
                    logger.info("Test added: %s", node.name)
                else:
                    logger.info("Test (not target): %s", node.name)
    return test_classes

def scheduler_opts(target_name=None, checks=None):
    """
    gather all options what have to be set for function class_fmf_generator
    now it is able set via ENVVARS

    :param target_name: override envvar TARGET
    :param checks: override envvar CHECKS
    :return: dict of test classes
    """
    if not target_name:
        target_name = os.environ.get("TARGET")
        if not target_name:
            raise EnvironmentError("TARGET envvar is not set.")
    if not checks:
        if os.environ.get("CHECKS"):
            checks = os.environ.get("CHECKS").split(":")
        else:
            checks = CHECKS
    output = class_fmf_generator(checks, target_name)
    return output



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL)
    classes = scheduler_opts()
    for item in classes:
        globals()[item] = classes[item]

    # try to schedule it via nosetests in case of direct schedule
    import nose
    logger.info("number of test classes: %s", len(classes))
    module_name = sys.modules[__name__].__file__
    logging.debug("running nose for package: %s", module_name)
    result = nose.run(argv=[sys.argv[0], module_name, '-v'])
    logging.info("all tests ok: %s", result)
else:
    classes = scheduler_opts()
    for item in classes:
        globals()[item] = classes[item]
