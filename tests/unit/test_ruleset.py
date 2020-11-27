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

import os

import pytest

from colin.core.exceptions import ColinRulesetException
from colin.core.ruleset.ruleset import Ruleset


def test_ruleset_yaml():
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    lol_ruleset_path = os.path.join(tests_dir, "data", "lol-ruleset.yaml")
    with open(lol_ruleset_path, "r") as fd:
        r = Ruleset(ruleset_file=fd)
        checks = r.get_checks(None)
    assert len(checks) == 1


def test_ruleset_json():
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    lol_ruleset_path = os.path.join(tests_dir, "data", "lol-ruleset.json")
    with open(lol_ruleset_path, "r") as fd:
        r = Ruleset(ruleset_file=fd)
        checks = r.get_checks(None)
    assert len(checks) == 1


def test_ruleset_tags():
    tags = ["a", "banana"]
    r = {"version": "1", "checks": [{"name": "name_label", "tags": tags[:]}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    assert len(checks) == 1
    assert checks[0].tags == tags


def test_ruleset_additional_tags():
    tags = ["a"]
    r = {"version": "1", "checks": [{"name": "name_label", "additional_tags": tags[:]}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    assert len(checks) == 1
    assert list(set(tags).intersection(set(checks[0].tags))) == tags


@pytest.mark.parametrize(
    "tags,expected_check_name", [(["banana"], None), (["name"], "name_label")]
)
def test_ruleset_tags_filtering(tags, expected_check_name):
    r = {"version": "1", "checks": [{"name": "name_label"}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None, tags=tags)
    if expected_check_name:
        assert len(checks) == 1
        assert checks[0].name == expected_check_name
    else:
        assert len(checks) == 0


# version in ruleset, should this case raise an exception?
@pytest.mark.parametrize(
    "version,should_raise",
    [
        (1, False),
        ("1", False),
        ("banana", True),
        (None, True),
        ("", True),
        ("<blank>", True),
    ],
)
def test_ruleset_version(version, should_raise):
    if version == "<blank>":
        r = {"banana": 123}
    else:
        r = {"version": version}
    if should_raise:
        with pytest.raises(ColinRulesetException):
            Ruleset(ruleset=r)
    else:
        assert Ruleset(ruleset=r)


def test_ruleset_override():
    m = "my-message!"
    r = {
        "version": "1",
        "checks": [
            {"name": "name_label", "tags": ["a", "b"], "just": "testing", "message": m}
        ],
    }
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    assert len(checks) == 1
    assert checks[0].message == m
    assert checks[0].just == "testing"
