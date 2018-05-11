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

from colin.core.checks.dockerfile import DockerfileAbstractCheck, InstructionCountAbstractCheck
from colin.core.result import CheckResult
from colin.core.target import ImageName


class FromTagNotLatestCheck(DockerfileAbstractCheck):

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
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


class MaintainerDeprecatedCheck(InstructionCountAbstractCheck):

    def __init__(self):
        super(MaintainerDeprecatedCheck, self) \
            .__init__(name="maintainer_deprecated",
                      message="Dockerfile instruction `MAINTAINER` is deprecated.",
                      description="Replace with label 'maintainer'.",
                      reference_url="https://docs.docker.com/engine/reference/builder/#maintainer-deprecated",
                      tags=["maintainer", "dockerfile", "deprecated"],
                      instruction="MAINTAINER",
                      max_count=0)
