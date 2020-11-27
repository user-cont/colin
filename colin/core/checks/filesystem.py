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

from .abstract_check import ImageAbstractCheck
from ..result import CheckResult

logger = logging.getLogger(__name__)


class FileCheck(ImageAbstractCheck):
    """ Check presence of files; w/o mounting the whole FS """

    def __init__(
        self, message, description, reference_url, tags, files, all_must_be_present
    ):
        super(FileCheck, self).__init__(message, description, reference_url, tags)
        self.files = files
        self.all_must_be_present = all_must_be_present

    def _handle_image(self, target):
        passed = self.all_must_be_present

        logs = []
        for f in self.files:
            try:
                f_present = target.file_is_present(f)
                logs.append(
                    f"File '{f}' is {'' if f_present else 'not '}present."
                )
            except IOError as ex:
                logger.info("File %s is not present, ex: %s", f, ex)
                f_present = False
                logs.append(f"File {f} is not present.")
            if self.all_must_be_present:
                passed = f_present and passed
            else:
                passed = f_present or passed

        for log in logs:
            logger.debug(log)

        return CheckResult(
            ok=passed,
            description=self.description,
            message=self.message,
            reference_url=self.reference_url,
            check_name=self.name,
            logs=logs,
        )

    def _handle_container(self, target):
        passed = self.all_must_be_present
        cont = target.instance

        logs = []
        for f in self.files:
            cmd = ["/bin/ls", "-1", f]
            try:
                f_present = cont.execute(cmd)
                logs.append(
                    f"File '{f}' is {'' if f_present else 'not '}present."
                )
            except Exception as ex:
                logger.info("File %s is not present, ex: %s", f, ex)
                f_present = False
                logs.append(f"File {f} is not present.")
            if self.all_must_be_present:
                passed = f_present and passed
            else:
                passed = f_present or passed

        return CheckResult(
            ok=passed,
            description=self.description,
            message=self.message,
            reference_url=self.reference_url,
            check_name=self.name,
            logs=logs,
        )

    def check(self, target):
        return self._handle_image(target)


# class FileSystemCheck(ImageAbstractCheck):
#     """ check for presence of files using `docker save` """
#
#     def __init__(self, message, description, reference_url, tags, files, all_must_be_present):
#         super(FileSystemCheck, self) \
#             .__init__(message, description, reference_url, tags)
#         self.files = files
#         self.all_must_be_present = all_must_be_present
#
#     def check(self, target):
#         try:
#             with target.instance.mount() as fs:
#                 passed = self.all_must_be_present
#
#                 logs = []
#                 for f in self.files:
#                     try:
#                         f_present = fs.file_is_present(f)
#                         logs.append("File '{}' is {}present."
#                                     .format(f, "" if f_present else "not "))
#                     except IOError as ex:
#                         f_present = False
#                         logs.append("Error: {}".format(str(ex)))
#
#                     if self.all_must_be_present:
#                         passed = f_present and passed
#                     else:
#                         passed = f_present or passed
#
#                 return CheckResult(ok=passed,
#                                    description=self.description,
#                                    message=self.message,
#                                    reference_url=self.reference_url,
#                                    check_name=self.name,
#                                    logs=logs)
#         except Exception as ex:
#             raise ColinException("There was an error while operating on filesystem of {}: {}"
#                                  .format(target.instance, str(ex)))
