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
import os
import sys

import click
import six

from colin.utils.cmd_tools import get_version_msg_from_the_cmd, is_rpm_installed
from .default_group import DefaultGroup
from ..core.checks.abstract_check import AbstractCheck
from ..core.colin import get_checks, run
from ..core.constant import COLIN_CHECKS_PATH
from ..core.exceptions import ColinException
from ..core.ruleset.ruleset import get_rulesets, get_checks_paths
from ..version import __version__

logger = logging.getLogger("colin.cli")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], auto_envvar_prefix="COLIN")


@click.group(cls=DefaultGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "--version", "-V")
def cli():
    """
    COLIN -- Container Linter
    """
    pass


@click.command(name="check", context_settings=CONTEXT_SETTINGS)
@click.argument("TARGET", type=click.STRING)
@click.option("--parent-target", type=click.STRING, help="Parent target")
@click.option(
    "--ruleset",
    "-r",
    type=click.STRING,
    envvar="COLIN_RULESET",
    help="Select a predefined ruleset (e.g. fedora).",
)
@click.option(
    "--ruleset-file",
    "-f",
    type=click.File(mode="r"),
    help="Path to a file to use for validation "
    "(by default they are placed in /usr/share/colin/rulesets).",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Enable debugging mode (debugging logs, full tracebacks).",
)
@click.option(
    "--json", type=click.File(mode="w"), help="File to save the output as json to."
)
@click.option(
    "--xunit", type=click.File(mode="w"), help="File to save the output as xunit to."
)
@click.option("--stat", is_flag=True, help="Print statistics instead of full results.")
@click.option(
    "--skip",
    "-s",
    multiple=True,
    type=click.STRING,
    help="Name of the check to skip. (this option is repeatable)",
)
@click.option(
    "--tag", "-t", multiple=True, type=click.STRING, help="Filter checks with the tag."
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode.")
@click.option(
    "checks_paths",
    "--checks-path",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    multiple=True,
    envvar=COLIN_CHECKS_PATH,
    help=f"Path to directory containing checks (default {get_checks_paths()}).",
)
@click.option("--pull", is_flag=True, help="Pull the image from registry.")
@click.option(
    "--target-type",
    type=click.STRING,
    default="image",
    help="Type of selected target (one of image, dockerfile, "
    "oci). For oci, please specify image name and path like this: oci:path:image",
)
@click.option(
    "--timeout", type=click.INT, help="Timeout for each check in seconds. (default=600)"
)
@click.option(
    "--insecure",
    is_flag=True,
    default=False,
    help="Pull from an insecure registry (HTTP or invalid TLS).",
)
def check(
    target,
    parent_target,
    ruleset,
    ruleset_file,
    debug,
    json,
    xunit,
    stat,
    skip,
    tag,
    verbose,
    checks_paths,
    target_type,
    timeout,
    pull,
    insecure,
):
    """
    Check the image/dockerfile (default).
    """
    if ruleset and ruleset_file:
        raise click.BadOptionUsage(
            "Options '--ruleset' and '--file-ruleset' cannot be used together."
        )

    if json and not os.path.isdir(os.path.dirname(os.path.realpath(json.name))):
        raise click.BadOptionUsage(
            "Parent directory for the json output file does not exist."
        )

    if xunit and not os.path.isdir(os.path.dirname(os.path.realpath(xunit.name))):
        raise click.BadOptionUsage(
            "Parent directory for the xunit output file does not exist."
        )

    try:
        if not debug:
            logging.basicConfig(stream=six.StringIO())

        log_level = _get_log_level(debug=debug, verbose=verbose)
        results = run(
            target=target,
            parent_target=parent_target,
            ruleset_name=ruleset,
            ruleset_file=ruleset_file,
            logging_level=log_level,
            tags=tag,
            pull=pull,
            checks_paths=checks_paths,
            target_type=target_type,
            timeout=timeout,
            insecure=insecure,
            skips=skip,
        )
        _print_results(results=results, stat=stat, verbose=verbose)

        if json:
            results.save_json_to_file(file=json)

        if xunit:
            results.save_xunit_to_file(file=xunit)

        if not results.ok:
            sys.exit(1)
        elif results.fail:
            sys.exit(3)

    except ColinException as ex:
        logger.error("An error occurred: %r", ex)
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
    except Exception as ex:
        logger.error("An error occurred: %r", ex)
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))


@click.command(name="list-checks", context_settings=CONTEXT_SETTINGS)
@click.option(
    "--ruleset",
    "-r",
    type=click.STRING,
    envvar="COLIN_RULESET",
    help="Select a predefined ruleset (e.g. fedora).",
)
@click.option(
    "--ruleset-file",
    "-f",
    type=click.File(mode="r"),
    help="Path to a file to use for validation "
    "(by default they are placed in /usr/share/colin/rulesets).",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Enable debugging mode (debugging logs, full tracebacks).",
)
@click.option(
    "--json", type=click.File(mode="w"), help="File to save the output as json to."
)
@click.option(
    "-s",
    "--skip",
    multiple=True,
    type=click.STRING,
    help="Name of the check to skip. (this option is repeatable)",
)
@click.option(
    "--tag", "-t", multiple=True, type=click.STRING, help="Filter checks with the tag."
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode.")
@click.option(
    "checks_paths",
    "--checks-path",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    multiple=True,
    envvar=COLIN_CHECKS_PATH,
    help=f"Path to directory containing checks (default {get_checks_paths()}).",
)
def list_checks(ruleset, ruleset_file, debug, json, skip, tag, verbose, checks_paths):
    """
    Print the checks.
    """
    if ruleset and ruleset_file:
        raise click.BadOptionUsage(
            "Options '--ruleset' and '--file-ruleset' cannot be used together."
        )

    try:
        if not debug:
            logging.basicConfig(stream=six.StringIO())

        log_level = _get_log_level(debug=debug, verbose=verbose)
        checks = get_checks(
            ruleset_name=ruleset,
            ruleset_file=ruleset_file,
            logging_level=log_level,
            tags=tag,
            checks_paths=checks_paths,
            skips=skip,
        )
        _print_checks(checks=checks)

        if json:
            AbstractCheck.save_checks_to_json(file=json, checks=checks)
    except ColinException as ex:
        logger.error("An error occurred: %r", ex)
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
    except Exception as ex:
        logger.error("An error occurred: %r", ex)
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))


@click.command(name="list-rulesets", context_settings=CONTEXT_SETTINGS)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Enable debugging mode (debugging logs, full tracebacks).",
)
def list_rulesets(debug):
    """
    List available rulesets.
    """
    try:
        rulesets = get_rulesets()
        max_len = max(len(r[0]) for r in rulesets)
        for r in rulesets:
            click.echo("{0: <{1}} ({2})".format(r[0], max_len, r[1]))
    except Exception as ex:
        logger.error("An error occurred: %r", ex)
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))


@click.command(name="info", context_settings=CONTEXT_SETTINGS)
def info():
    """
    Show info about colin and its dependencies.
    """
    installation_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir)
    )

    click.echo(f"colin {__version__} {installation_path}")
    click.echo(f"colin-cli {os.path.realpath(__file__)}\n")

    rpm_installed = is_rpm_installed()
    click.echo(
        get_version_msg_from_the_cmd(package_name="podman", use_rpm=rpm_installed)
    )
    click.echo(
        get_version_msg_from_the_cmd(package_name="skopeo", use_rpm=rpm_installed)
    )
    click.echo(
        get_version_msg_from_the_cmd(package_name="umoci", use_rpm=rpm_installed)
    )


cli.add_command(check)
cli.add_command(list_checks)
cli.add_command(list_rulesets)
cli.add_command(info)
cli.set_default_command(check)  # type: ignore


def _print_results(results, stat=False, verbose=False):
    """
    Prints the results to the stdout

    :type verbose: bool
    :param results: generator of results
    :param stat: if True print stat instead of full output
    """
    results.generate_pretty_output(
        stat=stat, verbose=verbose, output_function=click.secho
    )


def _print_checks(checks):
    if not checks:
        click.echo("No check found.")
        return
    for check in checks:
        click.echo(str(check))


def _get_log_level(debug, verbose):
    if debug:
        return logging.DEBUG
    elif verbose:
        return logging.INFO
    else:
        return logging.WARNING


if __name__ == "__main__":
    cli()
