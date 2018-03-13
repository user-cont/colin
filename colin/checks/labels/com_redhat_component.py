from colin.checks.abstract.dockerfile import LabelCheck


class ComRedhatComponentCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="com_redhat_component_label_required",
                         message="",
                         description="",
                         reference_url="",
                         tags=["com.redhat.component", "label", "required"],
                         label="com.redhat.component",
                         required=True,
                         value_regex=None)
