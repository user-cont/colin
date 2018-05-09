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

from six import iteritems


class AbstractCheck(object):

    def __init__(self, name, message, description, reference_url, tags):
        self.name = name
        self.message = message
        self.description = description
        self.reference_url = reference_url
        self.tags = tags
        self.severity = None

    def check(self, target):
        pass

    def __str__(self):
        return "{}\n" \
               "   -> {}\n" \
               "   -> {}\n" \
               "   -> {}\n" \
               "   -> {}\n" \
               "   -> {}\n".format(self.name,
                                   self.message,
                                   self.description,
                                   self.reference_url,
                                   self.tags,
                                   self.severity)

    @property
    def json(self):
        """
        Get json representation of the check

        :return: dict (str -> obj)
        """
        return {
            'name': self.name,
            'message': self.message,
            'description': self.description,
            'reference_url': self.reference_url,
            'tags': self.tags,
            'severity': self.severity,
        }

    @staticmethod
    def json_from_all_checks(checks):
        result_json = {}
        for (group, group_checks) in iteritems(checks):

            result_list = []
            for check in group_checks:
                result_list.append(check.json)

            result_json[group] = result_list
        return result_json

    @staticmethod
    def save_checks_to_json(file, checks):
        json.dump(obj=AbstractCheck.json_from_all_checks(checks=checks),
                  fp=file,
                  indent=4)
