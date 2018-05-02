import logging

from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.images import ImageCheck
from colin.checks.result import CheckResult

logger = logging.getLogger(__name__)


class CmdOrEntrypointCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super(CmdOrEntrypointCheck, self) \
            .__init__(name="cmd_or_entrypoint",
                      message="Cmd or Entrypoint has to be specified",
                      description="An ENTRYPOINT allows you to configure a container that will run as an executable. "
                                  "The main purpose of a CMD is to provide defaults for an executing container.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#CMD.2FENTRYPOINT_2",
                      tags=["cmd", "entrypoint"])

    def check(self, target):
        metadata = target.instance.get_metadata()["Config"]
        cmd_present = "Cmd" in metadata and metadata["Cmd"]
        msg_cmd_present = "Cmd {}specified.".format("" if cmd_present else "not ")
        logger.debug(msg_cmd_present)

        entrypoint_present = "Entrypoint" in metadata and metadata["Entrypoint"]
        msg_entrypoint_present = "Entrypoint {}specified.".format("" if entrypoint_present else "not ")
        logger.debug(msg_entrypoint_present)

        passed = cmd_present or entrypoint_present
        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[msg_cmd_present, msg_entrypoint_present])
