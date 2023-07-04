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
import time

import pytest

from colin.core.exceptions import ColinException
from colin.utils.cmd_tools import exit_after
from colin.utils.cmd_tools import retry


@exit_after(1)
def fast_fce():
    pass


@exit_after(1)
def slow_fce():
    time.sleep(2)


@exit_after(1)
def bad_fce():
    raise ColinException("Error")


def test_timeout_fast_fce():
    fast_fce()


def test_timeout_slow_fce():
    with pytest.raises(TimeoutError):
        slow_fce()


def test_timeout_bad_fce():
    with pytest.raises(ColinException):
        bad_fce()


def test_timeout_dirrect():
    with pytest.raises(TimeoutError):
        exit_after(1)(time.sleep)(2)


COUNTER = 0


def raise_exception():
    global COUNTER
    COUNTER += 1

    raise Exception("I am bad function")


def test_no_retry_for_success():
    global COUNTER
    COUNTER = 0

    @retry(5, 0)
    def always_success():
        global COUNTER
        COUNTER = COUNTER + 1

        return 42

    assert always_success() == 42
    assert COUNTER == 1


def test_retry_with_exception():
    global COUNTER
    COUNTER = 0

    @retry(5, 0)
    def always_raise_exception():
        raise_exception()

    with pytest.raises(Exception) as ex:
        always_raise_exception()

    assert str(ex.value) == "I am bad function"
    assert COUNTER == 5


def test_wrong_parameter():
    with pytest.raises(ValueError) as ex:
        retry(-1, 1)
    assert str(ex.value) == "retry_count have to be positive"

    with pytest.raises(ValueError) as ex:
        retry(0, 1)
    assert str(ex.value) == "retry_count have to be positive"

    @retry(5, -1)
    def fail_negative_sleep():
        raise_exception()

    with pytest.raises(ValueError) as ex:
        fail_negative_sleep()
    assert str(ex.value) == "sleep length must be non-negative"


def test_retry_with_sleep():
    global COUNTER
    COUNTER = 0

    @retry(4, 0.5)
    def fail_and_sleep():
        raise_exception()

    time_start = time.time()
    with pytest.raises(Exception) as ex:
        fail_and_sleep()
    time_end = time.time()

    assert str(ex.value) == "I am bad function"
    assert COUNTER == 4

    # there are 3 sleeps between 4 delays
    assert time_end - time_start >= 1.5
    # there were not 4 sleeps
    assert time_end - time_start < 4


def test_recover_after_few_failures():
    global COUNTER
    COUNTER = 0

    @retry(5, 0)
    def sleep_like_a_baby():
        global COUNTER
        if COUNTER < 3:
            COUNTER += 1
            raise Exception("sleeping")
        return []

    assert sleep_like_a_baby() == []
    assert COUNTER == 3
