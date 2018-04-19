from colin.checks.abstract.labels import LabelCheck


class ReleaseLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="release_label",
                      message="Label 'release' has to be specified.",
                      description="Release Number for this version.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["release", "label", "required"],
                      label="release",
                      required=True,
                      value_regex=None)
