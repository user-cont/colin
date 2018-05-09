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

import colin
import pytest
from conu import DockerBackend


@pytest.fixture()
def ruleset():
    return {
        "dynamic": {
            "required": [
                "shell"
            ]
        }
    }


def test_dynamic_check_ls(ruleset):
    image = build_image(dockerfile="Dockerfile-ls")
    results = colin.run(target=image, ruleset=ruleset)
    assert not results.ok


def test_dynamic_check_bash(ruleset):
    image = build_image(dockerfile="Dockerfile-bash")
    results = colin.run(target=image, ruleset=ruleset)
    assert results.ok


def build_image(dockerfile):
    with DockerBackend() as backend:
        name = 'colin-test-dynamic-check-image'
        integration_tests_dir = os.path.abspath(os.path.dirname(__file__))
        image_dir = os.path.join(integration_tests_dir, "dynamic_check_data")

        return backend.ImageClass.build(os.path.join(image_dir), tag=name, dockerfile=dockerfile)
