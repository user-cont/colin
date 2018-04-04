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


@pytest.mark.parametrize("string_input,image_str", [
    ("fedora", "Image: registry='None' namespace='None' repository='fedora' tag='None' digest='None'"),
    ("fedora:27", "Image: registry='None' namespace='None' repository='fedora' tag='27' digest='None'"),
    ("docker.io/fedora", "Image: registry='docker.io' namespace='None' repository='fedora' tag='None' digest='None'"),
    ("docker.io/fedora:latest",
     "Image: registry='docker.io' namespace='None' repository='fedora' tag='latest' digest='None'"),
    ("docker.io/modularitycontainers/conu",
     "Image: registry='docker.io' namespace='modularitycontainers' repository='conu' tag='None' digest='None'"),
    ("docker.io/centos/postgresql-96-centos7",
     "Image: registry='docker.io' namespace='centos' repository='postgresql-96-centos7' tag='None' digest='None'"),
    ("brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel6",
     "Image: registry='brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888' namespace='None' repository='rhel6' tag='None' digest='None'"),
    ("brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel6:guest-rhel-6.10-docker-26365-20180322014912",
     "Image: registry='brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888' namespace='None' repository='rhel6' tag='guest-rhel-6.10-docker-26365-20180322014912' digest='None'"),
    ("fedora@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Image: registry='None' namespace='None' repository='fedora' tag='None' digest='sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'"),
])
def test_image_class(string_input, image_str):
    image_name = ImageName.parse(string_input)
    assert str(image_name) == image_str
