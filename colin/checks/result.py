class AbstractResult(object):

    def __init__(self, ok, status, description, message, reference_url, check_name):
        super().__init__()
        self.ok = ok
        self.status = status
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name

    def __str__(self):
        return "{}:{}:{}".format("ok " if self.ok else "nok",
                                 self.status,
                                 self.check_name)


class DockerfileCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, reference_url, check_name, lines=None, correction_diff=None):
        super().__init__(ok, status, description, message, reference_url, check_name)
        self.lines = lines
        self.correction_diff = correction_diff


class ContainerCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, reference_url, check_name, logs):
        super().__init__(ok, status, description, message, reference_url, check_name)
        self.logs = logs


class ImageCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, reference_url, check_name, logs):
        super().__init__(ok, status, description, message, reference_url, check_name)
        self.logs = logs


class CheckResults(object):

    def __init__(self, results):
        self.results = results
