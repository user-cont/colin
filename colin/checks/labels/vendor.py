from colin.checks.abstract.labels import LabelCheck


class VendorLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="vendor_label",
                      message="Label 'vendor' has to be specified.",
                      description="'Red Hat, Inc.'",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md",
                      tags=["vendor", "label", "required"],
                      label="vendor",
                      required=True,
                      value_regex="^Red Hat, Inc.$")
