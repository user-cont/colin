from colin.checks.abstract.labels import LabelCheck


class ArchitectureLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="architecture_label",
                         message="Label 'architecture' has to be specified.",
                         description="Architecture the software in the image should target "
                                     "(Optional: if omitted, it will be built "
                                     "for all supported Fedora Architectures)",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["architecture", "label", "required"],
                         label="architecture",
                         required=True,
                         value_regex=None)
