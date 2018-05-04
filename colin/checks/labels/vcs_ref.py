from colin.checks.abstract.labels import LabelCheck


class VcsRefLabelCheck(LabelCheck):

    def __init__(self):
        super(VcsRefLabelCheck, self) \
            .__init__(name="vcs-ref_label",
                      message="Label 'vcs-ref' has to be specified.",
                      description="A 'reference' within the version control repository; e.g. a git commit, or a subversion branch.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-ref", "vcs", "label"],
                      label="vcs-ref",
                      required=True,
                      value_regex=None)
