import click
import json
import urllib.request


@click.command(
    name="create-repo",
    context_settings={"help_option_names": ["--help", "-h"]},
)
@click.argument("name", required=True)
@click.option("--org", "-g", default=None, help="Organization name.")
@click.option("--path", "-p", help="Path of repository.", metavar="PATH", default=None)
@click.option(
    "--description", "-d", help="Short description.", metavar="DESC", default=None
)
@click.option(
    "--homepage", "-e", help="URL with more information.", metavar="URL", default=None
)
@click.option("--private", "-r", help="Private repository.", is_flag=True, default=True)
@click.option(
    "--has-issues", "-i", help="With issues page.", is_flag=True, default=True
)
@click.option("--has-wiki", "-w", help="With wiki page.", is_flag=True, default=True)
@click.option(
    "--can-comment", "-m", help="Can make comments.", is_flag=True, default=True
)
@click.option(
    "--auto-init", "-a", help="Create an initial commit.", is_flag=True, default=False
)
@click.option(
    "--gitignore-template",
    "-n",
    help="Apply .gitignore template.",
    metavar="LANG",
    default=None,
)
@click.option(
    "--license-template",
    "-l",
    help="Apply license template.",
    metavar="LICENSE",
    default=None,
)
@click.pass_context
def command(ctx, **kwargs):
    """create user or org repositories"""
    kwargs["access_token"] = ctx.obj["access_token"]
    org = kwargs.pop("org", None)
    url = "https://gitee.com/api/v5/user/repos"
    if org is not None:
        url = f"https://gitee.com/api/v5/orgs/{org}/repos"
    req = urllib.request.Request(
        url=url,
        method="POST",
        headers={"Content-Type": "application/json;charset=UTF-8"},
        data=bytes(json.dumps(kwargs).encode("utf-8")),
    )
    urllib.request.urlopen(req)
