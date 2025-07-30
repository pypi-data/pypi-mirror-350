import json
from ruamel.yaml import YAML
import logging
import sys
import io
import os
from datetime import datetime, timedelta
from tempfile import mkdtemp
import shutil

import click

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    Tools for working with exercises
    """


@cli.command()
@click.option("--json/--yaml", "useJson", default=None)
@click.option("--offset", "-o", type=int, default=0)
@click.option("--limit", "-l", type=int, default=0)
@click.option("--order", default=None)
@click.option("--locale", default='en')
@pass_api_client
def list_all(api: ApiClient, useJson, offset, limit, order, locale):
    """
    List all exercises (as ID and name) in JSON, Yaml, or as a plain list.
    """
    exercises = api.get_exercises(offset, limit, order, locale)
    if useJson is True:
        json.dump(exercises, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(exercises, sys.stdout)
    else:
        for exercise in exercises:
            click.echo("{}\t{}".format(exercise["id"], exercise["name"]))


@cli.command()
@click.argument("exercise_id")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def get(api: ApiClient, exercise_id, useJson):
    """
    Get exercise data and print it in JSON or Yaml.
    """
    exercise = api.get_exercise(exercise_id)
    if useJson:
        json.dump(exercise, sys.stdout, sort_keys=True, indent=4)
    else:
        yaml = YAML(typ="safe")
        yaml.dump(exercise, sys.stdout)


@cli.command()
@click.argument("solution_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_ref_solution(api: ApiClient, solution_id, useJson):
    """
    Get one reference solution by its id.
    """
    solution = api.get_reference_solution(solution_id)
    if useJson is True:
        json.dump(solution, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(solution, sys.stdout)
    else:
        ts = int(solution["createdAt"])
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        click.echo("{} {} {} {}".format(solution["id"], solution["runtimeEnvironmentId"],
                                        date, solution["description"]))


@cli.command()
@click.argument("exercise_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_ref_solutions(api: ApiClient, exercise_id, useJson):
    """
    List all reference solutions of given exercise in JSON, Yaml, or as a plain list.
    """
    solutions = api.get_reference_solutions(exercise_id)
    if useJson is True:
        json.dump(solutions, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(solutions, sys.stdout)
    else:
        for solution in solutions:
            ts = int(solution["createdAt"])
            date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("{} {} {} {}".format(solution["id"], solution["runtimeEnvironmentId"],
                                            date, solution["description"]))


@cli.command()
@click.argument("ref_solution_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_ref_solution_evaluations(api: ApiClient, ref_solution_id, useJson):
    """
    Get reference solution evaluations and print them all in JSON or Yaml, or as a plain list.
    """
    evaluations = api.get_reference_solution_evaluations(ref_solution_id)
    if useJson is True:
        json.dump(evaluations, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(evaluations, sys.stdout)
    else:
        for evaluation in evaluations:
            ts = int(evaluation["submittedAt"])
            date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("{} {} {} {}".format(evaluation["id"],
                       evaluation["evaluationStatus"], evaluation["isCorrect"], date))


@cli.command()
@click.argument("solution_id")
@pass_api_client
def delete_ref_solution(api: ApiClient, solution_id):
    """
    Delete referenece solution and including all its evaluations.
    """
    api.delete_reference_solution(solution_id)


@cli.command()
@click.argument("evaluation_id")
@pass_api_client
def delete_ref_solution_evaluation(api: ApiClient, evaluation_id):
    """
    Delete referenece solution evaluation and all the results and logs.
    """
    api.delete_reference_solution_evaluation(evaluation_id)


@cli.command()
@click.argument("ref_solution_id")
@click.option('--debug', is_flag=True)
@pass_api_client
def resubmit_ref_solution(api: ApiClient, ref_solution_id, debug):
    """
    Resubmit reference solution for another evaluation.
    """
    api.resubmit_reference_solution(ref_solution_id, debug)


@cli.command()
@click.argument("locale")
@click.argument("exercise_id")
@click.option('--include_name', is_flag=True)
@pass_api_client
def add_localization(api: ApiClient, locale, exercise_id, include_name):
    """
    Add (or update if exists) a localized text of an exercise. The text is read from the standard input.
    If includeName flag is set, the first line of the input is used as the name.
    """
    full_exercise = api.get_exercise(exercise_id)
    copy_props = ["version", "difficulty", "localizedTexts", "isPublic", "isLocked", "configurationType",
                  "solutionFilesLimit", "solutionFilesLimit", "solutionSizeLimit", "mergeJudgeLogs"]
    exercise = {}
    for prop in copy_props:
        exercise[prop] = full_exercise[prop]

    localizedText = next(
        (lt for lt in exercise["localizedTexts"] if lt["locale"] == locale), None)
    if localizedText is None:
        localizedText = {
            "locale": locale,
            "name": "",
            "text": "",
            "link": "",
            "description": ""
        }
        exercise["localizedTexts"].append(localizedText)

    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    if include_name is True:
        localizedText["name"] = input_stream.readline().strip()

    localizedText["text"] = input_stream.read()
    api.update_exercise(exercise_id, exercise)


def _add_reference_solution(api: ApiClient, exercise_id, note, runtime_environment, files):
    uploaded_files = [api.upload_file(file, open(file, "rb"))[
        "id"] for file in files]

    preflight = api.presubmit_check(exercise_id, uploaded_files)
    if (preflight["environments"] is None or len(preflight["environments"]) == 0):
        print('No valid environments found for given files.', file=sys.stderr)
        return

    if runtime_environment is None:
        runtime_environment = preflight["environments"][0]

    if runtime_environment not in preflight["environments"]:
        print('Selected runtime {} is not allowed by the preflight check.'.format(
            runtime_environment), file=sys.stderr)
        return

    submit_data = {
        "note": note,
        "runtimeEnvironmentId": runtime_environment,
        "files": uploaded_files
    }
    variables = next((sv for sv in preflight['submitVariables'] if sv.get(
        "runtimeEnvironmentId") == runtime_environment), {}).get('variables', [])
    entry_point = next(
        (v for v in variables if v.get('name') == 'entry-point'), None)
    if entry_point is not None:
        submit_data["solutionParams"] = {"variables": [
            {"name": "entry-point", "value": os.path.basename(files[0])}]}

    return api.create_reference_solution(exercise_id, submit_data)


@cli.command()
@click.argument("files", nargs=-1)
@click.option("exercise_id", "-e", help="Exercise ID")
@click.option("note", "-n", default="", help="Note associated with the solution")
@click.option("runtime_environment", "-r", default=None, help="Runtime environment ID")
@pass_api_client
def add_reference_solution(api: ApiClient, exercise_id, note, runtime_environment, files):
    if len(files) == 0:
        print('No files given.', file=sys.stderr)
        return
    result = _add_reference_solution(
        api, exercise_id, note, runtime_environment, files)
    click.echo(result["referenceSolution"]["id"])


@cli.command()
@click.option("config_path", "-c")
@pass_api_client
def evaluate_all_rs(api: ApiClient):
    """
    Request evaluation for all reference solutions
    """
    with click.progressbar(api.get_exercises()) as bar:
        for exercise in bar:
            try:
                api.evaluate_reference_solutions(exercise["id"])
            except Exception as e:
                logging.error("Error in exercise {}: {}".format(
                    exercise["id"], str(e)))


@cli.command()
@click.option("threshold", "-t")
@pass_api_client
def check_rs_evaluations(api: ApiClient, threshold):
    """
    Find exercises that had no successful reference solution evaluation in
    a given number of days
    """
    for exercise in api.get_exercises():
        solutions = api.get_reference_solutions(exercise["id"])
        if not solutions:
            logging.error(
                "Exercise %s has no reference solutions", exercise["id"])
            continue

        found = False
        found_recent = False

        for solution in solutions:
            for evaluation in api.get_reference_solution_evaluations(solution["id"]):
                status_ok = evaluation["evaluationStatus"] == "done"
                submission_timestamp = int(evaluation["submittedAt"])
                submission_timestamp = max(0, submission_timestamp)
                submission_date = datetime.fromtimestamp(submission_timestamp)
                threshold_date = datetime.utcnow() - timedelta(days=int(threshold))
                recent = submission_date >= threshold_date
                if status_ok:
                    found = True
                    if recent:
                        found_recent = True
                        break

        if not found_recent:
            if found:
                logging.error(
                    "Exercise %s has no recent successful evaluations", exercise["id"])
            else:
                logging.error(
                    "Exercise %s has never had any successful evaluations", exercise["id"])


@cli.command()
@click.argument("exercise_id")
@pass_api_client
def delete(api: ApiClient, exercise_id):
    api.delete_exercise(exercise_id)


@cli.command()
@click.argument("exercise_id")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def get_config(api: ApiClient, exercise_id, useJson):
    """
    Get exercise configuration in JSON (or possibly yaml) format
    """
    config = api.get_exercise_config(exercise_id)
    if useJson:
        json.dump(config, sys.stdout, sort_keys=True, indent=4)
    else:
        yaml = YAML(typ="safe")
        yaml.dump(config, sys.stdout)


@cli.command()
@click.argument("exercise_id")
@click.argument("file_name")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def set_config(api: ApiClient, exercise_id, file_name, useJson):
    """
    Load a JSON or YAML from a file and set it as configuration.
    """
    with open(file_name, 'r', encoding="utf-8") as stream:
        if useJson:
            config = json.load(stream)
        else:
            yaml = YAML(typ="safe")
            config = yaml.load(stream)
    api.update_exercise_config(exercise_id, config)


@cli.command()
@click.argument("exercise_id")
@click.option("--excavate/--archive", "excavate", default=False)
@pass_api_client
def set_archived(api: ApiClient, exercise_id, excavate):
    """
    Set the archived flag of an exercise (put it into archived mode or excavate from archive).
    """
    api.set_exercise_archived(exercise_id, not excavate)


@cli.command()
@click.argument("exercise_id")
@click.argument("author")
@pass_api_client
def set_author(api: ApiClient, exercise_id, author):
    """
    Change the author of the exercise.
    """
    api.set_exercise_author(exercise_id, author)


@cli.command()
@click.argument("exercise_id")
@click.option('--admin', '-a', multiple=True)
@pass_api_client
def set_admins(api: ApiClient, exercise_id, admin):
    """
    Set exercise admins (replaces current list of admins).
    """
    api.set_exercise_admins(exercise_id, admin)


@cli.command()
@click.option('--stats', is_flag=True)
@pass_api_client
def tags_get_all(api: ApiClient, stats):
    """
    Get all tag names available. Optionally with statistics (how many exercises use each tag).
    """
    if stats:
        tags = api.get_exercise_tags_stats()
        for tag, count in tags.items():
            click.echo("{} {}".format(tag, count))
    else:
        tags = api.get_exercise_tags()
        for tag in tags:
            click.echo(tag)


@cli.command()
@click.argument("exercise_id")
@click.argument("tag")
@pass_api_client
def tags_add(api: ApiClient, exercise_id, tag):
    """
    Add specific tag to given exercise
    """
    api.exercise_add_tag(exercise_id, tag)


@cli.command()
@click.argument("exercise_id")
@click.argument("tag")
@pass_api_client
def tags_remove(api: ApiClient, exercise_id, tag):
    """
    Remove specific tag from given exercise
    """
    api.exercise_remove_tag(exercise_id, tag)


@cli.command()
@click.argument("tag")
@click.argument("rename_to")
@click.option('--force', is_flag=True)
@pass_api_client
def tags_rename_global(api: ApiClient, tag, rename_to, force):
    """
    Rename a tag globally. If the new name already exists, the operation will fail unless forced. HANDLE WITH CARE!
    """
    res = api.exercise_tags_rename_global(tag, rename_to, force)
    click.echo("{} exercise(s) affected".format(res["count"]))


@cli.command()
@click.argument("tag")
@pass_api_client
def tags_remove_global(api: ApiClient, tag):
    """
    Remove a tag from all exercises. HANDLE WITH CARE!
    """
    res = api.exercise_tags_remove_global(tag)
    click.echo("{} exercise(s) affected".format(res["count"]))


@cli.command()
@click.argument("ref_solution_id")
@click.argument("visibility")
@pass_api_client
def set_ref_solution_visibility(api: ApiClient, ref_solution_id, visibility):
    """
    Change visibility of a reference solution.
    """
    api.update_reference_solution_visibility(ref_solution_id, int(visibility))


@cli.command()
@click.argument("exercise_id")
@click.argument("group_id")
@click.option('--complete', is_flag=True)
@pass_api_client
def fork(api: ApiClient, exercise_id, group_id, complete):
    """
    Copy (fork) given exercise and make the copy resident in specified group.
    If complete flag is present, the (public) ref. solutions is copied as well.
    """
    res = api.fork_exercise(exercise_id, group_id)
    new_id = res["id"]

    if complete:
        # reference solutions must be copied one by one
        solutions = api.get_reference_solutions(exercise_id)
        for solution in solutions:
            if solution["visibility"] <= 0:
                continue  # only public solutions are copied

            # we need to list and download files first
            files = api.get_reference_solution_files(solution["id"])
            file_names = []
            entry_point = None
            tmpdir = mkdtemp()  # into a temporary directory
            if not tmpdir:
                raise Exception("Unable to create a temporary directory.")

            for file in files:
                if not file["name"]:
                    continue
                path = tmpdir + '/' + file["name"]
                if file.get("isEntryPoint", False):
                    entry_point = path
                else:
                    file_names.append(path)
                api.download_file(file["id"], path)

            if entry_point is not None:
                # make sure entry point is the first file on the list
                file_names.insert(0, entry_point)

            if len(file_names) > 0:
                ref_res = _add_reference_solution(api, new_id, solution["description"],
                                                  solution["runtimeEnvironmentId"], file_names)
                api.update_reference_solution_visibility(
                    ref_res["referenceSolution"]["id"], solution["visibility"])

            shutil.rmtree(tmpdir)

    click.echo(new_id)
