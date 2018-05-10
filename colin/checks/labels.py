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

from colin.core.checks.labels import LabelCheck


class ArchitectureLabelCheck(LabelCheck):

    def __init__(self):
        super(ArchitectureLabelCheck, self) \
            .__init__(name="architecture_label",
                      message="Label 'architecture' has to be specified.",
                      description="Architecture the software in the image should target. "
                                  "(Optional: if omitted, it will be built "
                                  "for all supported Fedora Architectures)",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["architecture", "label"],
                      label="architecture",
                      required=True,
                      value_regex=None)


class AuthoritativeSourceUrlLabelCheck(LabelCheck):

    def __init__(self):
        super(AuthoritativeSourceUrlLabelCheck, self) \
            .__init__(name="authoritative_source-url_label",
                      message="Label 'authoritative-source-url' has to be specified.",
                      description="The authoritative registry in which the image is published.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["authoritative-source-url", "label"],
                      label="authoritative-source-url",
                      required=True,
                      value_regex=None)


class BuildDateLabelCheck(LabelCheck):

    def __init__(self):
        super(BuildDateLabelCheck, self) \
            .__init__(name="build-date_label",
                      message="Label 'build-date' has to be specified.",
                      description="Date/Time image was built as RFC 3339 date-time.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["build-date", "label"],
                      label="build-date",
                      required=True,
                      value_regex=None)
        # TODO: Check the RFC 3339 date-time format


class BuildHostLabelCheck(LabelCheck):

    def __init__(self):
        super(BuildHostLabelCheck, self) \
            .__init__(name="com.redhat.build-host_label",
                      message="Label 'com.redhat.build-host' has to be specified.",
                      description="The build host used to create an image for internal use and auditability, similar to the use in RPM.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["com.redhat.build-host", "build-host", "label"],
                      label="com.redhat.build-host",
                      required=True,
                      value_regex=None)


class ComRedhatComponentLabelCheck(LabelCheck):

    def __init__(self):
        super(ComRedhatComponentLabelCheck, self) \
            .__init__(name="com.redhat.component_label",
                      message="Label 'com.redhat.component' has to be specified.",
                      description="The Bugzilla component name where bugs against this container should be reported by users.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["com.redhat.component", "label"],
                      label="com.redhat.component",
                      required=True,
                      value_regex=None)
        # TODO: Check the format


class DescriptionLabelCheck(LabelCheck):

    def __init__(self):
        super(DescriptionLabelCheck, self) \
            .__init__(name="description_label",
                      message="Label 'description' has to be specified.",
                      description="Detailed description of the image.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["description", "label"],
                      label="description",
                      required=True,
                      value_regex=None)


class DescriptionScopeLabelCheck(LabelCheck):

    def __init__(self):
        super(DescriptionScopeLabelCheck, self) \
            .__init__(name="distribution-scope_label",
                      message="Label 'distribution-scope' has to be specified.",
                      description="Scope of intended distribution of the image. (private/authoritative-source-only/restricted/public)",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["distribution-scope", "label"],
                      label="distribution-scope",
                      required=True,
                      value_regex=None)


class HelpLabelCheck(LabelCheck):

    def __init__(self):
        super(HelpLabelCheck, self) \
            .__init__(name="help_label",
                      message="Label 'help' has to be specified.",
                      description="A runnable command which results in display of Help information.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["help", "label"],
                      label="help",
                      required=True,
                      value_regex=None)


class IoK8sDescriptionLabelCheck(LabelCheck):

    def __init__(self):
        super(IoK8sDescriptionLabelCheck, self) \
            .__init__(name="io.k8s.description_label",
                      message="Label 'io.k8s.description' has to be specified.",
                      description="Description of the container displayed in Kubernetes",
                      reference_url=["https://github.com/projectatomic/ContainerApplicationGenericLabels",
                                     "https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md#other-labels"],
                      tags=["io.k8s.description", "description", "label"],
                      label="io.k8s.description",
                      required=True,
                      value_regex=None)


class IoK8sDisplayNameLabelCheck(LabelCheck):

    def __init__(self):
        super(IoK8sDisplayNameLabelCheck, self) \
            .__init__(name="io.k8s.display-name_label",
                      message="Label 'io.k8s.display-name' has to be specified.",
                      description="This label is used to display a human readable name of an image inside the Image / Repo Overview page.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["io.k8s.display-name", "label"],
                      label="io.k8s.display-name",
                      required=True,
                      value_regex=None)


class IoOpenshiftExposeServicesLabelCheck(LabelCheck):

    def __init__(self):
        super(IoOpenshiftExposeServicesLabelCheck, self) \
            .__init__(name="io.openshift.expose-services_label",
                      message="Label 'io.openshift.expose-services' has to be specified.",
                      description="port:service pairs separated with comma, e.g. \"8080:http,8443:https\"",
                      reference_url=["https://github.com/projectatomic/ContainerApplicationGenericLabels",
                                     "https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md#other-labels"],
                      tags=["io.openshift.expose-services", "label"],
                      label="io.openshift.expose-services",
                      required=True,
                      value_regex=None)


class IoOpenShiftTagsLabelCheck(LabelCheck):

    def __init__(self):
        super(IoOpenShiftTagsLabelCheck, self) \
            .__init__(name="io.openshift.tags_label",
                      message="Label 'io.openshift.tags' has to be specified.",
                      description="The primary purpose of this label is to include all relevant search terms for this image.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["io.openshift.tags", "label"],
                      label="io.openshift.tags",
                      required=True,
                      value_regex=None)


class MaintainerLabelCheck(LabelCheck):

    def __init__(self):
        super(MaintainerLabelCheck, self) \
            .__init__(name="maintainer_label",
                      message="Label 'maintainer' has to be specified.",
                      description="The name and email of the maintainer (usually the submitter).",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["maintainer", "label"],
                      label="maintainer",
                      required=True,
                      value_regex=None)


class NameLabelCheck(LabelCheck):

    def __init__(self):
        super(NameLabelCheck, self) \
            .__init__(name="name_label",
                      message="Label 'name' has to be specified.",
                      description="Name of the Image or Container.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["name", "label"],
                      label="name",
                      required=True,
                      value_regex=None)


class ReleaseLabelCheck(LabelCheck):

    def __init__(self):
        super(ReleaseLabelCheck, self) \
            .__init__(name="release_label",
                      message="Label 'release' has to be specified.",
                      description="Release Number for this version.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["release", "label"],
                      label="release",
                      required=True,
                      value_regex=None)


class SummaryLabelCheck(LabelCheck):

    def __init__(self):
        super(SummaryLabelCheck, self) \
            .__init__(name="summary_label",
                      message="Label 'summary' has to be specified.",
                      description="A short description of the image.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["summary", "label"],
                      label="summary",
                      required=True,
                      value_regex=None)


class UrlLabelCheck(LabelCheck):

    def __init__(self):
        super(UrlLabelCheck, self) \
            .__init__(name="url_label",
                      message="Label 'url' has to be specified.",
                      description="A URL where the user can find more information about the image.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["url", "label"],
                      label="url",
                      required=True,
                      value_regex=None)


class UsageLabelCheck(LabelCheck):

    def __init__(self):
        super(UsageLabelCheck, self) \
            .__init__(name="usage_label",
                      message="Label 'usage' has to be specified.",
                      description="A human readable example of container execution.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["usage", "label"],
                      label="usage",
                      required=True,
                      value_regex=None)


class VcsRefLabelCheck(LabelCheck):

    def __init__(self):
        super(VcsRefLabelCheck, self) \
            .__init__(name="vcs-ref_label",
                      message="Label 'vcs-ref' has to be specified.",
                      description="A 'reference' within the version control repository; e.g. a git commit, or a subversion branch.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-ref", "vcs", "label"],
                      label="vcs-ref",
                      required=True,
                      value_regex=None)


class VcsTypeLabelCheck(LabelCheck):

    def __init__(self):
        super(VcsTypeLabelCheck, self) \
            .__init__(name="vcs-type_label",
                      message="Label 'vcs-type' has to be specified.",
                      description="The type of version control used by the container source."
                                  "Generally one of git, hg, svn, bzr, cvs",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-type", "vcs", "label"],
                      label="vcs-type",
                      required=True,
                      value_regex=None)


class VcsUrlLabelCheck(LabelCheck):

    def __init__(self):
        super(VcsUrlLabelCheck, self) \
            .__init__(name="vcs-url_label",
                      message="Label 'vcs-url' has to be specified.",
                      description="URL of the version control repository.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels",
                      tags=["vcs-url", "vcs", "label"],
                      label="vcs-url",
                      required=True,
                      value_regex=None)


class VendorLabelCheck(LabelCheck):

    def __init__(self):
        super(VendorLabelCheck, self) \
            .__init__(name="vendor_label",
                      message="Label 'vendor' has to be specified.",
                      description="Name of the vendor.",
                      reference_url="https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md",
                      tags=["vendor", "label"],
                      label="vendor",
                      required=True)


class VersionLabelCheck(LabelCheck):

    def __init__(self):
        super(VersionLabelCheck, self) \
            .__init__(name="version_label",
                      message="Label 'version' has to be specified.",
                      description="Version of the image.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#LABELS",
                      tags=["version", "label"],
                      label="version",
                      required=True,
                      value_regex=None)
