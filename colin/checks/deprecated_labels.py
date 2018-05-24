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

from colin.core.checks.labels import DeprecatedLabelAbstractCheck


class ArchitectureLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "architecture_label_capital_deprecated"

    def __init__(self):
        super(ArchitectureLabelCapitalDeprecatedCheck, self). \
            __init__(message="Label 'Architecture' is deprecated.",
                     description="Replace with 'architecture'.",
                     reference_url="?????",
                     tags=["architecture", "label", "capital", "deprecated"],
                     old_label="Architecture",
                     new_label="architecture")


class BZComponentDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "bzcomponent_deprecated"

    def __init__(self):
        super(BZComponentDeprecatedCheck, self) \
            .__init__(message="Label 'BZComponent' is deprecated.",
                      description="Replace with 'com.redhat.component'.",
                      reference_url="?????",
                      tags=["com.redhat.component", "bzcomponent", "label", "deprecated"],
                      old_label="BZComponent",
                      new_label="com.redhat.component")


class InstallLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "install_label_capital_deprecated"

    def __init__(self):
        super(InstallLabelCapitalDeprecatedCheck, self) \
            .__init__(message="Label 'INSTALL' is deprecated.",
                      description="Replace with 'install'.",
                      reference_url="?????",
                      tags=["install", "label", "capital", "deprecated"],
                      old_label="INSTALL",
                      new_label="install")


class NameLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "name_label_capital_deprecated"

    def __init__(self):
        super(NameLabelCapitalDeprecatedCheck, self) \
            .__init__(message="Label 'Name' is deprecated.",
                      description="Replace with 'name'.",
                      reference_url="?????",
                      tags=["name", "label", "capital", "deprecated"],
                      old_label="Name",
                      new_label="name")


class ReleaseLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "release_label_capital_deprecated"

    def __init__(self):
        super(ReleaseLabelCapitalDeprecatedCheck, self) \
            .__init__(message="Label 'Release' is deprecated.",
                      description="Replace with 'release'.",
                      reference_url="?????",
                      tags=["release", "label", "capital", "deprecated"],
                      old_label="Release",
                      new_label="release")


class UninstallLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "uninstall_label_capital_deprecated"

    def __init__(self):
        super(UninstallLabelCapitalDeprecatedCheck, self) \
            .__init__(message="Label 'UNINSTALL' is deprecated.",
                      description="Replace with 'uninstall'.",
                      reference_url="?????",
                      tags=["uninstall", "label", "capital", "deprecated"],
                      old_label="UNINSTALL",
                      new_label="uninstall")


class VersionLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = "version_label_capital_deprecated"

    def __init__(self):
        super(VersionLabelCapitalDeprecatedCheck, self) \
            .__init__(message="Label 'Version' is deprecated.",
                      description="Replace with 'version'.",
                      reference_url="?????",
                      tags=["version", "label", "capital", "deprecated"],
                      old_label="Version",
                      new_label="version")
