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

from colin.core.target import ImageName


@pytest.mark.parametrize("string_input,image_result", [
    ("fedora", (None, None, 'fedora', None, None)),
    ("fedora:27", (None, None, 'fedora', '27', None)),
    ("docker.io/fedora", ('docker.io', None, 'fedora', None, None)),
    ("docker.io/fedora:latest", ('docker.io', None, 'fedora', 'latest', None)),
    ("docker.io/modularitycontainers/conu", ('docker.io', 'modularitycontainers', 'conu', None, None)),
    ("docker.io/centos/postgresql-96-centos7",
     ('docker.io', 'centos', 'postgresql-96-centos7', None, None)),
    ("some-registry.example.com:8888/rhel6",
     ('some-registry.example.com:8888', None, 'rhel6', None, None)),
    ("some-registry.example.com:8888/rhel6:some-example-6.10-something-26365-20180322014912",
     ('some-registry.example.com:8888', None, 'rhel6', 'some-example-6.10-something-26365-20180322014912', None)),
    ("fedora@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     (None, None, 'fedora', None, 'sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')),
    ("docker.io/fedora@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     ('docker.io', None, 'fedora', None, 'sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')),
    ("docker.io/centos/postgresql-96-centos7@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     ('docker.io', 'centos', 'postgresql-96-centos7', None,
      'sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')),
])
def test_image_class(string_input, image_result):
    image_name = ImageName.parse(string_input)
    registry, namespace, repository, tag, digest = image_result
    assert image_name.registry == registry
    assert image_name.namespace == namespace
    assert image_name.repository == repository
    assert image_name.tag == tag
    assert image_name.digest == digest
