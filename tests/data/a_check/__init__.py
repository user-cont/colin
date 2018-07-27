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

from colin.core.checks.abstract_check import AbstractCheck


class FunkyCheck(AbstractCheck):
    name = "this-is-a-funky-check"

    def __init__(self):
        super(FunkyCheck, self).__init__(
            message="yes!",
            description="no",
            reference_url="https://nope.example.com/",
            tags=["yes", "and", "no"]
        )


class ThisIsNotAChekk(AbstractCheck):
    name = "this-is-not-a-check"

    def __init__(self):
        super(ThisIsNotAChekk, self).__init__(
            message="yes!",
            description="no",
            reference_url="https://nope.example.com/",
            tags=["yes", "and", "no"]
        )


class ThisIsAlsoNotAChekk(object):
    name = "this-is-also-not-a-check"

    def __init__(self):
        super(ThisIsAlsoNotAChekk, self).__init__(
            message="yes!",
            description="no",
            reference_url="https://nope.example.com/",
            tags=["yes", "and", "no"]
        )
