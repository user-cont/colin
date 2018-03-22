from colin.checks.abstract.labels import LabelCheck


class UrlLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="url_label",
                         message="Label 'url' has to be specified.",
                         description="A URL where the user can find more information about the image.",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["url", "label", "required"],
                         label="url",
                         required=True,
                         value_regex=None)
        # TODO: Check the format for RHEL
