# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
This piece of code searches for python code on specific path and
loads AbstractCheck classes from it.
"""

import inspect
import logging
import os
from importlib import import_module
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

from ..core.checks.fmf_check import receive_fmf_metadata, FMFAbstractCheck

logger = logging.getLogger(__name__)


def path_to_module(path):
    if path.endswith(".py"):
        path = path[:-3]
    cleaned_path = path.replace(".", "").replace("-", "_")
    path_comps = cleaned_path.split(os.sep)[-2:]
    import_name = ".".join(path_comps)
    if import_name[0] == ".":
        import_name = import_name[1:]
    return import_name


def _load_module(path):
    module_name = path_to_module(path)
    logger.debug("Will try to load selected file as module '%s'.", module_name)

    s = spec_from_file_location(module_name, path)
    m = module_from_spec(s)
    s.loader.exec_module(m)
    return m


def should_we_load(kls):
    """ should we load this class as a check? """
    # we don't load abstract classes
    if kls.__name__.endswith("AbstractCheck"):
        return False
    # and we only load checks
    if not kls.__name__.endswith("Check"):
        return False
    mro = kls.__mro__
    # and the class needs to be a child of AbstractCheck
    for m in mro:
        if m.__name__ == "AbstractCheck":
            return True
    return False


def load_check_classes_from_file(path):
    logger.debug("Getting check(s) from the file '{}'.".format(path))
    m = _load_module(path)

    check_classes = []
    for _, obj in inspect.getmembers(m, inspect.isclass):
        if should_we_load(obj):
            if issubclass(obj, FMFAbstractCheck):
                node_metadata = receive_fmf_metadata(name=obj.name, path=os.path.dirname(path))
                obj.metadata = node_metadata
            check_classes.append(obj)
            # Uncomment when debugging this code.
            logger.debug("Check class '%s' loaded, module: '%s'", obj.__name__, obj.__module__)
    return check_classes


class CheckLoader(object):
    """
    find recursively all checks on a given path
    """

    def __init__(self, checks_paths):
        """
        :param checks_paths: list of str, directories where the checks are present
        """
        logger.debug("Will load checks from paths '%s'.", checks_paths)
        for p in checks_paths:
            if os.path.isfile(p):
                raise RuntimeError("Provided path %s is not a directory." % p)
        self._check_classes = None
        self._mapping = None
        self.paths = checks_paths

    def obtain_check_classes(self):
        """ find children of AbstractCheck class and return them as a list """
        check_classes = set()
        for path in self.paths:
            for root, _, files in os.walk(path):
                for fi in files:
                    if not fi.endswith(".py"):
                        continue
                    path = os.path.join(root, fi)
                    check_classes = check_classes.union(set(
                        load_check_classes_from_file(path)))
        return list(check_classes)

    def import_class(self, import_name):
        """
        import selected class

        :param import_name, str, e.g. some.module.MyClass
        :return the class
        """
        module_name, class_name = import_name.rsplit(".", 1)
        mod = import_module(module_name)
        check_class = getattr(mod, class_name)
        self.mapping[check_class.name] = check_class
        logger.info("successfully loaded class %s", check_class)
        return check_class

    @property
    def check_classes(self):
        if self._check_classes is None:
            self._check_classes = self.obtain_check_classes()
        return self._check_classes

    @property
    def mapping(self):
        if self._mapping is None:
            self._mapping = {}
            for c in self.check_classes:
                self._mapping[c.name] = c
        return self._mapping
