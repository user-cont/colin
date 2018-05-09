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

from ..exceptions import ColinException
from ..result import CheckResult
from .containers import ContainerCheck
from .images import ImageCheck


class FileSystemCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, files, all_must_be_present):
        super(FileSystemCheck, self) \
            .__init__(name, message, description, reference_url, tags)
        self.files = files
        self.all_must_be_present = all_must_be_present

    def check(self, target):
        try:
            with target.instance.mount() as fs:
                passed = self.all_must_be_present

                logs = []
                for f in self.files:
                    try:
                        f_present = fs.file_is_present(f)
                        logs.append("File '{}' is {}present."
                                    .format(f, "" if f_present else "not "))
                    except IOError as ex:
                        f_present = False
                        logs.append("Error: {}".format(str(ex)))

                    if self.all_must_be_present:
                        passed = f_present and passed
                    else:
                        passed = f_present or passed

                return CheckResult(ok=passed,
                                   severity=self.severity,
                                   description=self.description,
                                   message=self.message,
                                   reference_url=self.reference_url,
                                   check_name=self.name,
                                   logs=logs)
        except Exception as ex:
            raise ColinException("Problem with mounting filesystem with atomic. ({})"
                                 .format(str(ex)))
