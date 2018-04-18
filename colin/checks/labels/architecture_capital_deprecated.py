from colin.checks.abstract.labels import DeprecatedLabelCheck


class ArchitectureLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(self.__class__, self). \
            __init__(name="architecture_label_capital_deprecated",
                     message="Label 'Architecture' is deprecated.",
                     description="Replace with 'architecture'.",
                     reference_url="?????",
                     tags=["architecture", "label", "capital", "deprecated"],
                     old_label="Architecture",
                     new_label="architecture")
