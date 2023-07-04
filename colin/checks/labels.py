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

from colin.core.checks.labels import (
    LabelAbstractCheck,
    InheritedOptionalLabelAbstractCheck,
)
from colin.core.checks.fmf_check import FMFAbstractCheck


class ArchitectureLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "architecture_label"


class AuthoritativeSourceUrlLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "authoritative_source-url_label"


class BuildDateLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "build-date_label"
    # TODO: Check the RFC 3339 date-time format


class BuildHostLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "com.redhat.build-host_label"


class ComRedhatComponentLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "com.redhat.component_label"
    # TODO: Check the format


class DescriptionLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "description_label"


class DescriptionOrIoK8sDescriptionLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "description_or_io.k8s.description_label"


class DistributionScopeLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "distribution-scope_label"


class HelpLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "help_label"


class IoK8sDescriptionLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "io.k8s.description_label"


class IoK8sDisplayNameLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "io.k8s.display-name_label"


class MaintainerLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "maintainer_label"


class NameLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "name_label"


class ReleaseLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "release_label"


class SummaryLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "summary_label"


class UrlLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "url_label"


class RunOrUsageLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "run_or_usage_label"


class VcsRefLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "vcs-ref_label"


class VcsTypeLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "vcs-type_label"


class VcsUrlLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "vcs-url_label"


class VendorLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "vendor_label"


class VersionLabelCheck(FMFAbstractCheck, LabelAbstractCheck):
    name = "version_label"


class InheritedOptionalLabelCheck(
    FMFAbstractCheck, InheritedOptionalLabelAbstractCheck
):
    name = "inherited_labels"
