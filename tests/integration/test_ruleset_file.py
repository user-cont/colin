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

import tempfile

import pytest
import yaml

import colin
from colin.core.exceptions import ColinRulesetException


@pytest.fixture()
def ruleset():
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
            {"name": "maintainer_label"},
            {"name": "name_label"},
            {"name": "com.redhat.component_label"},
            {"name": "help_label"},
        ],
    }


@pytest.fixture()
def ruleset_unknown_check():
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [{"name": "maintainer_label"}, {"name": "i_forgot_the_name"}],
    }


@pytest.fixture()
def ruleset_coupled():
    return {
        "version": "1",
        "name": "Laughing out loud coublet ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
            {
                "names": [
                    "maintainer_label",
                    "name_label",
                    "com.redhat.component_label",
                ],
                "additional_tags": ["required"],
            }
        ],
    }


@pytest.fixture()
def expected_dict():
    return {
        "maintainer_label": "PASS",
        "name_label": "PASS",
        "com.redhat.component_label": "PASS",
        "help_label": "FAIL",
    }


def get_results_from_colin_labels_image(
    image, ruleset_name=None, ruleset_file=None, ruleset=None
):
    return colin.run(
        image.target_name,
        image.target_type,
        ruleset_name=ruleset_name,
        ruleset_file=ruleset_file,
        ruleset=ruleset,
    )


def test_specific_ruleset_as_fileobj(tmpdir, ruleset, expected_dict, target_label):
    (_, t) = tempfile.mkstemp(dir=str(tmpdir))

    with open(t, "w") as f:
        yaml.dump(ruleset, f)
    with open(t, "r") as f:
        result = get_results_from_colin_labels_image(image=target_label, ruleset_file=f)
    assert result
    labels_dict = {res.check_name: res.status for res in result.results}
    for key in expected_dict.keys():
        assert labels_dict[key] == expected_dict[key]


def test_specific_ruleset_directly(ruleset, expected_dict, target_label):
    result = get_results_from_colin_labels_image(image=target_label, ruleset=ruleset)
    assert result
    labels_dict = {res.check_name: res.status for res in result.results}
    for key in expected_dict.keys():
        assert labels_dict[key] == expected_dict[key]


def test_get_checks_directly(ruleset):
    checks = colin.get_checks(ruleset=ruleset)
    assert checks


def test_coupled_ruleset(ruleset_coupled):
    checks = colin.get_checks(ruleset=ruleset_coupled)
    assert checks
    assert len(checks) == 3
    for c in checks:
        assert "required" in c.tags


def test_unknown_check(ruleset_unknown_check):
    with pytest.raises(ColinRulesetException) as ex:
        colin.get_checks(ruleset=ruleset_unknown_check)
    assert (
        str(ex.value) == "Check i_forgot_the_name can't be loaded, we couldn't find it."
    )


def test_skip(ruleset):
    checks = colin.get_checks(ruleset=ruleset, skips=["name_label", "help_label"])
    assert len(checks) == 2
    for check in checks:
        assert check.name in ["com.redhat.component_label", "maintainer_label"]
