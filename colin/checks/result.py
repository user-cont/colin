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

from ..core.constant import REQUIRED, PASSED, FAILED, WARNING, OPTIONAL


class CheckResult(object):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
        super().__init__()
        self.ok = ok
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name
        self.severity = severity
        self.logs = logs

    @property
    def status(self):
        statuses = {REQUIRED: (PASSED, FAILED),
                    OPTIONAL: (PASSED, WARNING)}
        status_ok, status_nok = statuses[self.severity]

        return status_ok if self.ok else status_nok

    def __str__(self):
        return "{}:{}:{}".format("ok " if self.ok else "nok",
                                 self.status,
                                 self.check_name)


class DockerfileCheckResult(CheckResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, lines=None,
                 correction_diff=None):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.lines = lines
        self.correction_diff = correction_diff


class CheckResults(object):

    def __init__(self, results):
        self._results = results
        self._generated = False
        self._generated_result = {}

    @property
    def _dict_of_results(self):
        """
        Get the dictionary representation of results

        :return: dict (str -> dict (str -> str))
        """
        result_json = {}
        for group, results in self.results:
            result_list = []
            for r in results:
                result_list.append({
                    'name': r.check_name,
                    'ok': r.ok,
                    'status': r.status,
                    'description': r.description,
                    'message': r.message,
                    'reference_url': r.reference_url,
                    'severity': r.severity,
                    'logs': r.logs,
                })
            result_json[group] = result_list
        return result_json

    @property
    def json(self):
        """
        Get the json representation of results

        :return: str
        """
        return json.dumps(self._dict_of_results, indent=4)

    @property
    def all_results(self):
        """
        Get the list of all results

        :return: list of Result instances
        """
        result = []
        for _, checks in self.results:
            result += checks
        return result

    def save_json_to_file(self, file):
        json.dump(obj=self._dict_of_results,
                  fp=file,
                  indent=4)

    @property
    def results(self):
        """
        Get the result generator

        :return: Generator of group generator of results
        """
        if self._generated:
            return iteritems(self._generated_result)
        else:
            return self._group_generator()

    def _group_generator(self):
        """
        Forward original generator of result groups, but saves the value for the future use.

        :return: yields the group generator
        """
        for group, group_result in self._results:
            self._generated_result.setdefault(group, [])
            yield group, self._result_generator(group=group,
                                                results=group_result)
        self._generated = True

    def _result_generator(self, group, results):
        """
        Forward the result from one generator and saves the value for the future use.

        :param group: str
        :param results: Result object generator
        :return: yields the values from original generator
        """
        for r in results:
            self._generated_result[group].append(r)
            yield r
