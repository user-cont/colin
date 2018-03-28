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

from .abstract_check import AbstractCheck


class DockerfileCheck(AbstractCheck):
    pass


class InstructionCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, regex, required):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.regex = regex
        self.required = required

    def check(self, target):
        pass


class InstructionCountCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, min_count=None, max_count=None):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.min_count = min_count
        self.max_count = max_count

    def check(self, target):
        pass
