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
    expected_dict = {"maintainer_label_required": "PASS",
                     "name_label_required": "PASS",
                     "com_redhat_component_label_required": "PASS",
                     "summary_label_required": "PASS",
                     "version_label_required": "PASS",
                     "usage_label_required": "FAIL",
                     "release_label": "FAIL",
                     "architecture_label": "FAIL",
                     "url_label": "WARN",
                     "help_label": "WARN",
                     "build-date_label": "WARN",
                     "distribution-scope_label": "WARN",
                     "vcs-ref_label": "WARN",
                     "vcs-type_label": "WARN",
                     "description_label": "PASS",
                     "io.k8s.description_label": "PASS",
                     "vcs-url_label": "WARN",
                     "io.openshift.expose-services_label": "WARN",
                     "help_file_or_readme_required": "FAIL",
                     "cmd_or_entrypoint": "PASS",
                     "no_root": "FAIL",
    }
    labels_dict = {}
    for res in result.all_results:
        labels_dict[res.check_name] = res.status
    for key in expected_dict.keys():
        assert labels_dict[key] == expected_dict[key]
