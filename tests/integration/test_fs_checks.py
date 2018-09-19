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

import colin


@pytest.fixture()
def ruleset():
    """ simple ruleset as a pytest fixture """
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


def test_help_file_or_readme_bash(ruleset, target_bash):
    help_file_or_readme_test(ruleset=ruleset,
                             image=target_bash,
                             should_pass=True)


def test_help_file_or_readme_ls(ruleset, target_ls):
    help_file_or_readme_test(ruleset=ruleset,
                             image=target_ls,
                             should_pass=False)


def help_file_or_readme_test(ruleset, image, should_pass):
    """ verify that help_file_or_readme check works well """
    results = colin.run(target=image.target_name,
                        target_type=image.target_type,
                        ruleset=ruleset, logging_level=10, pull=False)
    assert results.ok
    assert results.fail is not should_pass
