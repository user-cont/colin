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

import pytest

import colin
from colin.checks.labels import RunOrUsageLabelCheck
from colin.core.target import ImageTarget
from tests.conftest import LABELS_IMAGE


@pytest.fixture("session")
def labels_target():
    target = ImageTarget(target=LABELS_IMAGE,
                         logging_level=10,
                         target_type="image",
                         pull=False)
    yield target
    target.clean_up()


@pytest.fixture()
def empty_ruleset():
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
        ]
    }


def get_results_from_colin_labels_image():
    return colin.run(LABELS_IMAGE, "image", ruleset_name="fedora",
                     logging_level=logging.DEBUG, pull=False)


def test_colin_image():
    assert get_results_from_colin_labels_image()


def test_labels_in_image():
    result = get_results_from_colin_labels_image()
    assert result
    expected_dict = {"maintainer_label": "PASS",
                     "name_label": "PASS",
                     "com.redhat.component_label": "PASS",
                     "summary_label": "PASS",
                     "version_label": "PASS",
                     "run_or_usage_label": "PASS",
                     "release_label": "FAIL",
                     "architecture_label": "FAIL",
                     "url_label": "PASS",
                     "help_label": "FAIL",
                     "build-date_label": "FAIL",
                     "distribution-scope_label": "FAIL",
                     "vcs-ref_label": "FAIL",
                     "vcs-type_label": "FAIL",
                     "description_label": "PASS",
                     "io.k8s.description_label": "PASS",
                     "vcs-url_label": "FAIL",
                     "help_file_or_readme": "FAIL",
                     # "cmd_or_entrypoint": "PASS",
                     # "no_root": "FAIL",
                     }
    labels_dict = {}
    for res in result.results:
        labels_dict[res.check_name] = res.status
    assert labels_dict == expected_dict


@pytest.mark.parametrize("labels, should_pass", [
    (["run"], True),
    (["usage"], False),
    (["run", "usage"], True),
    (["something", "different"], False),
    (["something", "completely", "different"], False),
])
def test_multiple_labels_check(labels, should_pass, labels_target):
    check = RunOrUsageLabelCheck()
    check.labels = labels

    result = check.check(labels_target)

    assert result.ok == should_pass
