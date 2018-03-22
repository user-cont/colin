from colin.checks.abstract.labels import LabelCheck


class ComRedhatComponentCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="com_redhat_component_label_required",
                         message="Label 'com.redhat.component' has to be specified.",
                         description="The Bugzilla component name where bugs against this container should be reported by users.",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["com.redhat.component", "label", "required"],
                         label="com.redhat.component",
                         required=True,
                         value_regex=None)
        # TODO: Check the format
