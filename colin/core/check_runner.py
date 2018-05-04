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

from six import iteritems

from ..checks.result import CheckResults, FailedCheckResult
from ..utils.caching_iterable import CachingIterable

logger = logging.getLogger(__name__)


def go_through_checks(target, checks):
    logger.debug("Going through checks.")
    results = _group_generator(target=target,
                               checks=checks)
    return CheckResults(results=results)


def _result_generator(target, checks):
    for check in checks:
        logger.debug("Checking {}".format(check.name))
        try:
            yield check.check(target)
        except Exception as ex:
            logger.warning("There occurred an error when executing the check. ({})".format(ex))
            yield FailedCheckResult(check, ex)


def _group_generator(target, checks):
    for (group, group_checks) in iteritems(checks):
        logger.debug("Checking group: {}".format(group))
        yield group, CachingIterable(_result_generator(target=target,
                                                       checks=group_checks))
