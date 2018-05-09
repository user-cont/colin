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
import sys
import warnings

import six

logger = logging.getLogger(__name__)


def path_to_module(path, top_path):
    if top_path not in path:
        raise RuntimeError("path {} is not placed in a dir {}".format(path, top_path))
    mo = path[len(top_path):]
    import_name = mo.replace("/", ".")
    if import_name[0] == ".":
        import_name = import_name[1:]
    if import_name.endswith(".py"):
        import_name = import_name[:-3]
    return import_name


def _load_module(path, top_path):
    module_name = path_to_module(path, top_path)
    logger.debug("Will try to load selected file as module '%s'.", module_name)
    if six.PY3:
        from importlib.util import module_from_spec
        from importlib.util import spec_from_file_location

        s = spec_from_file_location(module_name, path)
        m = module_from_spec(s)
        s.loader.exec_module(m)
        return m

    elif six.PY2:
        import imp

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # FIXME: let's at least debug log other warnings
            m = imp.load_source(module_name, path)
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
    for m in mro:
        if m.__name__ == "AbstractCheck":
            return True
    return False


def load_check_classes_from_file(path, top_path):
    logger.debug("Getting check(s) from the file '{}'.".format(path))
    m = _load_module(path, top_path)

    check_classes = []
    for name, obj in inspect.getmembers(m, inspect.isclass):
        if should_we_load(obj):
            check_classes.append(obj)
            logger.debug("Check class '{}' found.".format(obj.__name__))
    return check_classes


class CheckLoader(object):
    """
    find recursively all checks on a given path
    """
    def __init__(self, path):
        """
        :param path: str, path to a file or a dir where check classes are present
        """
        logger.debug("Will load checks from path '{}'.".format(path))
        self._check_classes = None
        self._mapping = None
        self.path = path
        for p in sys.path:
            if p in self.path:
                self.top_py_path = p
                break
        else:
            self.top_py_path = path
            sys.path.insert(0, path)
            logger.debug("%s is not on pythonpath, added it", path)

    def obtain_check_classes(self):
        """ find children of AbstractCheck class and return them as a list """
        check_classes = set()
        if os.path.isfile(self.path):
            return load_check_classes_from_file(self.path, self.top_py_path)
        for root, dirs, files in os.walk(self.path):
            for fi in files:
                if fi.endswith(".pyc"):
                    continue
                path = os.path.join(root, fi)
                check_classes = check_classes.union(set(
                    load_check_classes_from_file(path, self.top_py_path)))
        return list(check_classes)

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
                try:
                    i = c()
                except Exception as ex:
                    logger.debug("Can't instantiate check %s: %s", c.__name__, ex)
                    continue
                self._mapping[i.name] = i
        return self._mapping
