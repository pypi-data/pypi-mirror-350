import json
from ruamel.yaml import YAML
import sys
import time

import click

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    Tools for manipulating shadow asignments
    """


@cli.command()
@click.argument("group_id")
@pass_api_client
def create(api: ApiClient, group_id):
    """
    Create new shadow assignment in a group
    """

    assignment = api.create_shadow_assignment(group_id)
    click.echo(assignment["id"])


@cli.command()
@click.argument("assignment_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get(api: ApiClient, assignment_id, useJson):
    """
    Get shadow assignment data (including user points)
    """

    assignment = api.get_shadow_assignment(assignment_id)
    if useJson is True:
        json.dump(assignment, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(assignment, sys.stdout)
    else:
        for localizedText in assignment["localizedTexts"]:
            click.echo("{} {}".format(
                localizedText["locale"], localizedText["name"]))
        click.echo()
        for points in assignment["points"]:
            click.echo("{} {} {}".format(
                points["awardeeId"], points["points"], points["note"]))


@cli.command()
@click.argument("assignment_id")
@pass_api_client
def update(api: ApiClient, assignment_id):
    """
    Update shadow assignment (JSON with modifications must be given on stdin).
    """

    keys = ["version", "isPublic", "isBonus",
            "localizedTexts", "maxPoints", "deadline"]

    assignment = api.get_shadow_assignment(assignment_id)
    to_update_input = sys.stdin.read().strip()
    to_update = json.loads(to_update_input)

    data = {"sendNotification": False}
    for key in keys:
        data[key] = to_update.get(key, assignment[key])

    api.update_shadow_assignment(assignment_id, data)


@cli.command()
@click.argument("assignment_id")
@click.argument("user_id")
@click.argument("points")
@click.argument("note")
@pass_api_client
def create_points(api: ApiClient, assignment_id, user_id, points, note):
    """
    Create shadow assignment points record (for one user)
    """

    awarded_at = int(time.time())
    api.create_shadow_assignment_points(
        assignment_id, user_id, int(points), note, awarded_at)


@cli.command()
@click.argument("points_id")
@click.argument("points")
@click.argument("note")
@pass_api_client
def update_points(api: ApiClient, points_id, points, note):
    """
    Update shadow assignment points (one points record of one user)
    """

    awarded_at = int(time.time())
    api.update_shadow_assignment_points(points_id, int(points), note,
                                        awarded_at)


@cli.command()
@click.argument("points_id")
@pass_api_client
def delete_points(api: ApiClient, points_id):
    """
    Delete shadow assignment points record (of one user)
    """

    api.delete_shadow_assignment_points(points_id)
