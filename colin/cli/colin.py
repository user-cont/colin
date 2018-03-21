import click as click
from six import iteritems

from ..core.constant import COLOURS
from ..core.exceptions import ColinException
from ..core.colin import run

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('target', type=click.STRING)
@click.option('--config', '-c', type=click.STRING,
              help="Configuration name.")
@click.option('--json', type=click.File(mode='w'), help="File to save the output as json to.")
def cli(target, config, json):
    try:
        results = run(name_of_target=target,
                      config_name=config)

        for group, check_results in results.results:

            group_title_printed = False
            for r in check_results:

                if not group_title_printed:
                    click.echo("{}:".format(group.upper()))
                    group_title_printed = True

                click.secho(str(r), err=r.ok, fg=COLOURS[r.status])
                if not r.ok:
                    click.secho("   -> {}\n"
                                "   -> {}\n"
                                "   -> {}".format(r.message,
                                                  r.description,
                                                  r.reference_url),
                                fg=COLOURS[r.status])
        if json:
            results.save_json_to_file(file=json)

    except ColinException as ex:
        raise click.ClickException(str(ex))
    except Exception as ex:
        raise click.ClickException(str(ex))


if __name__ == '__main__':
    cli()
