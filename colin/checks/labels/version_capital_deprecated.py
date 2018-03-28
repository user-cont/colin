from colin.checks.abstract.labels import DeprecatedLabelCheck


class VersionLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super().__init__(name="version_label_capital_deprecated",
                         message="Label 'Version' is deprecated.",
                         description="Replace with 'version'.",
                         reference_url="?????",
                         tags=["version", "label", "capital", "deprecated"],
                         old_label="Version",
                         new_label="version")
