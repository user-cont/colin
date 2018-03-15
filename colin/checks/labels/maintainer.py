from colin.checks.abstract.labels import LabelCheck


class MaintainerCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="maintainer_label_required",
                         message="",
                         description="",
                         reference_url="",
                         tags=["maintainer", "label", "required"],
                         label="maintainer",
                         required=True,
                         value_regex=None)
