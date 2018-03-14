class AbstractResult(object):

    def __init__(self, ok, status, description, message):
        super().__init__()
        self.passed = ok
        self.status = status
        self.description = description
        self.message = message


class DockerfileCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, lines=None, correction_diff=None):
        super().__init__(ok, status, description, message)
        self.lines = lines
        self.correction_diff = correction_diff


class ContainerCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, logs):
        super().__init__(ok, status, description, message)
        self.logs = logs


class ImageCheckResult(AbstractResult):

    def __init__(self, ok, status, description, message, logs):
        super().__init__(ok, status, description, message)
        self.logs = logs


class CheckResults(object):

    def __init__(self, results):
        self.results = results
