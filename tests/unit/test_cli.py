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

from click.testing import CliRunner
from colin.cli.colin import check, list_checks, list_rulesets


def _call_colin(fnc, parameters=None):
    runner = CliRunner()
    if not parameters:
        return runner.invoke(fnc)
    else:
        return runner.invoke(fnc, parameters)


def _common_help_options(result):
    assert "-r, --ruleset TEXT" in result.output
    assert "-f, --ruleset-file FILENAME" in result.output
    assert "--debug" in result.output
    assert "--json FILENAME" in result.output
    assert "-t, --tag TEXT" in result.output
    assert "-v, --verbose" in result.output
    assert "-h, --help" in result.output


def test_check_command():
    result = _call_colin(check)
    expected_output = """Usage: check [OPTIONS] TARGET

Error: Missing argument "target".
"""
    assert result.exit_code == 2
    assert result.output == expected_output


def test_check_help_command():
    result = _call_colin(check, parameters=["-h"])
    assert result.exit_code == 0
    _common_help_options(result)
    assert "-s, --stat" in result.output


def test_list_checks():
    result = _call_colin(list_checks)
    expected_output = """maintainer_label
   -> Label 'maintainer' has to be specified.
   -> The name and email of the maintainer (usually the submitter).
   -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
   -> maintainer, label, required

from_tag_not_latest
   -> In FROM, tag has to be specified and not 'latest'.
   -> Using the 'latest' tag may cause unpredictable builds.It is recommended that a specific tag is used in the FROM.
   -> https://fedoraproject.org/wiki/Container:Guidelines#FROM
   -> dockerfile, from, baseimage, latest, required

maintainer_deprecated
   -> Dockerfile instruction `MAINTAINER` is deprecated.
   -> Replace with label 'maintainer'.
   -> https://docs.docker.com/engine/reference/builder/#maintainer-deprecated
   -> dockerfile, maintainer, deprecated, required

"""
    assert result.exit_code == 0
    assert result.output == expected_output
    assert _call_colin(list_checks, parameters=["-r", "default"]).output == \
           _call_colin(list_checks).output


def test_list_checks_help_command():
    result = _call_colin(list_checks, parameters=["-h"])
    _common_help_options(result)
    assert result.exit_code == 0


def test_list_checks_fedora():
    result = _call_colin(list_checks, parameters=["-r", "fedora"])
    assert result.exit_code == 0
    assert "maintainer_label" in result.output
    assert "maintainer_deprecated" in result.output
    assert "from_tag_not_latest" in result.output


def test_list_rulesets():
    result = _call_colin(list_rulesets)
    assert "fedora" in result.output
    assert "default" in result.output
    assert result.exit_code == 0


def test_list_rulesets_help_command():
    result = _call_colin(list_rulesets, parameters=["-h"])
    expected_result = """Usage: list-rulesets [OPTIONS]

  List available rulesets.

Options:
  --debug     Enable debugging mode (debugging logs, full tracebacks).
  -h, --help  Show this message and exit.
"""
    assert result.exit_code == 0
    assert result.output == expected_result
