import json
import os

from six import iteritems

from ..exceptions import ColinConfigException
from ..constant import CONFIG_DIRECTORY, JSON
from ..loader import load_check_implementation
from ..target import is_compatible


class Config(object):

    def __init__(self, config=None):
        """
        Load config for colin.

        :param config: str (name of the config file (without .json), default is "default"
        """
        self.name = config or "default"
        config_path = get_config_file(config=config)
        try:
            with open(config_path, mode='r') as config_file:
                self.config_dict = json.load(config_file)
        except Exception as ex:
            raise ColinConfigException("Config file '{}' cannot be loaded.".format(config_path))

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
        groups = {}
        for (group, check_files) in iteritems(check_files):
            checks = []
            for severity, check_file in check_files:

                check_classes = load_check_implementation(path=check_file, severity=severity)
                for check_class in check_classes:
                    if is_compatible(target_type, check_class, severity, tags):
                        checks.append(check_class)

            groups[group] = checks
        return groups

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
    def get_check_files(group, names, severity):
        """
        Get the check files from given group with given names.

        :param severity: str
        :param group: str
        :param names: list of str
        :return: list of str (paths)
        """
        check_files = []
        for f in names:
            check_file = Config.get_check_file(group=group,
                                               name=f)
            check_files.append((severity, check_file))
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
        groups = {}
        for g in self._get_check_groups(group):
            check_files = []
            for sev, files in iteritems(self.config_dict[g]):
                if (not severity) or severity == sev:
                    check_files += Config.get_check_files(group=g,
                                                          names=files,
                                                          severity=sev)
            groups[g] = check_files
        return groups


def get_checks_path():
    """
    Get path to checks.

    :return: str (absolute path of directory with checks)
    """
    rel_path = os.path.join(os.pardir, os.pardir, os.pardir, "checks")
    return os.path.abspath(os.path.join(__file__, rel_path))


def get_config_file(config):
    """
    Get the config file from name or path

    :param config: str (name or path)
    :return: str
    """
    if os.path.exists(config) and os.path.isfile(config):
        return config

    config_directory = get_config_directory()
    config_file = os.path.join(config_directory, config + JSON)

    if os.path.exists(config) and os.path.isfile(config):
        return config_file
    raise ColinConfigException("Config '{}' cannot be found.".format(config))


def get_config_directory():
    """
    Get the directory with config files
    First directory to check:  $HOME/.local/share/colin/config
    Second directory to check: /usr/local/share/colin/config
    :return: str
    """

    local_share = os.path.join(os.path.expanduser("~"),
                               ".local",
                               CONFIG_DIRECTORY)
    if os.path.isdir(local_share) and os.path.exists(local_share):
        return local_share

    usr_local_share = os.path.join("/usr/local", CONFIG_DIRECTORY)
    if os.path.isdir(usr_local_share) and os.path.exists(usr_local_share):
        return usr_local_share

    raise ColinConfigException("Config directory cannot be found.")
