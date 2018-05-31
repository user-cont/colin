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

from conu import DockerRunBuilder
from conu.exceptions import ConuException

from colin.core.target import TargetType
from ..exceptions import ColinException
from ..result import CheckResult
from .containers import ContainerAbstractCheck
from .images import ImageAbstractCheck


logger = logging.getLogger(__name__)


class FileCheck(ContainerAbstractCheck, ImageAbstractCheck):
    """ Check presence of files; w/o mounting the whole FS """
    init_list = ["files", "all_must_be_present"]

    def check(self, target):
        passed = self.all_must_be_present
        cleanup = False

        if target.target_type is TargetType.IMAGE:
            drb = DockerRunBuilder(command=["/bin/sleep", "infinity"],
                                   additional_opts=["--entrypoint="])
            cont = target.instance.run_via_binary(run_command_instance=drb)
            cleanup = True
        elif target.target_type is TargetType.CONTAINER:
            cont = target.instance
        else:
            return CheckResult(ok=False,
                               description=self.description,
                               message=self.message,
                               reference_url=self.reference_url,
                               check_name=self.name,
                               logs=["Unsupported target, this check can "
                                     "process only containers and images"])
        logs = []
        try:
            for f in self.files:
                cmd = ["/bin/ls", "-1", f]
                try:
                    f_present = cont.execute(cmd)
                    logs.append("File '{}' is {}present."
                                .format(f, "" if f_present else "not "))
                except ConuException as ex:
                    logger.info("File %s is not present, ex: %s", f, ex)
                    f_present = False
                    logs.append("File {} is not present.".format(f))
                if self.all_must_be_present:
                    passed = f_present and passed
                else:
                    passed = f_present or passed

            return CheckResult(ok=passed,
                               description=self.description,
                               message=self.message,
                               reference_url=self.reference_url,
                               check_name=self.name,
                               logs=logs)
        finally:
            if cleanup:
                cont.stop()
                cont.delete()


class FileSystemCheck(ContainerAbstractCheck, ImageAbstractCheck):
    init_list = ["files", "all_must_be_present"]

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
                                   description=self.description,
                                   message=self.message,
                                   reference_url=self.reference_url,
                                   check_name=self.name,
                                   logs=logs)
        except Exception as ex:
            raise ColinException("There was an error while operating on filesystem of {}: {}"
                                 .format(target.instance, str(ex)))
