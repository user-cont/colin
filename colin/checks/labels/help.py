from colin.checks.abstract.labels import LabelCheck


class HelpLabelCheck(LabelCheck):

    def __init__(self):
        super(HelpLabelCheck, self) \
            .__init__(name="help_label",
                      message="Label 'help' has to be specified.",
                      description="A runnable command which results in display of Help information.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["help", "label"],
                      label="help",
                      required=True,
                      value_regex=None)
