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

import os
import shutil

from colin import checks
from colin.core.loader import CheckLoader


def test_upstream_checks_can_be_loaded():
    """ check whether all upstream checks can be loaded """
    colin_checks_path = checks.__file__
    colin_checks_dir = os.path.dirname(colin_checks_path)
    l = CheckLoader(colin_checks_dir)
    assert l.check_classes
    assert l.mapping["bzcomponent_deprecated"]


def test_loading_custom_check(tmpdir):
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    a_check_dir = os.path.join(tests_dir, "data", "a_check")
    shutil.copytree(a_check_dir, str(tmpdir.join("a_check")))
    l = CheckLoader(str(tmpdir))
    assert len(l.check_classes) == 1
