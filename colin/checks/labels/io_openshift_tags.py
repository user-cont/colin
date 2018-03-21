from colin.checks.abstract.labels import LabelCheck


class IoOpenShiftTagsCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="io_openshift_tags_label_required",
                         message="Label 'io.openshift.tags' has to be specified.",
                         description="The primary purpose of this label is to include all relevant search terms for this image.",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["io.openshift.tags", "label", "required"],
                         label="io.openshift.tags",
                         required=True,
                         value_regex=None)
