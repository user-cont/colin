from colin.checks.abstract.dockerfile import DockerfileLabelCheck


class DockerfileLabelMaintainerCheck(DockerfileLabelCheck):

    def __init__(self):
        super().__init__(name="maintainer_label_required",
                         message="Label 'maintainer' has to be specified.",
                         description="The name and email of the maintainer (usually the submitter).",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["maintainer", "label", "required"],
                         label="maintainer",
                         required=True,
                         value_regex=None)
