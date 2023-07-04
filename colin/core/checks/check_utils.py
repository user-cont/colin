import re

from .abstract_check import DockerfileAbstractCheck, ImageAbstractCheck
from ..exceptions import ColinException


def check_label(labels, required, value_regex, target_labels):
    """
    Check if the label is required and match the regex

    :param labels: [str]
    :param required: bool (if the presence means pass or not)
    :param value_regex: str (using search method)
    :param target_labels: [str]
    :return: bool (required==True: True if the label is present and match the regex if specified)
                    (required==False: True if the label is not present)
    """
    present = target_labels is not None and not set(labels).isdisjoint(
        set(target_labels)
    )

    if not present:
        return not required
    if required and not value_regex:
        return True
    elif value_regex:
        pattern = re.compile(value_regex)
        present_labels = set(labels) & set(target_labels)
        return all(
            bool(pattern.search(target_labels[label])) for label in present_labels
        )

    else:
        return False


class NotLoadedCheck(DockerfileAbstractCheck, ImageAbstractCheck):
    def __init__(self, check_name, reason):
        self.name = check_name
        super().__init__(
            message=f"Check code '{check_name}' {reason}.",
            description="Did you set the right name in the ruleset file?",
            reference_url="",
            tags=[],
        )

    def check(self, target):
        raise ColinException(self.message)
