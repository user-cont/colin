import re


def check_label(label, required, value_regex, labels):
    """
    Check if the label is required and match the regex

    :param label: str
    :param required: bool (if the presence means pass or not)
    :param value_regex: str
    :param labels: [str]
    :return: bool (required==True: True if the label is present and match the regex if specified)
                    (required==False: True if the label is not present)
    """
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
