from colin.checks.abstract.labels import LabelCheck


class UsageCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="usage_label_required",
                         message="Label 'usage' has to be specified.",
                         description="A human readable example of container execution .",
                         reference_url="http://url-to-upstream-documentation/usage",
                         tags=["usage", "label", "required"],
                         label="usage",
                         required=True,
                         value_regex=None)
