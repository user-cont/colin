from colin.checks.abstract.labels import LabelCheck


class UsageCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="usage_label_required",
                      message="Label 'usage' has to be specified.",
                      description="A human readable example of container execution.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["usage", "label", "required"],
                      label="usage",
                      required=True,
                      value_regex=None)
