from colin.checks.abstract.dockerfile import LabelCheck


class NameCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="name_label_required",
                         message="",
                         description="",
                         reference_url="",
                         tags=["name", "label", "required"],
                         label="name",
                         required=True,
                         value_regex=None)
