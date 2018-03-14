from colin.core.loader import load_check_implementation
from colin.core.target import is_compatible


class Config(object):

    def __init__(self, name=None):
        self.name = name or "default"
        # load from /usr/share/colin/${name}

    def get_checks(self, group, target_type, severity=None, tags=None):
        check_files = self._get_check_files(group)
        checks = []
        for check_file in check_files:
            check_class = load_check_implementation(check_file)
            if is_compatible(target_type, check_class, severity, tags):
                checks.append(check_class)

    @staticmethod
    def _get_check_files(group=None):
        # get all files from /usr/lib/python3.6/colin/checks/${group}/
        # if not group, go through all directories
        return []
