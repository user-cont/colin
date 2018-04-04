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

import click as click
from six import iteritems

from colin.checks.abstract.abstract_check import AbstractCheck
from ..core.constant import COLOURS, OUTPUT_CHARS
from ..core.exceptions import ColinException
from ..core.colin import run, get_checks
from ..version import __version__

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def _print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('target', type=click.STRING)
@click.option('--config', '-c', type=click.Choice(['redhat', 'fedora']),
              help="Select a predefined configuration.")
@click.option('--config-file', '-f', type=click.File(mode='r'),
              help="Path to a file to use for validation (by default they are placed in /usr/share/colin).")
@click.option('--debug', default=False, is_flag=True,
              help="Enable debugging mode (debugging logs, full tracebacks).")
@click.option('--json', type=click.File(mode='w'),
              help="File to save the output as json to.")
@click.option('--stat', '-s', is_flag=True,
              help="Print statistics instead of full results.")
@click.option('--print-checks', is_flag=True,
              help="Print the checks without running them.")
@click.option('--verbose', '-v', is_flag=True,
              help="Verbose mode.")
@click.option('--version', "-V", is_flag=True, callback=_print_version,
              expose_value=False, is_eager=True,
              help="Print version.")
def cli(target, config, config_file, debug, json, stat, print_checks, verbose, version):
    if config and config_file:
        raise click.BadOptionUsage("Options '--config' and '--file-config' cannot be used together.")

    try:
        if debug:
            log_level = logging.DEBUG
        elif verbose:
            log_level = logging.INFO
        else:
            log_level = logging.WARNING

        if print_checks:
            checks = get_checks(name_of_target=target,
                                config_name=config,
                                config_file=config_file,
                                logging_level=log_level)
            _print_checks(checks=checks)

            if json:
                AbstractCheck.save_checks_to_json(file=json, checks=checks)


        else:
            results = run(name_of_target=target,
                          config_name=config,
                          config_file=config_file,
                          logging_level=log_level)
            _print_results(results=results, stat=stat)

            if json:
                results.save_json_to_file(file=json)

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


def _print_results(results, stat=False):
    """
    Prints the results to the stdout

    :param results: generator of group results
    :param stat: if True print stat instead of full output
    """
    for group, check_results in results.results:

        group_title_printed = False
        for r in check_results:

            if not group_title_printed:
                click.secho("{}:".format(group.upper()),
                            nl=not stat)
                group_title_printed = True

            if stat:
                click.secho(OUTPUT_CHARS[r.status],
                            fg=COLOURS[r.status],
                            nl=False)
            else:
                click.secho(str(r), fg=COLOURS[r.status])
                if not r.ok:
                    click.secho("   -> {}\n"
                                "   -> {}\n"
                                "   -> {}".format(r.message,
                                                  r.description,
                                                  r.reference_url),
                                fg=COLOURS[r.status])

        if group_title_printed and stat:
            click.echo()


def _print_checks(checks):
    for (group, group_checks) in iteritems(checks):

        group_title_printed = False
        for check in group_checks:

            if not group_title_printed:
                click.secho("{}:".format(group.upper()))
                group_title_printed = True

            click.echo(str(check))


if __name__ == '__main__':
    cli()
