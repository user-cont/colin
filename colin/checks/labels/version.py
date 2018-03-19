from colin.checks.abstract.labels import LabelCheck


class VersionCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="version_label_required",
                         message="Label 'version' has to be specified.",
                         description="Version of the image.",
                         reference_url="http://url-to-upstream-documentation/version",
                         tags=["version", "label", "required"],
                         label="version",
                         required=True,
                         value_regex=None)
