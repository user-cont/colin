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
from colin.core.target import inspect_object, TargetType
from .check_utils import check_label
from .containers import ContainerAbstractCheck
from .dockerfile import DockerfileAbstractCheck
from .images import ImageAbstractCheck
from ..result import CheckResult, FailedCheckResult


class LabelAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck, DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, labels, required,
                 value_regex=None):
        super(LabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.labels = labels
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        passed = check_label(labels=self.labels,
                             required=self.required,
                             value_regex=self.value_regex,
                             target_labels=target.labels)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


class DeprecatedLabelAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck,
                                   DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, old_label, new_label):
        super(DeprecatedLabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.old_label = old_label
        self.new_label = new_label

    def check(self, target):
        labels = target.labels
        old_present = labels is not None and self.old_label in labels

        passed = (not old_present) or (self.new_label in labels)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


class OverriddenLabelAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck,
                                   DockerfileAbstractCheck):
    def __init__(self, message, description, reference_url, tags, label, layers_for_base=1):
        super(OverriddenLabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.label = label
        self.layers_for_base = layers_for_base

    def check(self, target):

        if target.target_type == TargetType.IMAGE:
            _layer_count = len(inspect_object(target.instance, refresh=False)["RootFS"]["Layers"])
            if _layer_count <= self.layers_for_base:
                return CheckResult(ok=True,
                                   description=self.description,
                                   message=self.message,
                                   reference_url=self.reference_url,
                                   check_name=self.name,
                                   logs=["Target is a base image."])

        present = check_label(labels=[self.label],
                              required=True,
                              target_labels=target.labels,
                              value_regex=None)

        if not present:
            return CheckResult(ok=True,
                               description=self.description,
                               message=self.message,
                               reference_url=self.reference_url,
                               check_name=self.name,
                               logs=["Label '{}' not present.".format(self.label)])

        if not target.base_image:
            parent_labels = try_get_parent_labels_from_image(target)

            if parent_labels is None:
                return FailedCheckResult(check=self,
                                         logs=["Cannot find parent image or parent Dockerfile."])
        else:
            parent_labels = inspect_object(target.base_image, refresh=False)["Config"]["Labels"]

        passed = self.label not in parent_labels or target.labels[self.label] != parent_labels[
            self.label]

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


def try_get_parent_labels_from_image(image):
    # TODO: Get labels from the Dockerfile in /root/buildinfo directory.
    return []
