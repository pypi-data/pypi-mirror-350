import click
import urllib.request
import urllib.parse


@click.command("delete-repos")
@click.option("--owner", "-o", help="Repository owner", metavar="OWNER")
@click.argument("name")
@click.pass_context
def command(ctx, owner, name):
    """Delete existing repositories"""
    access_token = ctx.obj["access_token"]

    req = urllib.request.Request(
        url="https://gitee.com/api/v5/repos/%s/%s?access_token=%s"
        % (owner, name, access_token),
        method="DELETE",
        headers={"Content-Type": "application/json;charset=UTF-8"},
    )

    urllib.request.urlopen(req)
