from colin.checks.abstract.labels import LabelCheck


class DescriptionLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="io.k8s.description_label",
                         message="Label 'io.k8s.description' has to be specified.",
                         description="Description of the container displayed in Kubernetes",
                         reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md",
                         tags=["io.k8s.description", "description", "label", "required"],
                         label="io.k8s.description",
                         required=True,
                         value_regex=None)
