Usage of colin in Python code
==========================

The colin CLI is only a wrapper around the colin's python library.

All functionality can be accessed directly from the python code:

Module colin.core.colin
=======================

Functions
---------

`get_checks(target_type=None, tags=None, ruleset_name=None, ruleset_file=None, ruleset=None, logging_level=30, checks_paths=None, skips=None)`
:   Get the sanity checks for the target.

    :param skips: name of checks to skip
    :param target_type: TargetType enum
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param ruleset_name: str (e.g. fedora; if None, default would be used)
    :param ruleset_file: fileobj instance holding ruleset configuration
    :param ruleset: dict, content of a ruleset file
    :param logging_level: logging level (default logging.WARNING)
    :param checks_paths: list of str, directories where the checks are present
    :return: list of check instances

`run(target, target_type, tags=None, ruleset_name=None, ruleset_file=None, ruleset=None, logging_level=30, checks_paths=None, pull=None, insecure=False, skips=None, timeout=None)`
:   Runs the sanity checks for the target.

    :param timeout: timeout per-check (in seconds)
    :param skips: name of checks to skip
    :param target: str (image name, ostree or dockertar)
                    or ImageTarget
                    or path/file-like object for dockerfile
    :param target_type: string, either image, dockerfile, dockertar
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param ruleset_name: str (e.g. fedora; if None, default would be used)
    :param ruleset_file: fileobj instance holding ruleset configuration
    :param ruleset: dict, content of a ruleset file
    :param logging_level: logging level (default logging.WARNING)
    :param checks_paths: list of str, directories where the checks are present
    :param pull: bool, pull the image from registry
    :param insecure: bool, pull from an insecure registry (HTTP/invalid TLS)
    :return: Results instance
