Colin
=====

Welcome to the Colin documentation !

About
-----

Colin is a tool to check generic rules/best-practices for containers/images/dockerfiles.

CLI Usage
---------

This is how you can use colin afterwards:

.. code-block:: bash

    $ colin -h
    Usage: colin [OPTIONS] TARGET

    Options:
      -c, --config [redhat|fedora]  Select a predefined configuration.
      --debug                       Enable debugging mode (debugging logs, full tracebacks).
      -f, --config-file FILENAME    Path to a file to use for validation (by
                                    default they are placed in /usr/share/colin).
      --json FILENAME               File to save the output as json to.
      -s, --stat                    Print statistics instead of full results.
      -v, --verbose                 Verbose mode.
      -h, --help                    Show this message and exit.


Let's give it a shot:

.. code-block:: bash

    $ colin -f ./config/redhat.json rhel7
    LABELS:
    nok:failed:maintainer_label_required
       -> Label 'maintainer' has to be specified.
       -> The name and email of the maintainer (usually the submitter).
       -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
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

Source code
-----------

You may also wish to follow the `GitHub colin repo`_ if you have a GitHub account. This stores the source code and the issue tracker for sharing bugs and feature ideas. The repository should be forked into your personal GitHub account where all work will be done. Any changes should be submitted through the pull request process.

.. _GitHub colin repo: https://github.com/user-cont/colin

Content
=======

.. toctree::
   :maxdepth: 1

   python_api
   check_list

Index and Search
================
* :ref:`genindex`
* :ref:`search`
