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
from colin.core.checks.fmf_check import FMFAbstractCheck


class ArchitectureLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "architecture_label_capital_deprecated"


class BZComponentDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "bzcomponent_deprecated"


class InstallLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "_install_label_capital_deprecated"


class NameLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "name_label_capital_deprecated"


class ReleaseLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "release_label_capital_deprecated"


class UninstallLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "uninstall_label_capital_deprecated"


class VersionLabelCapitalDeprecatedCheck(FMFAbstractCheck, DeprecatedLabelAbstractCheck):
    name = "version_label_capital_deprecated"
