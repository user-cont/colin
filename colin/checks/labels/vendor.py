from colin.checks.abstract.labels import LabelCheck


class VendorLabelCheck(LabelCheck):

    def __init__(self):
        super(VendorLabelCheck, self) \
            .__init__(name="vendor_label",
                      message="Label 'vendor' has to be specified.",
                      description="Name of the vendor.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md",
                      tags=["vendor", "label"],
                      label="vendor",
                      required=True)
