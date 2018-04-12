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
import logging

from .labels import check_label
from ..result import CheckResult
from .abstract_check import AbstractCheck

logger = logging.getLogger(__name__)


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


class InstructionCountCheck(DockerfileCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, min_count=None, max_count=None):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.min_count = min_count
        self.max_count = max_count

    def check(self, target):
        count = 0
        for instruction in target.instance.structure:
            if instruction["instruction"] == self.instruction:
                count += 1
        log = "Found {} occurrences of the {} instruction. Needed: min {} | max {}".format(self.instruction,
                                                                                             count,
                                                                                             self.min_count,
                                                                                             self.max_count)
        logger.debug(log)
        passed = True
        if self.min_count:
            passed = passed and self.min_count <= count
        if self.max_count:
            passed = passed and count <= self.max_count

        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[log])


class DockerfileLabelCheck(DockerfileCheck):

    def __init__(self, name, message, description, reference_url, tags, label, required, value_regex=None):
        super().__init__(name, message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        labels = target.instance.labels
        passed = check_label(label=self.label,
                             required=self.required,
                             value_regex=self.value_regex,
                             labels=labels)

        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
