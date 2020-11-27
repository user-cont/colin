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
    check_loader = CheckLoader([colin_checks_dir])
    assert check_loader.check_classes
    assert check_loader.mapping["bzcomponent_deprecated"]
    assert check_loader.mapping["architecture_label_capital_deprecated"]
    assert check_loader.mapping["bzcomponent_deprecated"]
    assert check_loader.mapping["install_label_capital_deprecated"]
    assert check_loader.mapping["name_label_capital_deprecated"]
    assert check_loader.mapping["release_label_capital_deprecated"]
    assert check_loader.mapping["uninstall_label_capital_deprecated"]
    assert check_loader.mapping["version_label_capital_deprecated"]
    assert check_loader.mapping["architecture_label"]
    assert check_loader.mapping["authoritative_source-url_label"]
    assert check_loader.mapping["build-date_label"]
    assert check_loader.mapping["com.redhat.build-host_label"]
    assert check_loader.mapping["com.redhat.component_label"]
    assert check_loader.mapping["description_label"]
    assert check_loader.mapping["description_or_io.k8s.description_label"]
    assert check_loader.mapping["distribution-scope_label"]
    assert check_loader.mapping["help_label"]
    assert check_loader.mapping["io.k8s.description_label"]
    assert check_loader.mapping["io.k8s.display-name_label"]
    assert check_loader.mapping["maintainer_label"]
    assert check_loader.mapping["name_label"]
    assert check_loader.mapping["release_label"]
    assert check_loader.mapping["summary_label"]
    assert check_loader.mapping["url_label"]
    assert check_loader.mapping["run_or_usage_label"]
    assert check_loader.mapping["vcs-ref_label"]
    assert check_loader.mapping["vcs-type_label"]
    assert check_loader.mapping["vcs-url_label"]
    assert check_loader.mapping["vendor_label"]
    assert check_loader.mapping["version_label"]
    assert check_loader.mapping["cmd_or_entrypoint"]
    assert check_loader.mapping["help_file_or_readme"]
    assert check_loader.mapping["no_root"]
    # assert check_loader.mapping["shell_runnable"]   # FIXME: commented out before move to podman
    assert check_loader.mapping["from_tag_not_latest"]
    assert check_loader.mapping["maintainer_deprecated"]


def test_loading_custom_check(tmpdir):
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    a_check_dir = os.path.join(tests_dir, "data", "a_check")
    shutil.copytree(a_check_dir, str(tmpdir.join("a_check")))
    check_loader = CheckLoader([str(tmpdir)])
    assert len(check_loader.check_classes) == 3
    assert check_loader.mapping["a-peter-file-check"]
    assert check_loader.mapping["this-is-a-funky-check"]


def test_import_class():
    check_loader = CheckLoader([])
    check_name = "ArchitectureLabelCheck"
    imported_class = check_loader.import_class(f"colin.checks.labels.{check_name}")
    assert imported_class.name == "architecture_label"
