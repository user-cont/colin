from colin.checks.abstract.labels import LabelCheck


class IoK8sDescriptionLabelCheck(LabelCheck):

    def __init__(self):
        super(IoK8sDescriptionLabelCheck, self) \
            .__init__(name="io.k8s.description_label",
                      message="Label 'io.k8s.description' has to be specified.",
                      description="Description of the container displayed in Kubernetes",
                      reference_url=["https://github.com/projectatomic/ContainerApplicationGenericLabels",
                                     "https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md#other-labels"],
                      tags=["io.k8s.description", "description", "label"],
                      label="io.k8s.description",
                      required=True,
                      value_regex=None)
