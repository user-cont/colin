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
import colin
import pytest

from tests.conftest import BASH_IMAGE, LS_IMAGE


@pytest.fixture()
def ruleset():
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
            {
                "name": "help_file_or_readme"
            }
        ]
    }


@pytest.mark.parametrize("image_name,should_pass", [
    (LS_IMAGE, False),
    (BASH_IMAGE, True),
])
def test_help_file_or_readme(ruleset, image_name, should_pass):
    results = colin.run(target=image_name, ruleset=ruleset, logging_level=10)
    assert results.ok
    assert results.fail is not should_pass

