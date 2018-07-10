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
import os

from ..constant import JSON, RULESET_DIRECTORY, RULESET_DIRECTORY_NAME
from ..exceptions import ColinRulesetException
from ..loader import CheckLoader
from ..target import is_compatible
from .loader import (RulesetStruct, get_ruleset_struct_from_file,
                     get_ruleset_struct_from_fileobj)

logger = logging.getLogger(__name__)


class Ruleset(object):

    def __init__(self, ruleset_name=None, ruleset_file=None, ruleset=None):
        """
        Load ruleset for colin.

        :param ruleset_name: str (name of the ruleset file (without .json), default is "default"
        :param ruleset_file: fileobj instance holding ruleset configuration
        :param ruleset: dict, content of a ruleset file
        """
        self.check_loader = CheckLoader(get_checks_path())
        if ruleset:
            self.ruleset_struct = RulesetStruct(ruleset)
        elif ruleset_file:
            self.ruleset_struct = get_ruleset_struct_from_fileobj(ruleset_file)
        else:
            logger.debug("Loading ruleset with the name '{}'.".format(ruleset_name))
            ruleset_path = get_ruleset_file(ruleset=ruleset_name)
            self.ruleset_struct = get_ruleset_struct_from_file(ruleset_path)
        if self.ruleset_struct.version not in ["1", 1]:
            raise ColinRulesetException("colin accepts only ruleset version '1'. You provided %r"
                                        % self.ruleset_struct.version)

    def get_checks(self, target_type, tags=None):
        """
        Get all checks for given type/tags.

        :param target_type: TargetType enum
        :param tags: list of str
        :return: list of check instances
        """
        result = []
        for check_struct in self.ruleset_struct.checks:
            logger.debug("Processing check_struct {}.".format(check_struct))

            usable_targets = check_struct.usable_targets
            if target_type and usable_targets and target_type.name.lower() not in usable_targets:
                logger.info("Skipping... Target type does not match.")
                continue

            try:
                check_class = self.check_loader.mapping[check_struct.name]
            except KeyError:
                raise ColinRulesetException(
                    "Can't find code for check {}.".format(check_struct.name))
            try:
                check_instance = check_class()
            except Exception as ex:
                raise ColinRulesetException(
                    "Can't instantiate check {}: {}".format(check_class.__name__, ex))

            if check_struct.tags:
                logger.info("Overriding check's tags %s with the one defined in ruleset: %s",
                            check_instance.tags, check_struct.tags)
                check_instance.tags = check_struct.tags[:]
            if check_struct.additional_tags:
                logger.info("Adding additional tags: %s", check_struct.additional_tags)
                check_instance.tags += check_struct.additional_tags

            if not is_compatible(target_type=target_type, check_instance=check_instance):
                logger.error(
                    "Check '{}' not compatible with the target type: {}".format(
                        check_instance.name, target_type.name))
                raise ColinRulesetException(
                    "Check {} can't be used for target type {}".format(
                        check_instance, target_type))

            if tags:
                if not set(tags) < set(check_instance.tags):
                    logger.debug(
                        "Check '{}' not passed the tag control: {}".format(check_instance.name,
                                                                           tags))
                    continue

            # and finally, attach attributes from ruleset to the check instance
            for k, v in check_struct.other_attributes.items():
                # yes, this overrides things; yes, users may easily and severely broke their setup
                setattr(check_instance, k, v)

            result.append(check_instance)
            logger.debug("Check instance {} added.".format(check_instance.name))

        return result


def get_checks_path():
    """
    Get path to checks.

    :return: str (absolute path of directory with checks)
    """
    rel_path = os.environ.get("CHECK") or os.path.join(os.pardir, os.pardir, os.pardir, "checks")
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

    cwd_rulesets = os.path.join(".", RULESET_DIRECTORY_NAME)
    if os.path.isdir(cwd_rulesets):
        logger.debug("Ruleset directory found in current directory ('{}').".format(cwd_rulesets))
        return cwd_rulesets

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
