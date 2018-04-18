from colin.checks.abstract.labels import DeprecatedLabelCheck


class NameLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="name_label_capital_deprecated",
                      message="Label 'Name' is deprecated.",
                      description="Replace with 'name'.",
                      reference_url="?????",
                      tags=["name", "label", "capital", "deprecated"],
                      old_label="Name",
                      new_label="name")
