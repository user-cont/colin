# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging

from colin.core.checks.containers import ContainerAbstractCheck
from colin.core.checks.filesystem import FileSystemCheck
from colin.core.checks.images import ImageAbstractCheck
from colin.core.result import CheckResult
from colin.core.target import inspect_object


logger = logging.getLogger(__name__)


class CmdOrEntrypointCheck(ContainerAbstractCheck, ImageAbstractCheck):
    name = "cmd_or_entrypoint"

    def __init__(self):
        super(CmdOrEntrypointCheck, self) \
            .__init__(message="Cmd or Entrypoint has to be specified",
                      description="An ENTRYPOINT allows you to configure a container"
                                  " that will run as an executable. The main purpose"
                                  " of a CMD is to provide defaults for an executing container.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines"
                                    "#CMD.2FENTRYPOINT_2",
                      tags=["cmd", "entrypoint"])

    def check(self, target):
        metadata = inspect_object(target.instance)["Config"]
        cmd_present = "Cmd" in metadata and metadata["Cmd"]
        msg_cmd_present = "Cmd {}specified.".format("" if cmd_present else "not ")
        logger.debug(msg_cmd_present)

        entrypoint_present = "Entrypoint" in metadata and metadata["Entrypoint"]
        msg_entrypoint_present = "Entrypoint {}specified.".format(
            "" if entrypoint_present else "not ")
        logger.debug(msg_entrypoint_present)

        passed = cmd_present or entrypoint_present
        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[msg_cmd_present, msg_entrypoint_present])


class HelpFileOrReadmeCheck(FileSystemCheck):
    name = "help_file_or_readme"

    def __init__(self):
        super(HelpFileOrReadmeCheck, self) \
            .__init__(message="The 'helpfile' has to be provided.",
                      description="Just like traditional packages, containers need "
                                  "some 'man page' information about how they are to be used,"
                                  " configured, and integrated into a larger stack.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#Help_File",
                      files=['/help.1', '/README.md'],
                      tags=['filesystem', 'helpfile', 'man'],
                      all_must_be_present=False)


class NoRootCheck(ContainerAbstractCheck, ImageAbstractCheck):
    name = "no_root"

    def __init__(self):
        super(NoRootCheck, self) \
            .__init__(message="Service should not run as root by default.",
                      description="It can be insecure to run service as root.",
                      reference_url="?????",
                      tags=["root", "user"])

    def check(self, target):
        metadata = inspect_object(target.instance)["Config"]
        root_present = "User" in metadata and metadata["User"] in ["", "0", "root"]

        return CheckResult(ok=not root_present,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
