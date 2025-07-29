import os

import click


@click.command(
    name="set-git",
    context_settings={"help_option_names": ["--help", "-h"]},
)
def set_git():
    commands = [
        "git config --global user.name birds",
        "git config --global user.email cg626@163.com",
        "git config --global credential.helper store",
    ]
    for command in commands:
        os.system(command)
