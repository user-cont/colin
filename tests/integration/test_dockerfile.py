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
import pytest
import six

import colin


@pytest.fixture()
def dockerfile_with_missing_from():
    return six.StringIO("FROMM base\nENV a=b\nLABEL c=d\n")


@pytest.fixture()
def ruleset_from_tag_not_latest():
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
            {"name": "from_tag_not_latest"},
        ],
    }


def test_missing_from(dockerfile_with_missing_from, ruleset_from_tag_not_latest):
    result = colin.run(
        target=dockerfile_with_missing_from,
        target_type="dockerfile",
        ruleset=ruleset_from_tag_not_latest,
    )
    assert result
    assert not result.ok
    assert result.results_per_check["from_tag_not_latest"]
    assert not result.results_per_check["from_tag_not_latest"].ok
    assert result.results_per_check["from_tag_not_latest"].status == "ERROR"
    assert (
        result.results_per_check["from_tag_not_latest"].logs[0]
        == "Cannot find FROM instruction."
    )
