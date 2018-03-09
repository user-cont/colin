from colin.checks.abstract.abstract_check import AbstractCheck


class DockerfileCheck(AbstractCheck):
    pass


class InstructionCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, regex, required):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.regex = regex
        self.required = required

    def check(self):
        pass


class InstructionCountCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, instruction, min_count=None, max_count=None):
        super().__init__(name, message, description, reference_url, tags)
        self.instruction = instruction
        self.min_count = min_count
        self.max_count = max_count

    def check(self):
        pass


class LabelCheck(AbstractCheck):

    def __init__(self, name, message, description, reference_url, tags, label, required, value_regex=None):
        super().__init__(name, message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self):
        pass
