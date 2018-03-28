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

import six

if six.PY3:
    import inspect

    from importlib.util import module_from_spec
    from importlib.util import spec_from_file_location
    import logging

    from colin.core.constant import MODULE_NAME_IMPORTED_CHECKS

    logger = logging.getLogger(__name__)


    def load_check_implementation(path, severity):
        logger.debug("Getting check(s) from the file '{}'.".format(path))

        s = spec_from_file_location(MODULE_NAME_IMPORTED_CHECKS, path)
        m = module_from_spec(s)
        s.loader.exec_module(m)
        check_classes = []
        for name, obj in inspect.getmembers(m, inspect.isclass):
            if obj.__module__ == MODULE_NAME_IMPORTED_CHECKS:
                new_check = obj()
                new_check.severity = severity
                check_classes.append(new_check)
        return check_classes

else:
    def load_check_implementation(path):
        raise NotImplementedError()
