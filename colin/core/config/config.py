import json
import os

from six import iteritems

from colin.core.loader import load_check_implementation
from colin.core.target import is_compatible

CONFIG_DIRECTORY = "/usr/share/colin/"


class Config(object):

    def __init__(self, name=None):
        """
        Load config for colin.

        :param name: str (name of the config file (without .json), default is "default"
        """
        self.name = name or "default"
        config_path = os.path.join(CONFIG_DIRECTORY, self.name + ".json")
        try:
            with open(config_path, mode='r') as config_file:
                self.config_dict = json.load(config_file)
        except Exception as ex:
            pass

    def get_checks(self, target_type, group=None, severity=None, tags=None):
        """
        Get all checks for given type/group/severity/tags.

        :param target_type: TargetType enum
        :param group: str (if not group, get checks from all groups/directories)
        :param severity: str (optional x required)
        :param tags: list of str
        :return: list of check instances
        """
        check_files = self._get_check_files(group=group,
                                            severity=severity)
        checks = []
        for check_file in check_files:
            check_class = load_check_implementation(check_file)
            if is_compatible(target_type, check_class, severity, tags):
                checks.append(check_class)
        return checks

    @staticmethod
    def get_check_file(group, name):
        """
        Get the check file from given group with given name.

        :param group: str
        :param name: str
        :return: str (path)
        """
        return os.path.join(get_checks_path(), group, name + ".py")

    @staticmethod
    def get_check_files(group, names):
        """
        Get the check files from given group with given names.

        :param group: str
        :param names: list of str
        :return: list of str (paths)
        """
        check_files = []
        for f in names:
            check_files.append(Config.get_check_file(group=group,
                                                     name=f))
        return check_files

    def _get_check_groups(self, group=None):
        """
        Get check group to validate

        :param group: str (if None, all from the config will be used)
        :return: list of str (group names)
        """
        groups = [g for g in self.config_dict]
        if group:
            if group in groups:
                check_groups = [group]
            else:
                check_groups = []
        else:
            check_groups = groups
        return check_groups

    def _get_check_files(self, group=None, severity=None):
        """
        Get file names with checks filtered by group and severity.

        :param group: str (if None, all groups will be used)
        :param severity: str (if None, all severities will be used)
        :return: list of str (absolute paths)
        """
        check_files = []
        for g in self._get_check_groups(group):

            for sev, files in iteritems(self.config_dict[g]):
                if (not severity) or severity == sev:
                    check_files += Config.get_check_files(group=g,
                                                          names=files)
        return check_files


def get_checks_path():
    """
    Get path to checks.

    :return: str (absolute path of directory with checks)
    """
    rel_path = os.path.join(os.pardir, os.pardir, os.pardir, "checks")
    return os.path.abspath(os.path.join(__file__, rel_path))
