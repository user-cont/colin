from colin.checks.abstract.labels import LabelCheck


class BuildDateLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="build-date_label",
                         message="Label 'build-date' has to be specified.",
                         description="Date/Time image was built as RFC 3339 date-time.",
                         reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                         tags=["build-date", "label", "required"],
                         label="build-date",
                         required=True,
                         value_regex=None)
        # TODO: Check the RFC 3339 date-time format
