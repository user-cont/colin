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

    $ colin --help
    Usage: colin [OPTIONS] COMMAND [ARGS]...

      COLIN -- Container Linter

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      check          Check the image/dockerfile (default).
      info           Show info about colin and its dependencies.
      list-checks    Print the checks.
      list-rulesets  List available rulesets.

Let's give it a shot:

.. code-block:: bash

    $ colin -f ./rulesets/fedora.json registry.fedoraproject.org/f29/cockpit
    PASS:Label 'architecture' has to be specified.
    PASS:Label 'build-date' has to be specified.
    FAIL:Label 'description' has to be specified.
    PASS:Label 'distribution-scope' has to be specified.
    FAIL:Label 'help' has to be specified.
    FAIL:Label 'io.k8s.description' has to be specified.
    FAIL:Label 'url' has to be specified.
    PASS:Label 'vcs-ref' has to be specified.
    PASS:Label 'vcs-type' has to be specified.
    FAIL:Label 'vcs-url' has to be specified.
    PASS:Label 'com.redhat.component' has to be specified.
    FAIL:Label 'maintainer' has to be specified.
    PASS:Label 'name' has to be specified.
    PASS:Label 'release' has to be specified.
    FAIL:Label 'summary' has to be specified.
    PASS:Label 'version' has to be specified.
    FAIL:The 'helpfile' has to be provided.
    PASS:Label 'usage' has to be specified.

    PASS:10 FAIL:8


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
