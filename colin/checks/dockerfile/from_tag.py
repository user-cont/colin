from colin.checks.abstract.dockerfile import DockerfileCheck
from colin.checks.result import CheckResult
from colin.core.target import ImageName


class FromTagCheck(DockerfileCheck):

    def __init__(self):
        super(self.__class__, self) \
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
