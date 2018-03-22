from .containers import ContainerCheck
from .images import ImageCheck
from ..result import CheckResult


class FileSystemCheck(ContainerCheck, ImageCheck):

    def __init__(self, name, message, description, reference_url, tags, files, all_must_be_present):
        super().__init__(name, message, description, reference_url, tags)
        self.files = files
        self.all_must_be_present = all_must_be_present

    def check(self, target):
        with target.instance.mount() as fs:
            passed = True
            logs = []
            for f in self.files:
                f_present = fs.file_is_present(f)
                if self.all_must_be_present:
                    passed = f_present and passed
                else:
                    passed = f_present or passed
                logs.append("File '{}' {}present."
                            .format(f, "not " if f_present else ""))
            return CheckResult(ok=passed,
                               severity=self.severity,
                               description=self.description,
                               message=self.message,
                               reference_url=self.reference_url,
                               check_name=self.name,
                               logs=logs)
