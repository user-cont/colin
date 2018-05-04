from colin.checks.abstract.labels import LabelCheck


class IoOpenshiftExposeServicesLabelCheck(LabelCheck):

    def __init__(self):
        super(IoOpenshiftExposeServicesLabelCheck, self) \
            .__init__(name="io.openshift.expose-services_label",
                      message="Label 'io.openshift.expose-services' has to be specified.",
                      description="port:service pairs separated with comma, e.g. \"8080:http,8443:https\"",
                      reference_url=["https://github.com/projectatomic/ContainerApplicationGenericLabels",
                                     "https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md#other-labels"],
                      tags=["io.openshift.expose-services", "label"],
                      label="io.openshift.expose-services",
                      required=True,
                      value_regex=None)
