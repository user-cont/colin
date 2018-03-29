from colin.checks.abstract.labels import DeprecatedLabelCheck


class BZComponentDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super().__init__(name="bzcomponent_deprecated",
                         message="Label 'BZComponent' is deprecated.",
                         description="Replace with 'com.redhat.component'.",
                         reference_url="?????",
                         tags=["com.redhat.component", "bzcomponent", "label", "deprecated"],
                         old_label="BZComponent",
                         new_label="com.redhat.component")
