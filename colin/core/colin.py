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

import logging

from .check_runner import go_through_checks
from .ruleset.ruleset import Ruleset
from .target import Target

logger = logging.getLogger(__name__)


def run(target, target_type, tags=None, ruleset_name=None, ruleset_file=None,
        ruleset=None, logging_level=logging.WARNING, checks_paths=None, pull=None):
    """
    Runs the sanity checks for the target.

    :param target: str
                    or Image/Container (name of the container/image or Image/Container
                                        instance from conu)
                    or path or file-like object for dockerfile
    :param target_type: string, either image, container or dockerfile
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param ruleset_name: str (e.g. fedora; if None, default would be used)
    :param ruleset_file: fileobj instance holding ruleset configuration
    :param ruleset: dict, content of a ruleset file
    :param logging_level: logging level (default logging.WARNING)
    :param checks_paths: list of str, directories where the checks are present
    :param pull: bool, pull the image from registry
    :return: Results instance
    """
    _set_logging(level=logging_level)
    logger.debug("Checking started.")
    target = Target(target=target,
                    logging_level=logging_level,
                    pull=pull,
                    target_type=target_type)
    checks_to_run = _get_checks(target_type=target.target_type,
                                tags=tags,
                                ruleset_name=ruleset_name,
                                ruleset_file=ruleset_file,
                                ruleset=ruleset,
                                checks_paths=checks_paths
    )
    result = go_through_checks(target=target,
                               checks=checks_to_run)
    return result


def get_checks(target_type=None, tags=None, ruleset_name=None,
               ruleset_file=None, ruleset=None, logging_level=logging.WARNING, checks_paths=None):
    """
    Get the sanity checks for the target.

    :param target_type: TargetType enum
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param ruleset_name: str (e.g. fedora; if None, default would be used)
    :param ruleset_file: fileobj instance holding ruleset configuration
    :param ruleset: dict, content of a ruleset file
    :param logging_level: logging level (default logging.WARNING)
    :param checks_paths: list of str, directories where the checks are present
    :return: list of check instances
    """
    _set_logging(level=logging_level)
    logger.debug("Finding checks started.")
    return _get_checks(
        target_type=target_type,
        tags=tags,
        ruleset_name=ruleset_name,
        ruleset_file=ruleset_file,
        ruleset=ruleset,
        checks_paths=checks_paths
    )


def _get_checks(target_type, tags=None,
                ruleset_name=None, ruleset_file=None, ruleset=None, checks_paths=None):
    ruleset = Ruleset(ruleset_name=ruleset_name,
                      ruleset_file=ruleset_file,
                      ruleset=ruleset,
                      checks_paths=checks_paths)
    return ruleset.get_checks(tags=tags, target_type=target_type)


def _set_logging(
        logger_name="colin",
        level=logging.INFO,
        handler_class=logging.StreamHandler,
        handler_kwargs=None,
        format='%(asctime)s.%(msecs).03d %(filename)-17s %(levelname)-6s %(message)s',
        date_format='%H:%M:%S'):
    """
    Set personal logger for this library.

    :param logger_name: str, name of the logger
    :param level: int, see logging.{DEBUG,INFO,ERROR,...}: level of logger and handler
    :param handler_class: logging.Handler instance, default is StreamHandler (/dev/stderr)
    :param handler_kwargs: dict, keyword arguments to handler's constructor
    :param format: str, formatting style
    :param date_format: str, date style in the logs
    """
    if level != logging.NOTSET:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        handler_kwargs = handler_kwargs or {}
        handler = handler_class(**handler_kwargs)
        handler.setLevel(level)

        formatter = logging.Formatter(format, date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
