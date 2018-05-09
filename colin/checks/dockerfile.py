from colin.core.checks.dockerfile import DockerfileCheck, InstructionCountCheck
from colin.core.result import CheckResult
from colin.core.target import ImageName


class FromTagNotLatestCheck(DockerfileCheck):

    def __init__(self):
        super(FromTagNotLatestCheck, self) \
            .__init__(name="from_tag_not_latest",
                      message="In FROM, tag has to be specified and not 'latest'.",
                      description="Using the 'latest' tag may cause unpredictable builds."
                                  "It is recommended that a specific tag is used in the FROM.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#FROM",
                      tags=["from", "dockerfile", "baseimage", "latest"])

    def check(self, target):
        im = ImageName.parse(target.instance.baseimage)
        passed = im.tag and im.tag != "latest"
        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


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
