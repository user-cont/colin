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
import re

from conu import ConuException

from ..exceptions import ColinException
from ..result import CheckResult, FailedCheckResult
from .containers import ContainerCheck
from .images import ImageCheck


class CmdCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, cmd, expected_output=None,
                 expected_regex=None,
                 substring=None):
        super().__init__(name, message, description, reference_url, tags)
        self.cmd = cmd
        self.expected_output = expected_output
        self.expected_regex = expected_regex
        self.substring = substring

    def check(self, target):

        try:
            output = target.get_output(cmd=self.cmd)
        except ConuException as ex:
            if str(ex).endswith("exit code 126") or str(ex).endswith("error: 127"):
                return CheckResult(ok=False,
                                   description=self.description,
                                   message=self.message,
                                   reference_url=self.reference_url,
                                   check_name=self.name,
                                   logs=["exec: '{}': executable file not found in $PATH".format(self.cmd)])
            else:
                return FailedCheckResult(check=self,
                                         logs=[str(ex)])
        except ColinException as ex:
            return FailedCheckResult(check=self,
                                     logs=[str(ex)])
        passed = True
        logs = ["Output:\n{}".format(output)]
        if self.substring is not None:
            substring_present = self.substring in output
            passed = passed and substring_present
            logs.append("{}: Substring '{}' is {}present in the output of the command '{}'." \
                        .format("ok" if substring_present else "nok",
                                self.substring,
                                "" if substring_present else "not ",
                                self.cmd))

        if self.expected_output is not None:
            expected_output = self.expected_output == output
            if expected_output:
                logs.append("ok: Output of the command '{}' was as expected." \
                            .format(self.cmd))
            else:
                logs.append("nok: Output of the command '{}' does not match the expected one: '{}'." \
                            .format(self.cmd, self.expected_output))

                passed = False

        if self.expected_regex is not None:
            pattern = re.compile(self.expected_regex)
            if pattern.match(output):
                logs.append("ok: Output of the command '{}' match the regex '{}'." \
                            .format(self.cmd, self.expected_regex))
            else:
                logs.append("nok: Output of the command '{}' does not match the expected regex: '{}'." \
                            .format(self.cmd, self.expected_regex))

                passed = False

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=logs)
