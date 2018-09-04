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
import re

from .abstract_check import AbstractCheck
from .check_utils import check_label
from ..result import CheckResult

logger = logging.getLogger(__name__)


def get_instructions_from_dockerfile_parse(dfp, instruction):
    """
    Get the list of instruction dictionary for given instruction name.
    (Subset of DockerfileParser.structure only for given instruction.)

    :param dfp: DockerfileParser
    :param instruction: str
    :return: list
    """
    return [inst for inst in dfp.structure if inst["instruction"] == instruction]


class DockerfileAbstractCheck(AbstractCheck):
    check_type = "dockerfile"


class InstructionAbstractCheck(DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, instruction, value_regex,
                 required):
        super(InstructionAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.instruction = instruction
        self.value_regex = value_regex
        self.required = required

    def check(self, target):
        instructions = get_instructions_from_dockerfile_parse(target.instance, self.instruction)
        pattern = re.compile(self.value_regex)
        logs = []
        passed = True
        for inst in instructions:
            match = bool(pattern.match(inst["value"]))
            passed = match == self.required
            log = "Value for instruction {} " \
                  "{}mach regex: '{}'.".format(inst["content"],
                                               "" if match else "does not ",
                                               self.value_regex)
            logs.append(log)
            logger.debug(log)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=logs)


class InstructionCountAbstractCheck(DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, instruction, min_count=None,
                 max_count=None):
        super(InstructionCountAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.instruction = instruction
        self.min_count = min_count
        self.max_count = max_count

    def check(self, target):
        count = len(get_instructions_from_dockerfile_parse(target.instance, self.instruction))

        log = "Found {} occurrences of the {} instruction. Needed: min {} | max {}" \
            .format(count,
                    self.instruction,
                    self.min_count,
                    self.max_count)
        logger.debug(log)
        passed = True
        if self.min_count is not None:
            passed = passed and self.min_count <= count
        if self.max_count is not None:
            passed = passed and count <= self.max_count

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[log])


class DockerfileLabelAbstractCheck(DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, label, required,
                 value_regex=None):
        super(DockerfileLabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        labels = target.instance.labels
        passed = check_label(labels=self.label,
                             required=self.required,
                             value_regex=self.value_regex,
                             target_labels=labels)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
