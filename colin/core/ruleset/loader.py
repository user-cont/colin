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

"""
This module is responsible for loading rulesets: reading from disk, parsing/validating
"""
import json
import logging

from ..exceptions import ColinRulesetException

logger = logging.getLogger(__name__)


def get_ruleset_struct_from_fileobj(fileobj):
        try:
            logger.debug("Loading ruleset from file '{}'.".format(fileobj.name))
            return RulesetStruct(json.load(fileobj))
        except Exception as ex:
            msg = "Ruleset file '{}' cannot be loaded: {}".format(fileobj.name, ex)
            logger.error(msg)
            raise ColinRulesetException(msg)


def get_ruleset_struct_from_file(file_path):
    try:
        with open(file_path, "r") as fd:
            return get_ruleset_struct_from_fileobj(fd)
    except ColinRulesetException as ex:
        raise ex
    except Exception as ex:
        msg = "Ruleset '{}' cannot be loaded: {}".format(file_path, ex)

        logger.error(msg)
        raise ColinRulesetException(msg)


def nicer_get(di, required, *path):
    """
    this is a nicer way of doing dict.get()
    
    :param di: dict
    :param required: bool, raises an exc if value is not found, otherwise returns None
    :param path: list of str to navigate in the dict
    :return: your value
    """
    
    r = di
    for p in path:
        try:
            r = r[p]
        except KeyError:
            if required:
                logger.error("can't locate %s in ruleset dict, keys present: %s",
                             p, list(r.keys()))
                logger.debug("full dict = %s", r)
                raise ColinRulesetException("Validation error: can't locate %s in ruleset." % p)
            return
    return r


class CheckStruct(object):
    """
      {
        "name": "label_name",
        "tags": ["foo", "bar"],
        "additional_tags": ["baz"],
        "usable_targets": ["image", "dockerfile"],
      }
    """
    def __init__(self, check_dict):
        self.c = check_dict
        # TODO: validate the dict
        # TODO: get check class and merry them here

    def _get(self, required, *path):
        return nicer_get(self.c, required, *path)

    def __str__(self):
        return "%s" % self.name
    
    @property
    def name(self):
        return self._get(True, "name")

    @property
    def tags(self):
        return self._get(False, "tags")

    @property
    def additional_tags(self):
        return self._get(False, "additional_tags")

    @property
    def usable_targets(self):
        return self._get(False, "usable_targets")

    @property
    def other_attributes(self):
        """ return dict with all other data except for the described above"""
        return {k: v for k, v in self.c.items() if
                k not in ["name", "tags", "additional_tags", "usable_targets"]}


class RulesetStruct(object):
    """
    {
      "version": "1",
      "name": "Mandatory checks for Red Hat container images"
      "description": "This set of checks is required to pass on every container image we, as Red Hat, release. For more info..."
      "contact_email": "cvp@redhat.com?"
      "checks": [{
        "name": "label_name",
        "tags": ["foo", "bar"],
        "additional_tags": ["baz"],
        "usable_targets": ["image", "dockerfile"],
      }, {}...
  ]}
    """
    def __init__(self, ruleset_dict):
        self.d = ruleset_dict
        # TODO: validate ruleset
        self._checks = None

    def _get(self, *path):
        return nicer_get(self.d, True, *path)

    def __str__(self):
        return "%s" % self.name

    @property
    def version(self):
        return self._get("version")

    @property
    def name(self):
        return self._get("name")

    @property
    def description(self):
        return self._get("description")

    @property
    def contact_email(self):
        return self._get("contact_email")

    @property
    def checks(self):
        if self._checks is None:
            self._checks = [CheckStruct(c) for c in self._get("checks")]
        return self._checks
