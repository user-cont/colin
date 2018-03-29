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
from .config.config import Config
from .target import Target

logger = logging.getLogger(__name__)


def run(name_of_target, group=None, severity=None, tags=None, config_name=None, config_file=None,
        logging_level=logging.WARNING):
    """
    Runs the sanity checks for the target.

    :param name_of_target: str (name of the container or image, dockerfile will be added in the future)
    :param group: str (name of the folder with group of checks, if None, all of them will be checked.)
    :param severity: str (if not None, only those checks will be run -- optional x required x warn ...)
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param config_name: str (e.g. fedora; if None, default would be used)
    :param config_file: str (path)
    :param logging_level: logging level (default logging.WARNING)
    :return: Results instance
    """
    _set_logging(level=logging_level)
    logger.debug("Checking started.")
    target = Target(name=name_of_target,
                    logging_level=logging_level)
    checks_to_run = _get_checks(target=target,
                                group=group,
                                severity=severity,
                                tags=tags,
                                config_name=config_name,
                                config_file=config_file)
    result = go_through_checks(target=target,
                               checks=checks_to_run)
    return result


def get_checks(name_of_target, group=None, severity=None, tags=None, config_name=None, config_file=None,
               logging_level=logging.WARNING):
    """
    Get the sanity checks for the target.

    :param name_of_target: str (name of the container or image, dockerfile will be added in the future)
    :param group: str (name of the folder with group of checks, if None, all of them will be checked.)
    :param severity: str (if not None, only those checks will be run -- optional x required x warn ...)
    :param tags: list of str (if not None, the checks will be filtered by tags.)
    :param config_name: str (e.g. fedora; if None, default would be used)
    :param config_file: str (path)
    :param logging_level: logging level (default logging.WARNING)
    :return: list of groups of checks
    """
    _set_logging(level=logging_level)
    logger.debug("Finding checks started.")
    target = Target(name=name_of_target,
                    logging_level=logging_level)
    return _get_checks(target=target,
                       group=group,
                       severity=severity,
                       tags=tags,
                       config_name=config_name,
                       config_file=config_file)


def _get_checks(target, group=None, severity=None, tags=None, config_name=None, config_file=None):
    logger.debug("Checking started.")
    config = Config(config_name=config_name,
                    config_file=config_file)
    return config.get_checks(group=group,
                             severity=severity,
                             tags=tags,
                             target_type=target.target_type)


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
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler_kwargs = handler_kwargs or {}
    handler = handler_class(**handler_kwargs)
    handler.setLevel(level)

    formatter = logging.Formatter(format, date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
