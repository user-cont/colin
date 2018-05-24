import re


def check_label(labels, required, value_regex, target_labels):
    """
    Check if the label is required and match the regex

    :param labels: [str]
    :param required: bool (if the presence means pass or not)
    :param value_regex: str
    :param target_labels: [str]
    :return: bool (required==True: True if the label is present and match the regex if specified)
                    (required==False: True if the label is not present)
    """
    present = target_labels is not None and not set(labels).isdisjoint(set(target_labels))

    if present:
        if required and not value_regex:
            return True
        elif value_regex:
            pattern = re.compile(value_regex)
            present_labels = set(labels) & set(target_labels)
            for l in present_labels:
                if not bool(pattern.match(target_labels[l])):
                    return False
            return True
        else:
            return False

    else:
        return not required
