import click
import csv
import sys
import json
from ruamel.yaml import YAML

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_user_context, pass_api_client


@click.group()
def cli():
    """
    Tools for user manipulation
    """


def format_user_csv(user):
    return {
        'id': user['id'],
        'title_before': user['name']['titlesBeforeName'],
        'first_name': user['name']['firstName'],
        'last_name': user['name']['lastName'],
        'title_after': user['name']['titlesAfterName'],
        'avatar_url': user['avatarUrl'],
    }


@cli.command()
@click.argument("user_id")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def get(api: ApiClient, user_id, useJson):
    """
    Get user data and print it in JSON or Yaml.
    """
    user = api.get_user(user_id)
    if useJson:
        json.dump(user, sys.stdout, sort_keys=True, indent=4)
    else:
        yaml = YAML(typ="safe")
        yaml.dump(user, sys.stdout)


@cli.command()
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def get_list(api: ApiClient, useJson):
    """
    Get data of multiple users, list of IDs is given on stdin (one ID per line)
    """
    ids = map(lambda id: id.strip(), sys.stdin.readlines())
    ids = list(filter(lambda id: id, ids))

    users = api.get_users_list(ids)
    if useJson:
        json.dump(users, sys.stdout, sort_keys=True, indent=4)
    else:
        yaml = YAML(typ="safe")
        yaml.dump(users, sys.stdout)


@cli.command()
@click.option("--json/--yaml", "useJson", default=None, help='Default is CSV.')
@click.option('--only-active', 'onlyActive', is_flag=True, help='Return full records formated into CSV.')
@click.option("search", "-s", default=None, help="Substring to search")
@click.option("roles", "-r", default=None, help="Roles split by comma")
@pass_user_context
@pass_api_client
def search(api: ApiClient, context: UserContext, search, roles, useJson, onlyActive):
    """
    Search for a user
    """
    if roles is not None:
        roles = roles.split(',')

    users = []
    instances_ids = api.get_user(context.user_id)[
        "privateData"]["instancesIds"]
    for instance_id in instances_ids:
        for user in api.search_users(instance_id, search, roles):
            if not onlyActive or user.get("privateData", {}).get("isAllowed", False):
                users.append(user)

    if useJson is True:
        json.dump(users, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(users, sys.stdout)
    else:
        # print CSV header
        fieldnames = ['id', 'title_before', 'first_name',
                      'last_name', 'title_after', 'avatar_url']
        csv_writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        csv_writer.writeheader()

        for user in users:
            csv_writer.writerow(format_user_csv(user))


@cli.command()
@click.argument("email")
@click.argument("first_name")
@click.argument("last_name")
@click.option('--password', help='Password. If no password is given, it is prompted.',
              prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--instance_id', help='Instance where the new user belongs to. If no instance is provided, instance of logged user is taken.')
@click.option('--join_group', multiple=True, help='Id of a group which is immediately joined by the registered user. This option may be repeated.')
@pass_user_context
@pass_api_client
def register(api: ApiClient, context: UserContext, email, first_name, last_name, password, instance_id, join_group):
    """
    Register new user with local account
    """
    if instance_id is None:
        instances_ids = api.get_user(context.user_id)[
            "privateData"]["instancesIds"]
        if len(instances_ids) != 1:
            click.echo(
                "Instance ID is ambiguous. Provide explicit ID via --instance_id option.")
            return
        instance_id = instances_ids[0]

    res = api.register_user(
        instance_id, email, first_name, last_name, password)
    user_id = res['user']['id']
    click.echo("User {id} ({first_name} {last_name}, {email}) registered in instance {instance_id}".format(
        id=user_id, first_name=first_name, last_name=last_name, email=email, instance_id=instance_id))

    for group_id in join_group:
        api.group_add_student(group_id, user_id)
        click.echo("User {} joined group {}".format(user_id, group_id))


@cli.command()
@click.argument("id")
@click.option("--name", nargs=2, help="New name as two arguments (first_name last_name).")
@click.option("--gravatar/--no-gravatar")
@pass_api_client
def edit(api: ApiClient, id, name, gravatar):
    """
    Edit profile of a user
    """

    user = api.get_user(id)
    data = {
        "degreesAfterName": user['name']['degreesBeforeName'],
        "degreesBeforeName": user['name']['degreesAfterName'],
        "email": user["privateData"]["email"],
        "gravatarUrlEnabled": user['avatarUrl'] is not None,
    }

    if name is not None:
        data["firstName"] = name[0]
        data["lastName"] = name[1]

    if gravatar is not None:
        data["gravatarUrlEnabled"] = gravatar
    api.update_user(id, data)


@cli.command()
@click.argument("id")
@pass_api_client
def enable(api: ApiClient, id):
    """
    Enable user (who was previously disabled)
    """

    api.set_allow_user(id, True)


@cli.command()
@click.argument("id")
@pass_api_client
def disable(api: ApiClient, id):
    """
    Disable user (the user will no longer be allowed to log in or perform any other API calls)
    """

    api.set_allow_user(id, False)


@cli.command()
@click.argument("id")
@pass_api_client
def delete(api: ApiClient, id):
    """
    Delete user (users are only soft-deleted)
    """

    api.delete_user(id)
