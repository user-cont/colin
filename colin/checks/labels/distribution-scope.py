from colin.checks.abstract.labels import LabelCheck


class DescriptionScopeLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="distribution-scope_label",
                         message="Label 'distribution-scope' has to be specified.",
                         description="Scope of intended distribution of the image. (private/authoritative-source-only/restricted/public)",
                         reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                         tags=["distribution-scope", "label", "required"],
                         label="distribution-scope",
                         required=True,
                         value_regex=None)
