from colin.checks.abstract.labels import LabelCheck


class VcsUrlLabelCheck(LabelCheck):

    def __init__(self):
        super(VcsUrlLabelCheck, self) \
            .__init__(name="vcs-url_label",
                      message="Label 'vcs-url' has to be specified.",
                      description="URL of the version control repository.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-url", "vcs", "label"],
                      label="vcs-url",
                      required=True,
                      value_regex=None)
