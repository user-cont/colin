from colin.checks.abstract.abstract_check import AbstractCheck


class DockerfileCheck(AbstractCheck):
    pass


class InstructionCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, regex, required):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.regex = regex
        self.required = required

    def check(self, target):
        pass


class InstructionCountCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, min_count=None, max_count=None):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.min_count = min_count
        self.max_count = max_count

    def check(self, target):
        pass
