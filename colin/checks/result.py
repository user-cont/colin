import json

from six import itervalues, iteritems

from ..core.constant import REQUIRED, PASSED, FAILED, WARNING, OPTIONAL


class AbstractResult(object):

    def __init__(self, ok, description, message, reference_url, check_name, severity):
        super().__init__()
        self.ok = ok
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name
        self.severity = severity

    @property
    def status(self):
        statuses = {REQUIRED: (PASSED, FAILED),
                    OPTIONAL: (PASSED, WARNING)}
        status_ok, status_nok = statuses[self.severity]

        return status_ok if self.ok else status_nok

    def __str__(self):
        return "{}:{}:{}".format("ok " if self.ok else "nok",
                                 self.status,
                                 self.check_name)


class DockerfileCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, lines=None,
                 correction_diff=None):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.lines = lines
        self.correction_diff = correction_diff


class ContainerCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.logs = logs


class ImageCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.logs = logs


class CheckResults(object):

    def __init__(self, results):
        self.results = results
