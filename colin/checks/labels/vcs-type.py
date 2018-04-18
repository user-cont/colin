from colin.checks.abstract.labels import LabelCheck


class VcsTypeLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="vcs-type_label",
                      message="Label 'vcs-type' has to be specified.",
                      description="The type of version control used by the container source."
                                  "Generally one of git, hg, svn, bzr, cvs",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-type", "vcs", "label", "required"],
                      label="vcs-type",
                      required=True,
                      value_regex=None)
