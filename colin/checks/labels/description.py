from colin.checks.abstract.labels import LabelCheck


class DescriptionLabelCheck(LabelCheck):

    def __init__(self):
        super(DescriptionLabelCheck, self) \
            .__init__(name="description_label",
                      message="Label 'description' has to be specified.",
                      description="Detailed description of the image.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["description", "label"],
                      label="description",
                      required=True,
                      value_regex=None)
