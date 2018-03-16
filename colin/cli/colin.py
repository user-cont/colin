import click as click

from ..core.colin import run

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('target', type=click.STRING)
@click.option('--config', '-c', type=click.STRING,
              help="Configuration name.")
def cli(target, config):
    results = run(name_of_target=target,
                  config_name=config)

    for r in results.results:
        click.secho(str(r), err=r.ok, fg='green' if r.ok else 'red')
        if not r.ok:
            click.secho("   -> {}\n"
                        "   -> {}\n"
                        "   -> {}".format(r.message,
                                            r.description,
                                            r.reference_url),
                        fg='red')
        click.echo()


if __name__ == '__main__':
    cli()
