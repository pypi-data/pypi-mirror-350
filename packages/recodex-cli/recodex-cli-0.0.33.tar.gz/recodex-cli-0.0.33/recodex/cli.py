import json
from pprint import pprint

import appdirs
import click
import pkg_resources
import sys
from pathlib import Path

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_api_client, pass_data_dir, ReCodExContext


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """
    ReCodEx CLI
    """
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    config_dir = Path(appdirs.user_config_dir("recodex"))
    data_dir = Path(appdirs.user_data_dir("recodex"))

    context_path = data_dir / "context.yaml"
    user_context = UserContext.load(
        context_path) if context_path.exists() else UserContext()
    api_client = ApiClient(user_context.api_url, user_context.api_token)

    if user_context.api_token is not None and user_context.is_token_almost_expired() and not user_context.is_token_expired:
        user_context = user_context.replace_token(api_client.refresh_token())
        user_context.store(context_path)

    ctx.obj = ReCodExContext(
        api_client,
        config_dir,
        data_dir,
        user_context
    )


for entry_point in pkg_resources.iter_entry_points("recodex"):
    plugin = entry_point.load()
    plugin.name = entry_point.name
    cli.add_command(plugin)


@cli.command()
@click.argument("api_url")
@pass_data_dir
def init(data_dir: Path, api_url):
    """
    Set up the CLI with a token that you already own
    """

    api_token = click.prompt("API token")
    api = ApiClient(api_url, api_token)

    try:
        api.get_status()
    except:
        click.echo("API connection test failed", err=True)
        raise

    context = UserContext(api_url, api_token)

    data_dir.mkdir(parents=True, exist_ok=True)
    context.store(data_dir / "context.yaml")


@cli.command()
@pass_data_dir
@pass_api_client
def status(api: ApiClient, data_dir: Path):
    context = UserContext.load(data_dir / "context.yaml")

    if context.api_token is None:
        click.echo("No token is configured", err=True)
        sys.exit()

    if context.api_url is None:
        click.echo("No API URL is configured", err=True)
        sys.exit()

    click.echo("API URL: {}".format(context.api_url))
    click.echo("User ID: {}".format(context.user_id))

    if context.is_token_expired:
        click.echo("The token is expired", err=True)
        sys.exit()

    user_data = api.get_user(context.user_id)
    click.echo("User name: {}".format(user_data["fullName"]))


@cli.command()
@click.argument("method")
@click.argument("path")
@pass_api_client
def call(api: ApiClient, method, path):
    """
    Perform an API call directly
    """

    method = method.lower()
    data = {}

    if method in ("post", "put"):
        data = json.loads(sys.stdin.read())

    pprint(api.extract_payload(api.call(method, path, data=data)))


if __name__ == "__main__":
    cli()
