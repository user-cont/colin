#!/usr/bin/python3
"""
FMF scheduler via unittest testcases.
Can be used as cli or as an argument to external scheduler like nosetest.
Found test via fmf files and creates dynamic testclassed based on that.
"""


import os
import sys
import imp
import logging
import unittest
import click

from colin.core.target import Target, is_compatible
from colin.core.checks.fmf_check import ExtendedTree, FMFAbstractCheck
from colin.core.constant import PASSED, COLIN_CHECKS_PATH
from colin.core.ruleset.ruleset import get_checks_paths

from colin.core.checks.dockerfile import DockerfileAbstractCheck, DockerfileLabelAbstractCheck,\
    InstructionCountAbstractCheck, InstructionAbstractCheck

CLASS_MAPPING = {"DockerfileAbstractCheck": DockerfileAbstractCheck,
                 "DockerfileLabelAbstractCheck": DockerfileLabelAbstractCheck,
                 "InstructionCountAbstractCheck": InstructionCountAbstractCheck,
                 "InstructionAbstractCheck": InstructionAbstractCheck
                 }
logger = logging.getLogger(__name__)


def get_log_level():
    return int(os.environ.get(("DEBUG")) or logging.INFO)


# COPYied from:
# https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class DynamicClassBase(unittest.TestCase):
    """
    Basic Derived test Class
    """
    backendclass = None
    longMessage = True


def make_check_function(target):
    """
    rename check function to test, to be able to find this function via testing frameworks
    :return: function
    """

    def test(self):
        out = self.backendclass().check(target)
        if out.status is not PASSED:
            raise AssertionError("test:{} -> {}".format(
                self.backendclass.name,
                str(out))
            )
    return test


def make_base_fmf_class_abstract(node, target, base_class=DynamicClassBase, fmf_class=FMFAbstractCheck):
    """
    Generate test classes without python dedicated classes (new)
    it creates class like:

    class SomeClassName(DynamicClassBase):
        backend = FMFAbstractCheck_inherited_class
        def test():
            backend.check(TARGET)


    :param node: fmf metadata item
    :param target: test subject class
    :param base_class: optional parameter, to override base class for inheritance
    :param fmf_class: base fmf class, have to be set via CLASS_MAPPING
    :return: unittest inherited class
    """
    class_name = node.data["class"]
    out_class_name = node.name.rsplit("/", 1)[-1]
    outclass = type(out_class_name, (base_class,), {
        'test': make_check_function(target=target),
        'backendclass': type(class_name, (fmf_class, CLASS_MAPPING[class_name],), {
            '__doc__': node.data.get("description"),
            'name': out_class_name,
            'metadata': node,
        })
    })
    return outclass


def make_wrapped_fmf_class(node, target):
    """
    It creates class like:

    class SomeClassName(DynamicClassBase):
        backend = FMFAbstractCheck_inherited_class
        def test():
            backend.check(TARGET)

    :param node: fmf metadata item
    :param target: test subject class
    :return: unittest inherited class
    """
    first_class_name = node.name.rsplit("/", 1)[-1]
    second_class_name = node.data.get("class")
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
    logger.debug("Try to import: %s from path %s", modulename, modulepath)
    moduleimp = imp.load_source(modulename, modulepath)
    inernalclass = getattr(moduleimp, second_class_name)
    inernalclass.name = node.name
    inernalclass.metadata = node
    # more verbose output
    # full_class_name = '{0}_{1}'.format(first_class_name, second_class_name)
    full_class_name = '{0}'.format(first_class_name)
    return type(full_class_name, (DynamicClassBase,), {'test': test_func,
                                                       'backendclass': inernalclass
                                                       })


def unittests_class_fmf_generator(fmfpathes, target_name, log_level, ruleset_tree_path=None, filter_names=None, filters=None):
    """
    generates dynamic test unittest classes based on FMF metadata.

    :param fmfpathes: path to checks
    :param target_name: what is the target object
    :param log_level:
    :param ruleset_tree_path:
    :return:
    """
    target = Target(target_name, log_level)
    test_classes = {}
    metadata_forest = []
    if ruleset_tree_path:
        ruleset_mtd = ExtendedTree(ruleset_tree_path)
        source_metadata_trees = [ExtendedTree(fmfpath) for fmfpath in fmfpathes]
        ruleset_mtd.references(datatrees=source_metadata_trees)
        metadata_forest = [ruleset_mtd]
    else:
        metadata_forest = [ExtendedTree(fmfpath) for fmfpath in fmfpathes]
    for metadata_item in metadata_forest:
        for node in metadata_item.prune(names=filter_names, filters=filters):
            if node.data.get("class") or node.data.get("test"):
                logger.debug("node (%s) contains test and class item", node.name)

                if node.data.get("class") in CLASS_MAPPING:
                    logger.debug("Using pure FMF metadata for %s (class %s)", node.name, node.data.get("class"))
                    test_class = make_base_fmf_class_abstract(node=node, target=target)
                else:
                    logger.debug("searching for %s", node.name)
                    test_class = make_wrapped_fmf_class(node=node, target=target)
                if is_compatible(target_type=target.target_type, check_instance=test_class.backendclass()):
                    test_classes[test_class.__name__] = test_class
                    logger.debug("Test added: %s", node.name)
                else:
                    logger.debug("Test (not target): %s", node.name)
            else:
                if "__pycache__" not in node.name:
                    logger.warning("error in fmf config for node (missing test and class items): %s (data: %s) ", node.name, node.data)
    return test_classes


def scheduler_opts(target_name=None, checks=None, ruleset_path=None,
                   filter_names=None, filters=None, log_level=None):
    """
    gather all options what have to be set for function class_fmf_generator
    now it is able set via ENVVARS

    :param target_name: override envvar TARGET
    :param checks: override envvar CHECKS
    :param ruleset_path: path to directory, where are fmf rulesets
    :param filters: dict of filters, filter out just selected cases, use FMF filter format,
           via FILTER envvar use ";" as filter separator
    :param filter_names: dict of item names for filtering user ";" as separator for NAMES envvar
    :return: dict of test classes
    """
    if not target_name:
        target_name = os.environ.get("TARGET")
        if not target_name:
            raise EnvironmentError("TARGET envvar is not set.")
    if not checks:
        checks = get_checks_paths()
    if not ruleset_path:
        ruleset_path = os.environ.get("RULESETPATH")
    if not filters:
        filters = os.environ.get("FILTERS", "").split(";")
    if not filter_names:
        filter_names = os.environ.get("NAMES", "").split(";")
    if not log_level:
        log_level = get_log_level()
    output = unittests_class_fmf_generator(checks, target_name,
                                           ruleset_tree_path=ruleset_path,
                                           filter_names=filter_names,
                                           filters=filters,
                                           log_level=log_level)
    return output

@click.command()
@click.argument('target', type=click.STRING)
@click.option('checks_paths', '-c', '--checks-paths',
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              multiple=True, envvar=COLIN_CHECKS_PATH, default=get_checks_paths(),
              help="Path to directory containing checks (default {}).".format(get_checks_paths()))
@click.option('ruleset_dir', '--ruleset-dir', '-r', type=click.Path(),
              help="Path to a directory with rulesets")
@click.option('--name', '-n', multiple=True, type=click.STRING,
              help="Select cases by key names")
@click.option('filter_opts','--filter', '-f', multiple=True, type=click.STRING,
              help="Filter cases based on FMF filter rules")
@click.option('-v', '--verbose', type=click.INT, default=0,
              help="change verbosity of unittest scheduler")
@click.option('--debug', default=False, is_flag=True,
              help="Enable debugging mode (debugging logs, full tracebacks).")
def cmdline(target, checks_paths, ruleset_dir, name, filter_opts, verbose, debug):
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(stream=sys.stdout, level=log_level)
    test_classes = scheduler_opts(target_name=target, checks=checks_paths, ruleset_path=ruleset_dir,
                   filter_names=name, filters=filter_opts, log_level=log_level)
    loader = unittest.TestLoader()
    tests = [loader.loadTestsFromTestCase(test) for test in test_classes.values()]
    suite = unittest.TestSuite(tests)

    runner = unittest.TextTestRunner(verbosity=verbose)
    runner.run(suite)


if __name__ == "__main__":
    cmdline()
else:
    # when used as an testsuite set all classes globals, you can then invoke it eg:
    # TARGET=tests/data/Dockerfile nosetests fmf_scheduler.py
    classes = scheduler_opts()
    for item in classes:
        globals()[item] = classes[item]
