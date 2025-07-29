import os

import click


@click.command(
    name="pull-gitee",
    context_settings={"help_option_names": ["--help", "-h"]},
)
@click.argument("path", required=True)
def pull_gitee(path):
    url = f"https://gitee.com/{path}.git"
    commands = [
        f"git clone {url}",
    ]
    for command in commands:
        os.system(command)
