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
from time import sleep

import pytest

from colin.core.exceptions import ColinException
from colin.utils.cmd_tools import exit_after


@exit_after(1)
def fast_fce():
    pass


@exit_after(1)
def slow_fce():
    sleep(2)


@exit_after(1)
def bad_fce():
    raise ColinException("Error")


def test_timeout_fast_fce():
    fast_fce()


def test_timeout_slow_fce():
    with pytest.raises(TimeoutError):
        slow_fce()


def test_timeout_bad_fce():
    with pytest.raises(ColinException):
        bad_fce()


def test_timeout_dirrect():
    with pytest.raises(TimeoutError):
        exit_after(1)(sleep)(2)
