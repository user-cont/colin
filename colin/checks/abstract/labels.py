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

from .containers import ContainerCheck
from .images import ImageCheck
from ..result import CheckResult


class LabelCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, label, required, value_regex=None):
        super().__init__(name, message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        labels = target.instance.get_metadata()["Config"]["Labels"]
        present = labels is not None and self.label in labels

        if present:
            if self.required and not self.value_regex:
                passed = True
            elif self.value_regex:
                pattern = re.compile(self.value_regex)
                passed = bool(pattern.match(labels[self.label]))
            else:
                passed = False

        else:
            passed = not self.required

        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
