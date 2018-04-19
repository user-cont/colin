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

import six
from six import iteritems

from ..core.constant import (COLOURS, ERROR, FAILED, OPTIONAL, OUTPUT_CHARS,
                             PASSED, REQUIRED, WARNING)


class CheckResult(object):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
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
        return "{}:{}".format(self.status,
                              self.message)


class DockerfileCheckResult(CheckResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, lines=None,
                 correction_diff=None):
        super(self.__class__, self) \
            .__init__(ok, description, message, reference_url, check_name, severity)
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

    @property
    def statistics(self):
        """
        Get the dictionary with the count of the check-statuses

        :return: dict(str -> int)
        """
        result = {}
        for r in self.all_results:
            result.setdefault(r.status, 0)
            result[r.status] += 1
        return result

    @property
    def ok(self):
        """
        If the results ended without any error


        :return: True, if there is no check which ends with error status
        """
        return ERROR not in self.statistics

    @property
    def fail(self):
        """
        If the results ended without any fail


        :return: True, if there is no check which ends with fail status
        """
        return FAILED in self.statistics

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

    def generate_pretty_output(self, stat, verbose, output_function):
        """
        Send the formated to the provided function

        :param stat: if True print stat instead of full output
        :param verbose: bool
        :param output_function: function to send output to
        """
        for group, check_results in self.results:

            group_title_printed = False
            for r in check_results:

                if not group_title_printed:
                    output_function("{}:".format(group.upper()),
                                    nl=not stat)
                    group_title_printed = True

                if stat:
                    output_function(OUTPUT_CHARS[r.status],
                                    fg=COLOURS[r.status],
                                    nl=False)
                else:
                    output_function(str(r), fg=COLOURS[r.status])
                    if verbose:
                        output_function("  -> {}\n"
                                        "  -> {}".format(r.description,
                                                         r.reference_url),
                                        fg=COLOURS[r.status])

            if group_title_printed and stat:
                output_function("")

        if not stat or verbose:
            output_function("")
            for status, count in six.iteritems(self.statistics):
                output_function("{}:{} ".format(status, count), nl=False)
            output_function("")

    def get_pretty_string(self, stat, verbose):
        """
        Pretty string representation of the results

        :param stat: bool
        :param verbose: bool
        :return: str
        """
        pretty_output = _PrettyOutputToStr()
        self.generate_pretty_output(stat=stat,
                                    verbose=verbose,
                                    output_function=pretty_output.save_output)
        return pretty_output.result


class FailedCheckResult(CheckResult):

    def __init__(self, check, exception):
        super(self.__class__, self) \
            .__init__(ok=False,
                      message=check.message,
                      description=str(exception),
                      reference_url="",
                      check_name=check.name,
                      severity=check.severity,
                      logs=[str(exception)]
                      )

    @property
    def status(self):
        return ERROR


class _PrettyOutputToStr(object):

    def __init__(self):
        self.result = ""

    def save_output(self, text=None, fg=None, nl=True):
        text = text or ""
        self.result += text
        if nl:
            self.result += "\n"
