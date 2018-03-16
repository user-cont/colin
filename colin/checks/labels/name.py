from colin.checks.abstract.labels import LabelCheck


class NameCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="name_label_required",
                         message="Label 'name' has to be specified.",
                         description="Name of the Image or Container.",
                         reference_url="http://url-to-upstream-documentation/name",
                         tags=["name", "label", "required"],
                         label="name",
                         required=True,
                         value_regex=None)
