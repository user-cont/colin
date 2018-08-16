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
import shutil

import colin.checks
from colin.core.loader import CheckLoader


def test_upstream_checks_can_be_loaded():
    """ check whether all upstream checks can be loaded """
    colin_checks_path = colin.checks.__file__
    colin_checks_dir = os.path.dirname(colin_checks_path)
    l = CheckLoader([colin_checks_dir])
    assert l.check_classes
    assert l.mapping["bzcomponent_deprecated"]
    assert l.mapping["architecture_label_capital_deprecated"]
    assert l.mapping["bzcomponent_deprecated"]
    assert l.mapping["install_label_capital_deprecated"]
    assert l.mapping["name_label_capital_deprecated"]
    assert l.mapping["release_label_capital_deprecated"]
    assert l.mapping["uninstall_label_capital_deprecated"]
    assert l.mapping["version_label_capital_deprecated"]
    assert l.mapping["architecture_label"]
    assert l.mapping["authoritative_source-url_label"]
    assert l.mapping["build-date_label"]
    assert l.mapping["com.redhat.build-host_label"]
    assert l.mapping["com.redhat.component_label"]
    assert l.mapping["description_label"]
    assert l.mapping["description_or_io.k8s.description_label"]
    assert l.mapping["distribution-scope_label"]
    assert l.mapping["help_label"]
    assert l.mapping["io.k8s.description_label"]
    assert l.mapping["io.k8s.display-name_label"]
    assert l.mapping["maintainer_label"]
    assert l.mapping["name_label"]
    assert l.mapping["release_label"]
    assert l.mapping["summary_label"]
    assert l.mapping["url_label"]
    assert l.mapping["run_or_usage_label"]
    assert l.mapping["vcs-ref_label"]
    assert l.mapping["vcs-type_label"]
    assert l.mapping["vcs-url_label"]
    assert l.mapping["vendor_label"]
    assert l.mapping["version_label"]
    assert l.mapping["cmd_or_entrypoint"]
    assert l.mapping["help_file_or_readme"]
    assert l.mapping["no_root"]
    assert l.mapping["shell_runnable"]
    assert l.mapping["from_tag_not_latest"]
    assert l.mapping["maintainer_deprecated"]


def test_loading_custom_check(tmpdir):
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    a_check_dir = os.path.join(tests_dir, "data", "a_check")
    shutil.copytree(a_check_dir, str(tmpdir.join("a_check")))
    l = CheckLoader([str(tmpdir)])
    assert len(l.check_classes) == 3
    assert l.mapping["a-peter-file-check"]
    assert l.mapping["this-is-a-funky-check"]
