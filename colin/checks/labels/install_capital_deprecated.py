from colin.checks.abstract.labels import DeprecatedLabelCheck


class InstallLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super().__init__(name="install_label_capital_deprecated",
                         message="Label 'INSTALL' is deprecated.",
                         description="Replace with 'install'.",
                         reference_url="?????",
                         tags=["install", "label", "capital", "deprecated"],
                         old_label="INSTALL",
                         new_label="install")
