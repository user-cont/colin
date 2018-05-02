from colin.checks.abstract.labels import LabelCheck


class IoK8sDisplayNameCheck(LabelCheck):

    def __init__(self):
        super(IoK8sDisplayNameCheck, self) \
            .__init__(name="io_k8s_display-name_label_required",
                      message="Label 'io.k8s.display-name' has to be specified.",
                      description="This label is used to display a human readable name of an image inside the Image / Repo Overview page.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["io.k8s.display-name", "label"],
                      label="io.k8s.display-name",
                      required=True,
                      value_regex=None)
