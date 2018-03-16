import re

from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.images import ImageCheck
from colin.checks.result import ImageCheckResult
from colin.core.constant import PASSED, FAILED


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

        return ImageCheckResult(ok=passed,
                                status=PASSED if passed else FAILED,
                                description=self.description,
                                message=self.message,
                                reference_url=self.reference_url,
                                logs=[])
