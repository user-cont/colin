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
from colin.core.checks.filesystem import FileCheck
from colin.core.checks.images import ImageAbstractCheck
from colin.core.result import CheckResult
from colin.core.checks.fmf_check import FMFAbstractCheck


logger = logging.getLogger(__name__)


class CmdOrEntrypointCheck(FMFAbstractCheck, ContainerAbstractCheck, ImageAbstractCheck):
    name = "cmd_or_entrypoint"

    def check(self, target):
        raise RuntimeError("This check is not support now: skopeo doesn't provide this metadata.")
        metadata = target.config_metadata
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


class HelpFileOrReadmeCheck(FMFAbstractCheck, FileCheck):
    name = "help_file_or_readme"


class NoRootCheck(FMFAbstractCheck, ContainerAbstractCheck, ImageAbstractCheck):
    name = "no_root"

    def check(self, target):
        raise RuntimeError("This check is not support now: skopeo doesn't provide this metadata.")
        metadata = target.config_metadata
        root_present = "User" in metadata and metadata["User"] in ["", "0", "root"]

        return CheckResult(ok=not root_present,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
