from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.dockerfile import DockerfileCheck
from colin.checks.abstract.images import ImageCheck


class DockerfileLabelCheck(DockerfileCheck):
    def check(self, target):
        pass


class ImageLabelCheck(ImageCheck):
    def check(self, target):
        pass


class ContainerLabelCheck(ContainerCheck):
    def check(self, target):
        pass


class LabelCheck(DockerfileLabelCheck, ImageLabelCheck, ContainerLabelCheck):

    def __init__(self, name, message, description, reference_url, tags, label, required, value_regex=None):
        super().__init__(name, message, description, reference_url, tags)
        self.label = label
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        pass
