List of all checks
==================

Colin checks several labels and the best practises (e.g. helpfile check).

Since there can be many platforms/setups with different requirements,
we can define so-called rulesets, that defines:

- subset of checks to be used,
- metadata changes/extensions.

*Ruleset* is only a json/yaml file with following structure:

.. code-block:: json

    {
      "version": "1",
      "name": "Ruleset for Fedora containers/images/dockerfiles.",
      "description": "This set of checks is defined by the Fedora Container Guidelines.",
      "contact_email": "user-cont-team@redhat.com",
      "checks": [
        {
          "name": "architecture_label"
        },
        {
          "name": "build-date_label"
        },
        :
        :
      ]
    }


Rulesets in the *standard* location can be shown with `colin list-rulesets`
and we can use them by name in other commands. (e.g. `colin check -r fedora`).

.. code-block:: bash

    $ colin list-rulesets
    default (./rulesets/default.json)
    fedora  (./rulesets/fedora.json)
    fedora  (/home/flachman/.local/share/colin/rulesets/fedora.json)
    default (/home/flachman/.local/share/colin/rulesets/default.json)
    fedora  (/usr/local/share/colin/rulesets/fedora.json)
    default (/usr/local/share/colin/rulesets/default.json)


Colin can use ruleset-files in the following directories:

- `./rulesets/` (subdirectory of the current working directory)
- `~/local/share/colin/rulesets/` (user installation)
- `/usr/local/share/colin/rulesets/` (system-wide installation)

We can easily list the checks with the following command:

.. code-block:: bash

    $ colin list-checks -f rulesets/fedora.json
    architecture_label
       -> Label 'architecture' has to be specified.
       -> Architecture the software in the image should target. (Optional: if omitted, it will be built for all supported Fedora Architectures)
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, architecture

    build-date_label
       -> Label 'build-date' has to be specified.
       -> Date/Time image was built as RFC 3339 date-time.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, build-date

    description_label
       -> Label 'description' has to be specified.
       -> Detailed description of the image.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, description

    distribution-scope_label
       -> Label 'distribution-scope' has to be specified.
       -> Scope of intended distribution of the image. (private/authoritative-source-only/restricted/public)
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, distribution-scope

    help_label
       -> Label 'help' has to be specified.
       -> A runnable command which results in display of Help information.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, help

    io.k8s.description_label
       -> Label 'io.k8s.description' has to be specified.
       -> Description of the container displayed in Kubernetes
       -> ['https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md', 'https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md#other-labels']
       -> label, io.k8s.description, description

    url_label
       -> Label 'url' has to be specified.
       -> A URL where the user can find more information about the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, url

    vcs-ref_label
       -> Label 'vcs-ref' has to be specified.
       -> A 'reference' within the version control repository; e.g. a git commit, or a subversion branch.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, vcs-ref, vcs

    vcs-type_label
       -> Label 'vcs-type' has to be specified.
       -> The type of version control used by the container source. Generally one of git, hg, svn, bzr, cvs
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, vcs-type, vcs

    vcs-url_label
       -> Label 'vcs-url' has to be specified.
       -> URL of the version control repository.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, vcs-url, vcs

    com.redhat.component_label
       -> Label 'com.redhat.component' has to be specified.
       -> The Bugzilla component name where bugs against this container should be reported by users.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, com.redhat.component, required

    maintainer_label
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, maintainer, required

    name_label
       -> Label 'name' has to be specified.
       -> Name of the Image or Container.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, name, required

    release_label
       -> Label 'release' has to be specified.
       -> Release Number for this version.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, release, required

    summary_label
       -> Label 'summary' has to be specified.
       -> A short description of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, summary, required

    version_label
       -> Label 'version' has to be specified.
       -> Version of the image.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, version, required

    from_tag_not_latest
       -> In FROM, tag has to be specified and not 'latest'.
       -> Using the 'latest' tag may cause unpredictable builds.It is recommended that a specific tag is used in the FROM.
       -> https://fedoraproject.org/wiki/Container:Guidelines#FROM
       -> dockerfile, from, baseimage, latest, required

    maintainer_deprecated
       -> Dockerfile instruction `MAINTAINER` is deprecated.
       -> Replace with label 'maintainer'.
       -> https://docs.docker.com/engine/reference/builder/#maintainer-deprecated
       -> dockerfile, maintainer, deprecated, required

    description_or_io.k8s.description_label
       -> Label 'description' or 'io.k8s.description' has to be specified.
       -> Detailed description of the image.
       -> https://github.com/projectatomic/ContainerApplicationGenericLabels/blob/master/vendor/redhat/labels.md
       -> label, description, required

    help_file_or_readme
       -> The 'helpfile' has to be provided.
       -> Just like traditional packages, containers need some 'man page' information about how they are to be used, configured, and integrated into a larger stack.
       -> https://fedoraproject.org/wiki/Container:Guidelines#Help_File
       -> filesystem, helpfile, man, required

    run_or_usage_label
       -> Label 'usage' has to be specified.
       -> A human readable example of container execution.
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
       -> label, usage, required
