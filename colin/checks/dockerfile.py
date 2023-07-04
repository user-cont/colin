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

from colin.core.checks.abstract_check import DockerfileAbstractCheck
from colin.core.checks.dockerfile import InstructionCountAbstractCheck
from colin.core.checks.fmf_check import FMFAbstractCheck
from colin.core.exceptions import ColinException
from colin.core.result import CheckResult
from colin.utils.cont import ImageName


class FromTagNotLatestCheck(FMFAbstractCheck, DockerfileAbstractCheck):
    name = "from_tag_not_latest"

    def check(self, target):
        if not target.instance.parent_images:
            raise ColinException("Cannot find FROM instruction.")

        im = ImageName.parse(target.instance.baseimage)
        passed = im.tag and im.tag != "latest"
        return CheckResult(
            ok=passed,
            description=self.description,
            message=self.message,
            reference_url=self.reference_url,
            check_name=self.name,
            logs=[],
        )


class MaintainerDeprecatedCheck(FMFAbstractCheck, InstructionCountAbstractCheck):
    name = "maintainer_deprecated"
