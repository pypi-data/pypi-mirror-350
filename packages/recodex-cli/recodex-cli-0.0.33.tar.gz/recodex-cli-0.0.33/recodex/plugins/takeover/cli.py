import click
from pathlib import Path

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_data_dir, pass_api_client


@click.command()
@click.argument("user_id")
@pass_api_client
@pass_data_dir
def takeover(data_dir:Path, api: ApiClient, user_id):
    """
    Log in as a different user
    """

    token = api.takeover(user_id)["accessToken"]
    UserContext(api.api_url, token).store(data_dir / "context.yaml")
