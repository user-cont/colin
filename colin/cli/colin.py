import click as click

from ..core.constant import COLOURS, OUTPUT_CHARS
from ..core.exceptions import ColinException
from ..core.colin import run

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('target', type=click.STRING)
@click.option('--config', '-c', type=click.STRING,
              help="Name of the configuration or path.")
@click.option('--json', type=click.File(mode='w'),
              help="File to save the output as json to.")
@click.option('--stat', '-s', is_flag=True,
              help="Print statistics instead of full results.")
def cli(target, config, json, stat):
    try:
        results = run(name_of_target=target,
                      config_name=config)
        _print_results(results=results, stat=stat)

        if json:
            results.save_json_to_file(file=json)

    except ColinException as ex:
        raise click.ClickException(str(ex))
    except Exception as ex:
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


if __name__ == '__main__':
    cli()
