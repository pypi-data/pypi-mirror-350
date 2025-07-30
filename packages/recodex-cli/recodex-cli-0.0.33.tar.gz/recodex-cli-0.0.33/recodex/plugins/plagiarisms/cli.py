import sys
import click
import json
from ruamel.yaml import YAML

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    API related to plagiarism detection and suspected solution similarities
    """


@cli.command()
@click.argument("tool")
@click.argument("tool_params")
@pass_api_client
def create_batch(api: ApiClient, tool, tool_params):
    """
    Create a new plagiarism detection batch
    """
    batch = api.create_plagiarism_batch(tool, tool_params)
    click.echo(batch["id"])


@cli.command()
@click.argument("id")
@click.option("--upload-completed/--upload-reopen", "completed", default=None)
@click.option("--assignments", "assignments", is_flag=True)
@pass_api_client
def update_batch(api: ApiClient, id, completed, assignments):
    """
    Update a plagiarism detection batch (whether its upload has been completed).
    Mark assignments as checked by the batch.
    """
    ids = None
    if assignments:
        ids = []
        data = sys.stdin.read()
        for token in data.split():
            token = token.strip()
            if token:
                ids.append(token)

    api.update_plagiarism_batch(id, completed, ids)


@cli.command()
@click.argument("id")
@click.argument("solution_id")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def add_similarity(api: ApiClient, id, solution_id, useJson):
    """
    Add detected similarity record to open plagiarism detection batch
    """

    if useJson:
        data = json.load(sys.stdin)
    else:
        yaml = YAML(typ="safe")
        data = yaml.load(sys.stdin)
    print(data)
    api.add_plagiarism_detected_similarity(id, solution_id, data)
