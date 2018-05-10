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


def get_results_from_colin_labels_image():
    return colin.run("colin-labels", ruleset_name="fedora")


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
                     "usage_label": "FAIL",
                     "release_label": "FAIL",
                     "architecture_label": "FAIL",
                     "url_label": "FAIL",
                     "help_label": "FAIL",
                     "build-date_label": "FAIL",
                     "distribution-scope_label": "FAIL",
                     "vcs-ref_label": "FAIL",
                     "vcs-type_label": "FAIL",
                     "description_label": "PASS",
                     "io.k8s.description_label": "PASS",
                     "vcs-url_label": "FAIL",
                     "io.openshift.expose-services_label": "FAIL",
                     "help_file_or_readme": "FAIL",
                     "cmd_or_entrypoint": "PASS",
                     "no_root": "FAIL",
                     }
    labels_dict = {}
    for res in result.results:
        labels_dict[res.check_name] = res.status
    for key in expected_dict.keys():
        assert labels_dict[key] == expected_dict[key]
