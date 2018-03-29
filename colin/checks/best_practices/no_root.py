from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.images import ImageCheck
from colin.checks.result import CheckResult


class NoRootCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super().__init__(name="no_root",
                         message="Service should not run as root by default.",
                         description="",
                         reference_url="?????",
                         tags=["root", "user"])

    def check(self, target):
        metadata = target.instance.get_metadata()["Config"]
        root_present = "User" in metadata and metadata["User"] and metadata["User"] != "root"

        return CheckResult(ok=root_present,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
