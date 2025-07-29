import click
import json
import urllib.parse
import urllib.request


@click.command("list-repos")
@click.option("--page", "-p", help="Current page", metavar="NUM", type=int, default=1)
@click.option(
    "--repos-per-page",
    "-r",
    help="Repositories per page",
    metavar="NUM",
    type=int,
    default=20,
)
@click.pass_context
def command(ctx, **kwargs):
    """List all repositories"""
    kwargs["access_token"] = ctx.obj["access_token"]
    kwargs["per_page"] = kwargs["repos_per_page"]
    del kwargs["repos_per_page"]

    req = urllib.request.Request(
        url="https://gitee.com/api/v5/user/repos?%s" % urllib.parse.urlencode(kwargs),
        method="GET",
        headers={"Content-Type": "application/json;charset=UTF-8"},
    )

    with urllib.request.urlopen(req) as response:
        for repo in json.loads(response.read().decode("utf-8")):
            print(repo["full_name"])
