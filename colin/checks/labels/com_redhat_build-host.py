from colin.checks.abstract.labels import LabelCheck


class BuildHostLabelCheck(LabelCheck):

    def __init__(self):
        super().__init__(name="com.redhat.build-host_label",
                         message="Label 'com.redhat.build-host' has to be specified.",
                         description="The build host used to create an image for internal use and auditability, similar to the use in RPM.",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                         tags=["com.redhat.build-host", "build-host", "label", "required"],
                         label="com.redhat.build-host",
                         required=True,
                         value_regex=None)
