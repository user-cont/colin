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
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

import six

from .constant import COLOURS, ERROR, FAILED, OUTPUT_CHARS, PASSED
from ..utils.caching_iterable import CachingIterable


class CheckResult(object):
    def __init__(self, ok, description, message, reference_url, check_name, logs):
        self.ok = ok
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name
        self.logs = logs

    @property
    def status(self):
        return PASSED if self.ok else FAILED

    def __str__(self):
        return f"{self.status}:{self.message}"


class DockerfileCheckResult(CheckResult):
    def __init__(
        self,
        ok,
        description,
        message,
        reference_url,
        check_name,
        lines=None,
        correction_diff=None,
    ):
        super(DockerfileCheckResult, self).__init__(
            ok, description, message, reference_url, check_name
        )
        self.lines = lines
        self.correction_diff = correction_diff


class CheckResults(object):
    def __init__(self, results):
        self.results = CachingIterable(results)

    @property
    def results_per_check(self):
        return {r.check_name: r for r in self.results}

    @property
    def _dict_of_results(self):
        """
        Get the dictionary representation of results

        :return: dict (str -> dict (str -> str))
        """
        result_list = [
            {
                "name": r.check_name,
                "ok": r.ok,
                "status": r.status,
                "description": r.description,
                "message": r.message,
                "reference_url": r.reference_url,
                "logs": r.logs,
            }
            for r in self.results
        ]
        return {"checks": result_list}

    @property
    def json(self):
        """
        Get the json representation of results

        :return: str
        """
        return json.dumps(self._dict_of_results, indent=4)

    def save_json_to_file(self, file):
        json.dump(obj=self._dict_of_results, fp=file, indent=4)

    @property
    def xunit(self):
        """
        Get the xunit representation of results

        :return: str
        """

        top = Element("testsuites")

        testsuite = SubElement(top, "testsuite")

        for r in self.results:
            testcase = SubElement(
                testsuite,
                "testcase",
                {
                    "name": r.check_name,
                    # Can't use PASSED or FAILED global variables because their values are PASS
                    # and FAIL respectively and xunit wants them suffixed with -ED.
                    "status": "PASSED" if r.ok else "FAILED",
                    "url": r.reference_url,
                },
            )
            if r.logs:
                logs = SubElement(testcase, "logs")
                for log in r.logs:
                    log = SubElement(
                        logs,
                        "log",
                        {
                            "message": log,
                            "result": "INFO",
                            "waiver_authorization": "Not Waivable",
                        },
                    )

        rough_string = tostring(top, "utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def save_xunit_to_file(self, file):
        """
        Write the contents of xunit to the passed file pointer.
        :param file: the file to which to write
        :return: return code of the write command
        """
        file.write(self.xunit)

    @property
    def statistics(self):
        """
        Get the dictionary with the count of the check-statuses

        :return: dict(str -> int)
        """
        result = {}
        for r in self.results:
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

    def generate_pretty_output(self, stat, verbose, output_function, logs=True):
        """
        Send the formated to the provided function

        :param stat: if True print stat instead of full output
        :param verbose: bool
        :param output_function: function to send output to
        """

        has_check = False
        for r in self.results:
            has_check = True
            if stat:
                output_function(OUTPUT_CHARS[r.status], fg=COLOURS[r.status], nl=False)
            else:
                output_function(str(r), fg=COLOURS[r.status])
                if verbose:
                    output_function(
                        f"  -> {r.description}\n  -> {r.reference_url}",
                        fg=COLOURS[r.status],
                    )
                    if logs and r.logs:
                        output_function("  -> logs:", fg=COLOURS[r.status])
                        for line in r.logs:
                            output_function(f"    -> {line}", fg=COLOURS[r.status])

        if not has_check:
            output_function("No check found.")
        elif stat and not verbose:
            output_function("")
        else:
            output_function("")
            for status, count in six.iteritems(self.statistics):
                output_function(f"{status}:{count} ", nl=False)
            output_function("")

    def get_pretty_string(self, stat, verbose):
        """
        Pretty string representation of the results

        :param stat: bool
        :param verbose: bool
        :return: str
        """
        pretty_output = _PrettyOutputToStr()
        self.generate_pretty_output(
            stat=stat, verbose=verbose, output_function=pretty_output.save_output
        )
        return pretty_output.result


class FailedCheckResult(CheckResult):
    def __init__(self, check, logs=None):
        super(FailedCheckResult, self).__init__(
            ok=False,
            message=check.message,
            description=check.description,
            reference_url=check.reference_url,
            check_name=check.name,
            logs=logs or [],
        )

    @property
    def status(self):
        return ERROR


class _PrettyOutputToStr(object):
    def __init__(self):
        self.result = ""

    def save_output(self, text=None, nl=True):
        text = text or ""
        self.result += text
        if nl:
            self.result += "\n"
