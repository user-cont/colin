from .containers import ContainerCheck
from .images import ImageCheck
from ..result import CheckResult
from ...core.exceptions import ColinException


class FileSystemCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, files, all_must_be_present):
        super().__init__(name, message, description, reference_url, tags)
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
