from colin.checks.abstract.labels import LabelCheck


class AuthoritativeSourceUrlLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="authoritative-source-url_label",
                      message="Label 'authoritative-source-url' has to be specified.",
                      description="The authoritative registry in which the image is published.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["authoritative-source-url", "label", "required"],
                      label="authoritative-source-url",
                      required=True,
                      value_regex=None)
