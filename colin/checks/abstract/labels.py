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


def check_label(label, required, value_regex, labels):
    present = labels is not None and label in labels

    if present:
        if required and not value_regex:
            return True
        elif value_regex:
            pattern = re.compile(value_regex)
            return bool(pattern.match(labels[label]))
        else:
            return False

    else:
        return not required


class LabelCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, label, required, value_regex=None):
        super().__init__(name, message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        labels = target.instance.get_metadata()["Config"]["Labels"]
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


class DeprecatedLabelCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, old_label, new_label):
        super().__init__(name, message, description, reference_url, tags)
        self.old_label = old_label
        self.new_label = new_label

    def check(self, target):
        labels = target.instance.get_metadata()["Config"]["Labels"]
        old_present = labels is not None and self.old_label in labels

        passed = (not old_present) or (self.new_label in labels)

        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
