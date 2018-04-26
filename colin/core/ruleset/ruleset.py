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

import json
import logging
import os

import six
from six import iteritems

from ..constant import JSON, RULESET_DIRECTORY
from ..exceptions import ColinRulesetException
from ..loader import load_check_implementation
from ..target import is_compatible

logger = logging.getLogger(__name__)


class Ruleset(object):

    def __init__(self, ruleset_name=None, ruleset_file=None, ruleset=None):
        """
        Load ruleset for colin.

        :param ruleset_name: str (name of the ruleset file (without .json), default is "default"
        :param ruleset_file: fileobj instance holding ruleset configuration
        :param ruleset: dict, content of a ruleset file
        """
        if ruleset_file:
            try:
                logger.debug("Loading ruleset from file '{}'.".format(ruleset_file.name))
                self.ruleset_dict = json.load(ruleset_file)
            except Exception as ex:
                msg = "Ruleset file '{}' cannot be loaded.".format(ruleset_file.name)
                logger.error(msg)
                raise ColinRulesetException(msg)
        elif ruleset_name:
            try:
                logger.debug("Loading ruleset with the name '{}'.".format(ruleset_name))
                ruleset_path = get_ruleset_file(ruleset=ruleset_name)
                with open(ruleset_path, mode='r') as ruleset_file_obj:
                    self.ruleset_dict = json.load(ruleset_file_obj)
            except ColinRulesetException as ex:
                raise ex
            except Exception as ex:
                file_name = ruleset_path if ruleset_path else ruleset_name
                msg = "Ruleset '{}' cannot be loaded.".format(file_name)

                logger.error(msg)
                raise ColinRulesetException(msg)
        elif ruleset:
            self.ruleset_dict = ruleset
        else:
            logger.error("none of the arguments ruleset_{name,file}, ruleset was passed")
            raise ColinRulesetException("No ruleset was selected.")
        # TODO: validate ruleset

    def get_checks(self, target_type, group=None, severity=None, tags=None):
        """
        Get all checks for given type/group/severity/tags.

        :param target_type: TargetType enum
        :param group: str (if not group, get checks from all groups/directories)
        :param severity: str (optional x required)
        :param tags: list of str
        :return: list of check instances
        """
        groups = {}
        for g in self._get_check_groups(group):
            logger.debug("Getting checks for group '{}'.".format(g))
            check_files = []
            for sev, rules in iteritems(self.ruleset_dict[g]):

                if severity and severity != sev:
                    continue

                check_files += Ruleset.get_checks_from_rules(rules=rules,
                                                             group=g,
                                                             target_type=target_type,
                                                             severity=sev,
                                                             tags=tags)
            groups[g] = check_files
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
    def get_checks_from_rules(rules, group, target_type, severity, tags):
        """
        get check from the list of check items in the resultset file.

        :param rules: [str or dict]
        :param group: str
        :param target_type: TargetType enum
        :param severity: str
        :param tags: [str]
        :return: list of filtered check instances
        """
        rule_items = []
        for rule in rules:

            if isinstance(rule, six.string_types):
                rule_items.append(rule)
            elif isinstance(rule, dict):
                if target_type and target_type.name not in rule["type"]:
                    continue

                rule_items += rule["checks"]

        check_instances = []
        for r in rule_items:
            logger.debug("Loading check instance for {}".format(r))
            check_instances += load_check_implementation(path=Ruleset.get_check_file(group, r))
        result = []
        for check_instance in check_instances:
            check_instance.severity = severity
            if not is_compatible(target_type=target_type, check_instance=check_instance):
                logger.debug(
                    "Check '{}' not compatible with the target type: {}".format(check_instance.name, target_type.name))
                continue

            if tags:
                if not set(tags) < set(check_instance.tags):
                    logger.debug("Check '{}' not passed the tag control: {}".format(check_instance.name,
                                                                                  tags))
                    continue
            result.append(check_instance)
            logger.debug("Check instance {} added.".format(check_instance.name))

        return result

    def _get_check_groups(self, group=None):
        """
        Get check group to validate

        :param group: str (if None, all from the ruleset will be used)
        :return: list of str (group names)
        """
        groups = [g for g in self.ruleset_dict]
        if group:
            if group in groups:
                check_groups = [group]
            else:
                check_groups = []
        else:
            check_groups = groups
        logger.debug("Found groups: {}.".format(check_groups))
        return check_groups


def get_checks_path():
    """
    Get path to checks.

    :return: str (absolute path of directory with checks)
    """
    rel_path = os.path.join(os.pardir, os.pardir, os.pardir, "checks")
    return os.path.abspath(os.path.join(__file__, rel_path))


def get_ruleset_file(ruleset=None):
    """
    Get the ruleset file from name

    :param ruleset: str
    :return: str
    """
    ruleset = ruleset or "default"

    ruleset_directory = get_ruleset_directory()
    ruleset_file = os.path.join(ruleset_directory, ruleset + JSON)

    if os.path.isfile(ruleset_file):
        logger.debug("Ruleset file '{}' found.".format(ruleset_file))
        return ruleset_file

    logger.warning("Ruleset with the name '{}' cannot be found at '{}'."
                   .format(ruleset, ruleset_file))
    raise ColinRulesetException("Ruleset with the name '{}' cannot be found.".format(ruleset))


def get_ruleset_directory():
    """
    Get the directory with ruleset files
    First directory to check:  $HOME/.local/share/colin/rulesets
    Second directory to check: /usr/local/share/colin/rulesets
    :return: str
    """

    local_share = os.path.join(os.path.expanduser("~"),
                               ".local",
                               RULESET_DIRECTORY)
    if os.path.isdir(local_share):
        logger.debug("Local ruleset directory found ('{}').".format(local_share))
        return local_share

    usr_local_share = os.path.join("/usr/local", RULESET_DIRECTORY)
    if os.path.isdir(usr_local_share):
        logger.debug("Global ruleset directory found ('{}').".format(usr_local_share))
        return usr_local_share

    msg = "Ruleset directory cannot be found."
    logger.warning(msg)
    raise ColinRulesetException(msg)


def get_rulesets():
    """"
    Get available rulesets.
    """
    rulesets_dir = get_ruleset_directory()
    ruleset_files = [f[:-len(JSON)] for f in os.listdir(rulesets_dir) if
                     os.path.isfile(os.path.join(rulesets_dir, f)) and f.lower().endswith(JSON)]
    return ruleset_files
