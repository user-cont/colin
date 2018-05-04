from colin.checks.abstract.labels import LabelCheck


class MaintainerLabelCheck(LabelCheck):

    def __init__(self):
        super(MaintainerLabelCheck, self) \
            .__init__(name="maintainer_label_required",
                      message="Label 'maintainer' has to be specified.",
                      description="The name and email of the maintainer (usually the submitter).",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["maintainer", "label"],
                      label="maintainer",
                      required=True,
                      value_regex=None)
