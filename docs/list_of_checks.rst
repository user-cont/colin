List of all checks
==================

Colin checks several labels and the best practises (e.g. helpfile check) in Fedora and Red Hat images.

Fedora
------

Below is a list of the labels which are checked in the Fedora images.

.. code-block:: bash

    $ colin list-checks -r fedora
    LABELS:
    maintainer_label_required
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['maintainer', 'label', 'required']
       -> required

    name_label_required
       -> Label 'name' has to be specified.
       -> Name of the Image or Container.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['name', 'label', 'required']
       -> required

    com_redhat_component_label_required
       -> Label 'com.redhat.component' has to be specified.
       -> The Bugzilla component name where bugs against this container should be reported by users.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['com.redhat.component', 'label', 'required']
       -> required

    summary_label_required
       -> Label 'summary' has to be specified.
       -> A short description of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['summary', 'label', 'required']
       -> required

    version_label_required
       -> Label 'version' has to be specified.
       -> Version of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['version', 'label', 'required']
       -> required

    usage_label_required
       -> Label 'usage' has to be specified.
       -> A human readable example of container execution.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['usage', 'label', 'required']
       -> required

    release_label
       -> Label 'release' has to be specified.
       -> Release Number for this version.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['release', 'label', 'required']
       -> required

    architecture_label
       -> Label 'architecture' has to be specified.
       -> Architecture the software in the image should target. (Optional: if omitted, it will be built for all supported Fedora Architectures)
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['architecture', 'label', 'required', 'optional']
       -> required

    url_label
       -> Label 'url' has to be specified.
       -> A URL where the user can find more information about the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['url', 'label', 'required']
       -> optional

    help_label
       -> Label 'help' has to be specified.
       -> A runnable command which results in display of Help information.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['help', 'label', 'required', 'optional']
       -> optional

    build-date_label
       -> Label 'build-date' has to be specified.
       -> Date/Time image was built as RFC 3339 date-time.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['build-date', 'label', 'required']
       -> optional

    distribution-scope_label
       -> Label 'distribution-scope' has to be specified.
       -> Scope of intended distribution of the image. (private/authoritative-source-only/restricted/public)
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['distribution-scope', 'label', 'required']
       -> optional

    vcs-ref_label
       -> Label 'vcs-ref' has to be specified.
       -> A 'reference' within the version control repository; e.g. a git commit, or a subversion branch.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-ref', 'vcs', 'label', 'required']
       -> optional

    vcs-type_label
       -> Label 'vcs-type' has to be specified.
       -> The type of version control used by the container source.Generally one of git, hg, svn, bzr, cvs
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-type', 'vcs', 'label', 'required']
       -> optional

    description_label
       -> Label 'description' has to be specified.
       -> Detailed description of the image.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['description', 'label', 'required']
       -> optional

    io.k8s.description_label
       -> Label 'io.k8s.description' has to be specified.
       -> Description of the container displayed in Kubernetes
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> ['io.k8s.description', 'description', 'label', 'required']
       -> optional

    vcs-url_label
       -> Label 'vcs-url' has to be specified.
       -> URL of the version control repository.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-url', 'vcs', 'label', 'optional']
       -> optional

    maintainer_label_required
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['maintainer', 'label', 'required']
       -> optional

    BEST_PRACTICES:
    help_file_or_readme_required
       -> The 'helpfile' has to be provided.
       -> Just like traditional packages, containers need some 'man page' information about how they are to be used, configured, and integrated into a larger stack.
       -> https://fedoraproject.org/wiki/Container:Guidelines#Help_File
       -> ['filesystem', 'helpfile', 'man']
       -> required

    cmd_or_entrypoint
       -> Cmd or Entrypoint has to be specified
       ->
       -> ?????
       -> ['cmd', 'entrypoint', 'required']
       -> required

    no_root
       -> Service should not run as root by default.
       ->
       -> ?????
       -> ['root', 'user']
       -> required

Red Hat images
--------------

Below is a list of the labels which are checked in the Red Hat images.

.. code-block:: bash

    $ colin list-checks -r redhat
    LABELS:
    name_label_required
       -> Label 'name' has to be specified.
       -> Name of the Image or Container.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['name', 'label', 'required']
       -> required

    com_redhat_component_label_required
       -> Label 'com.redhat.component' has to be specified.
       -> The Bugzilla component name where bugs against this container should be reported by users.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['com.redhat.component', 'label', 'required']
       -> required

    summary_label_required
       -> Label 'summary' has to be specified.
       -> A short description of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['summary', 'label', 'required']
       -> required

    version_label_required
       -> Label 'version' has to be specified.
       -> Version of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['version', 'label', 'required']
       -> required

    usage_label_required
       -> Label 'usage' has to be specified.
       -> A human readable example of container execution.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['usage', 'label', 'required']
       -> required

    io_k8s_display-name_label_required
       -> Label 'io.k8s.display-name' has to be specified.
       -> This label is used to display a human readable name of an image inside the Image / Repo Overview page.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['io.k8s.display-name', 'label', 'required']
       -> required

    architecture_label
       -> Label 'architecture' has to be specified.
       -> Architecture the software in the image should target. (Optional: if omitted, it will be built for all supported Fedora Architectures)
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['architecture', 'label', 'required', 'optional']
       -> required

    com.redhat.build-host_label
       -> Label 'com.redhat.build-host' has to be specified.
       -> The build host used to create an image for internal use and auditability, similar to the use in RPM.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['com.redhat.build-host', 'build-host', 'label', 'required']
       -> required

    authoritative-source-url_label
       -> Label 'authoritative-source-url' has to be specified.
       -> The authoritative registry in which the image is published.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['authoritative-source-url', 'label', 'required']
       -> required

    url_label
       -> Label 'url' has to be specified.
       -> A URL where the user can find more information about the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['url', 'label', 'required']
       -> required

    vendor_label
       -> Label 'vendor' has to be specified.
       -> 'Red Hat, Inc.'
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> ['vendor', 'label', 'required']
       -> required

    release_label
       -> Label 'release' has to be specified.
       -> Release Number for this version.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['release', 'label', 'required']
       -> required

    build-date_label
       -> Label 'build-date' has to be specified.
       -> Date/Time image was built as RFC 3339 date-time.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['build-date', 'label', 'required']
       -> required

    distribution-scope_label
       -> Label 'distribution-scope' has to be specified.
       -> Scope of intended distribution of the image. (private/authoritative-source-only/restricted/public)
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['distribution-scope', 'label', 'required']
       -> required

    vcs-ref_label
       -> Label 'vcs-ref' has to be specified.
       -> A 'reference' within the version control repository; e.g. a git commit, or a subversion branch.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-ref', 'vcs', 'label', 'required']
       -> required

    vcs-type_label
       -> Label 'vcs-type' has to be specified.
       -> The type of version control used by the container source.Generally one of git, hg, svn, bzr, cvs
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-type', 'vcs', 'label', 'required']
       -> required

    description_label
       -> Label 'description' has to be specified.
       -> Detailed description of the image.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['description', 'label', 'required']
       -> required

    io.k8s.description_label
       -> Label 'io.k8s.description' has to be specified.
       -> Description of the container displayed in Kubernetes
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> ['io.k8s.description', 'description', 'label', 'required']
       -> required

    architecture_label_capital_deprecated
       -> Label 'Architecture' is deprecated.
       -> Replace with 'architecture'.
       -> ?????
       -> ['architecture', 'label', 'capital', 'deprecated']
       -> required

    bzcomponent_deprecated
       -> Label 'BZComponent' is deprecated.
       -> Replace with 'com.redhat.component'.
       -> ?????
       -> ['com.redhat.component', 'bzcomponent', 'label', 'deprecated']
       -> required

    name_label_capital_deprecated
       -> Label 'Name' is deprecated.
       -> Replace with 'name'.
       -> ?????
       -> ['name', 'label', 'capital', 'deprecated']
       -> required

    version_label_capital_deprecated
       -> Label 'Version' is deprecated.
       -> Replace with 'version'.
       -> ?????
       -> ['version', 'label', 'capital', 'deprecated']
       -> required

    install_label_capital_deprecated
       -> Label 'INSTALL' is deprecated.
       -> Replace with 'install'.
       -> ?????
       -> ['install', 'label', 'capital', 'deprecated']
       -> required

    uninstall_label_capital_deprecated
       -> Label 'UNINSTALL' is deprecated.
       -> Replace with 'uninstall'.
       -> ?????
       -> ['uninstall', 'label', 'capital', 'deprecated']
       -> required

    release_label_capital_deprecated
       -> Label 'Release' is deprecated.
       -> Replace with 'release'.
       -> ?????
       -> ['release', 'label', 'capital', 'deprecated']
       -> required

    vcs-url_label
       -> Label 'vcs-url' has to be specified.
       -> URL of the version control repository.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels
       -> ['vcs-url', 'vcs', 'label', 'optional']
       -> optional

    maintainer_label_required
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['maintainer', 'label', 'required']
       -> optional

    maintainer_label_required
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> ['maintainer', 'label', 'required']
       -> optional

    BEST_PRACTICES:
    help_file_required
       -> The 'helpfile' has to be provided.
       -> Just like traditional packages, containers need some 'man page' information about how they are to be used, configured, and integrated into a larger stack.
       -> https://fedoraproject.org/wiki/Container:Guidelines#Help_File
       -> ['filesystem', 'helpfile', 'man']
       -> required

    cmd_or_entrypoint
       -> Cmd or Entrypoint has to be specified
       ->
       -> ?????
       -> ['cmd', 'entrypoint', 'required']
       -> required

    no_root
       -> Service should not run as root by default.
       ->
       -> ?????
       -> ['root', 'user']
       -> required
