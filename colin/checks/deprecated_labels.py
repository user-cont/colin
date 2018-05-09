from colin.core.checks.labels import DeprecatedLabelCheck


class ArchitectureLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(ArchitectureLabelCapitalDeprecatedCheck, self). \
            __init__(name="architecture_label_capital_deprecated",
                     message="Label 'Architecture' is deprecated.",
                     description="Replace with 'architecture'.",
                     reference_url="?????",
                     tags=["architecture", "label", "capital", "deprecated"],
                     old_label="Architecture",
                     new_label="architecture")


class BZComponentDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(BZComponentDeprecatedCheck, self) \
            .__init__(name="bzcomponent_deprecated",
                      message="Label 'BZComponent' is deprecated.",
                      description="Replace with 'com.redhat.component'.",
                      reference_url="?????",
                      tags=["com.redhat.component", "bzcomponent", "label", "deprecated"],
                      old_label="BZComponent",
                      new_label="com.redhat.component")


class InstallLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(InstallLabelCapitalDeprecatedCheck, self) \
            .__init__(name="install_label_capital_deprecated",
                      message="Label 'INSTALL' is deprecated.",
                      description="Replace with 'install'.",
                      reference_url="?????",
                      tags=["install", "label", "capital", "deprecated"],
                      old_label="INSTALL",
                      new_label="install")


class NameLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(NameLabelCapitalDeprecatedCheck, self) \
            .__init__(name="name_label_capital_deprecated",
                      message="Label 'Name' is deprecated.",
                      description="Replace with 'name'.",
                      reference_url="?????",
                      tags=["name", "label", "capital", "deprecated"],
                      old_label="Name",
                      new_label="name")


class ReleaseLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(ReleaseLabelCapitalDeprecatedCheck, self) \
            .__init__(name="release_label_capital_deprecated",
                      message="Label 'Release' is deprecated.",
                      description="Replace with 'release'.",
                      reference_url="?????",
                      tags=["release", "label", "capital", "deprecated"],
                      old_label="Release",
                      new_label="release")


class UninstallLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(UninstallLabelCapitalDeprecatedCheck, self) \
            .__init__(name="uninstall_label_capital_deprecated",
                      message="Label 'UNINSTALL' is deprecated.",
                      description="Replace with 'uninstall'.",
                      reference_url="?????",
                      tags=["uninstall", "label", "capital", "deprecated"],
                      old_label="UNINSTALL",
                      new_label="uninstall")


class VersionLabelCapitalDeprecatedCheck(DeprecatedLabelCheck):

    def __init__(self):
        super(VersionLabelCapitalDeprecatedCheck, self) \
            .__init__(name="version_label_capital_deprecated",
                      message="Label 'Version' is deprecated.",
                      description="Replace with 'version'.",
                      reference_url="?????",
                      tags=["version", "label", "capital", "deprecated"],
                      old_label="Version",
                      new_label="version")
