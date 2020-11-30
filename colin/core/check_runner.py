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
import traceback

from .constant import CHECK_TIMEOUT
from .result import CheckResults, FailedCheckResult
from ..utils.cmd_tools import exit_after

logger = logging.getLogger(__name__)


def go_through_checks(target, checks, timeout=None):
    logger.debug("Going through checks.")
    results = _result_generator(target=target, checks=checks, timeout=timeout)
    return CheckResults(results=results)


def _result_generator(target, checks, timeout=None):
    try:
        for check in checks:
            logger.debug("Checking %s", check.name)
            try:
                _timeout = timeout or check.timeout or CHECK_TIMEOUT
                logger.debug("Check timeout: %s", _timeout)
                yield exit_after(_timeout)(check.check)(target)
            except TimeoutError as ex:
                logger.warning("The check hit the timeout: %s", _timeout)
                yield FailedCheckResult(check, logs=[str(ex)])
            except Exception as ex:
                tb = traceback.format_exc()
                logger.warning("There was an error while performing check: %s", tb)
                yield FailedCheckResult(check, logs=[str(ex)])
    finally:
        target.clean_up()
