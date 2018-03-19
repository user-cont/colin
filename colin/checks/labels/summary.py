from colin.checks.abstract.labels import LabelCheck


class SummaryCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="summary_label_required",
                         message="Label 'summary' has to be specified.",
                         description="A short description of the image.",
                         reference_url="http://url-to-upstream-documentation/summary",
                         tags=["summary", "label", "required"],
                         label="summary",
                         required=True,
                         value_regex=None)
