from colin.checks.abstract.labels import DeprecatedLabelCheck


class UninstallLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super().__init__(name="uninstall_label_capital_deprecated",
                         message="Label 'UNINSTALL' is deprecated.",
                         description="Replace with 'uninstall'.",
                         reference_url="?????",
                         tags=["uninstall", "label", "capital", "deprecated"],
                         old_label="UNINSTALL",
                         new_label="uninstall")
