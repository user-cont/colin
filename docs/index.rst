Colin
=====

Welcome to the Colin documentation !

About
-----

Colin is a tool to check generic rules/best-practices for containers/images/dockerfiles.

Colin is a short cut for **CO**\ ntainer **LIN**\ ter

CLI Usage
---------

This is how you can use colin afterwards:

.. code-block:: bash

   $ colin -h
   Usage: colin [OPTIONS] COMMAND [ARGS]...

     COLIN -- Container Linter

   Options:
     -V, --version  Show the version and exit.
     -h, --help     Show this message and exit.

   Commands:
     check          Check the image/container (default).
     list-checks    Print the checks.
     list-rulesets  List available rulesets.

Let's give it a shot:

.. code-block:: bash

   $ colin check -r redhat rhel7
   LABELS:
   ok :passed:name_label_required
   ok :passed:com_redhat_component_label_required
   ok :passed:summary_label_required
   ok :passed:version_label_required
   nok:failed:usage_label_required
      -> Label 'usage' has to be specified.
      -> A human readable example of container execution.
      -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
   ok :passed:io_k8s_display-name_label_required
   ok :passed:io_openshift_tags_label_required
   ok :passed:architecture_label
   ok :passed:com.redhat.build-host_label
   ok :passed:authoritative-source-url_label
   ok :passed:url_label
   ok :passed:vendor_label
   ok :passed:release_label
   ok :passed:build-date_label
   ok :passed:distribution-scope_label
   ok :passed:vcs-ref_label
   ok :passed:vcs-type_label
   ok :passed:description_label
   ok :passed:io.k8s.description_label
   ok :passed:architecture_label_capital_deprecated
   ok :passed:bzcomponent_deprecated
   ok :passed:name_label_capital_deprecated
   ok :passed:version_label_capital_deprecated
   ok :passed:install_label_capital_deprecated
   ok :passed:uninstall_label_capital_deprecated
   ok :passed:release_label_capital_deprecated
   nok:warning:vcs-url_label
      -> Label 'vcs-url' has to be specified.
      -> URL of the version control repository.
      -> https://github.com/projectatomic/ContainerApplicationGenericLabels
   nok:warning:maintainer_label_required
      -> Label 'maintainer' has to be specified.
      -> The name and email of the maintainer (usually the submitter).
      -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
   nok:warning:io.openshift.expose-services_label
      -> Label 'io.openshift.expose-services' has to be specified.
      -> port:service pairs separated with comma, e.g. "8080:http,8443:https"
      -> ?????
   nok:warning:maintainer_label_required
      -> Label 'maintainer' has to be specified.
      -> The name and email of the maintainer (usually the submitter).
      -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS

Source code
-----------

You may also wish to follow the `GitHub colin repo`_ if you have a GitHub account. This stores the source code and the issue tracker for sharing bugs and feature ideas. The repository should be forked into your personal GitHub account where all work will be done. Any changes should be submitted through the pull request process.

.. _GitHub colin repo: https://github.com/user-cont/colin

Content
=======

.. toctree::
   :maxdepth: 1

   python_api
   list_of_checks

Index and Search
================
* :ref:`genindex`
* :ref:`search`
