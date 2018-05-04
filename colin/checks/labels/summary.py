from colin.checks.abstract.labels import LabelCheck


class SummaryCheck(LabelCheck):

    def __init__(self):
        super(SummaryCheck, self) \
            .__init__(name="summary_label_required",
                      message="Label 'summary' has to be specified.",
                      description="A short description of the image.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["summary", "label"],
                      label="summary",
                      required=True,
                      value_regex=None)
