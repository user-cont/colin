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
import functools
import logging
import subprocess
import threading
import time

try:
    import thread
except ImportError:
    import _thread as thread  # type: ignore

logger = logging.getLogger(__name__)


def get_version_of_the_python_package(module):
    """
    Return the str containing the name version and package location.

    :param module: module to show info about
    :return: str 'name version path'
    """
    return "{} {} {}".format(
        getattr(module, "__name__", None),
        getattr(module, "__version__", None),
        getattr(module, "__path__", [None])[0],
    )


def get_version_msg_from_the_cmd(
    package_name, cmd=None, use_rpm=None, max_lines_of_the_output=None
):
    """
    Get str with the version (or string representation of the error).

    :param package_name: str
    :param cmd: str or [str] (defaults to [package_name, "--version"])
    :param use_rpm: True/False/None (whether to use rpm -q for getting a version)
    :param max_lines_of_the_output: use first n lines of the output
    :return: str
    """
    if use_rpm is None:
        use_rpm = is_rpm_installed()
    if use_rpm:
        rpm_version = get_rpm_version(package_name=package_name)
        if rpm_version:
            return f"{rpm_version} (rpm)"

    try:
        cmd = cmd or [package_name, "--version"]
        version_result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if version_result.returncode == 0:
            version_output = version_result.stdout.decode().rstrip()
            if max_lines_of_the_output:
                version_output = " ".join(
                    version_output.split("\n")[:max_lines_of_the_output]
                )
            return version_output

        else:
            return f"{package_name}: cannot get version with {cmd}"
    except FileNotFoundError:
        return f"{package_name} not accessible!"


def get_rpm_version(package_name):
    """Get a version of the package with 'rpm -q' command."""
    version_result = subprocess.run(
        ["rpm", "-q", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if version_result.returncode == 0:
        return version_result.stdout.decode().rstrip()
    else:
        return None


def is_rpm_installed():
    """Tests if the rpm command is present."""
    try:
        version_result = subprocess.run(
            ["rpm", "--usage"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        rpm_installed = not version_result.returncode
    except FileNotFoundError:
        rpm_installed = False
    return rpm_installed


def exit_after(s):
    """
    Use as decorator to exit process if
    function takes longer than s seconds.

    Direct call is available via exit_after(TIMEOUT_IN_S)(fce)(args).

    Inspired by https://stackoverflow.com/a/31667005
    """

    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, thread.interrupt_main)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            except KeyboardInterrupt:
                raise TimeoutError(
                    f"Function '{fn.__name__}' hit the timeout ({s}s)."
                )
            finally:
                timer.cancel()
            return result

        return inner

    return outer


def retry(retry_count=5, delay=2):
    """
    Use as decorator to retry functions few times with delays

    Exception will be raised if last call fails

    :param retry_count: int could of retries in case of failures. It must be
                        a positive number
    :param delay: int delay between retries
    """
    if retry_count <= 0:
        raise ValueError("retry_count have to be positive")

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for i in range(retry_count, 0, -1):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    if i <= 1:
                        raise
                time.sleep(delay)

        return wrapper

    return decorator
