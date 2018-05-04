from colin.checks.abstract.dockerfile import InstructionCountCheck


class MaintainerDeprecatedCheck(InstructionCountCheck):

    def __init__(self):
        super(MaintainerDeprecatedCheck, self) \
            .__init__(name="maintainer_deprecated",
                      message="Dockerfile instruction `MAINTAINER` is deprecated.",
                      description="Replace with label 'maintainer'.",
                      reference_url="https://docs.docker.com/engine/reference/builder/#maintainer-deprecated",
                      tags=["maintainer", "dockerfile", "deprecated"],
                      instruction="MAINTAINER",
                      max_count=0)
