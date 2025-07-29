import os
import click
from configparser import ConfigParser
from . import create_repo
from . import delete_repos
from . import list_repos


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    from commands import __version__

    click.echo(__version__)
    ctx.exit()


@click.group(
    name="gitee-utils", context_settings={"help_option_names": ["--help", "-h"]}
)
@click.option(
    "--version",
    help="Show version information.",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--config-file",
    help="File path of configurations",
    metavar="FILE",
    required=False,
    default="%s/.init-gitee/config.ini" % (os.getenv("HOME")),
)
@click.pass_context
def cli(ctx, config_file) -> int:
    """A command-line tool to manage repositories on Gitee."""

    if not os.path.exists(config_file):
        raise Exception('Configuration file "%s" not found.' % config_file)

    config = ConfigParser()
    config.read(config_file)

    ctx.obj = {"access_token": config.get("auth", "access_token")}


cli.add_command(create_repo.command)
cli.add_command(delete_repos.command)
cli.add_command(list_repos.command)

if __name__ == "__main__":
    cli()
