import click
import logging
from pprint import pprint
from pathlib import Path
from ruamel.yaml import YAML

from recodex.decorators import pass_config_dir, pass_api_client
from recodex.api import ApiClient
from .codex_config import load_codex_test_config
from .plugin_config import Config
from .utils import load_details, load_active_text, load_exercise_files, make_exercise_config, load_content, \
    load_additional_files, load_allowed_extensions, load_reference_solution_details, get_custom_judges, \
    load_reference_solution_file, replace_file_references, upload_file


@click.group()
def cli():
    """
    Tools for working with legacy CodEx exercises (and importing them)
    """
    pass


@cli.command()
@click.argument("exercise_folder")
@pass_api_client
def details(api: ApiClient, exercise_folder):
    soup = load_content(exercise_folder)

    print("### Exercise details")
    pprint(load_details(soup))
    print()

    print("### Exercise assignment text")
    pprint(load_active_text(soup))
    print()

    config = Config.load(Path.cwd() / "import-config.yml")
    tests = load_codex_test_config(
        Path(exercise_folder) / "testdata" / "config")
    test_id_map = {test.name: test.number for test in tests}
    files = []

    print("### Exercise files")
    for name, path in load_exercise_files(exercise_folder):
        print(f"{path} as {name}")
        # Make sure the file names are present in the exercise file list
        files.append(name)

    print("### Exercise configuration")
    pprint(make_exercise_config(config, soup, files,
           api.get_pipelines(), tests, test_id_map))
    print()


@cli.command()
@click.argument("exercise_folder")
def name(exercise_folder):
    content_soup = load_content(exercise_folder)
    details = load_details(content_soup)
    print(details["name"])


@cli.command()
@click.argument("exercise_folder")
def has_dir_test(exercise_folder):
    tests = load_codex_test_config(
        Path(exercise_folder) / "testdata" / "config")
    for test in tests:
        if test.in_type == "dir":
            print(test.number, "in")
        if test.out_type == "dir":
            print(test.number, "out")


@cli.command()
@click.argument("exercise_folder", nargs=-1)
@pass_api_client
def get_id(api: ApiClient, exercise_folder):
    """
    Look up an imported exercise in the API and print its ID
    """

    exercises = api.get_exercises()

    for folder in exercise_folder:
        found = False
        content_soup = load_content(folder)
        details = load_details(content_soup)
        for exercise in exercises:
            if exercise["name"] == details["name"]:
                print(folder, exercise["id"])
                found = True
                break

        if not found:
            print(folder, "Nothing found")


@cli.command()
@click.option("exercise_id", "-e")
@click.argument("exercise_folder")
@pass_api_client
def set_score_config(api: ApiClient, exercise_id, exercise_folder):
    tests = load_codex_test_config(
        Path(exercise_folder) / "testdata" / "config")

    score_config = {test.name: int(test.points) for test in tests}
    yaml = YAML(typ="safe")
    api.set_exercise_score_config(exercise_id, yaml.dump(
        {"testWeights": score_config}, default_flow_style=False))


@cli.command(name="import")
@click.option("exercise_id", "-e")
@click.option("group_id", "-g")
@click.option("hwgroup_id", "-w")
@click.argument("exercise_folder")
@pass_api_client
@pass_config_dir
def run_import(config_dir: Path, api: ApiClient, exercise_folder, group_id, exercise_id=None, hwgroup_id=None):
    logging.basicConfig(level=logging.INFO)

    config = Config.load(config_dir / "codex_import.yml")

    logging.info("*** Importing from %s", exercise_folder)

    content_soup = load_content(exercise_folder)
    logging.info("content.xml loaded")

    # If no exercise ID was given, create a new, empty exercise
    if exercise_id is None:
        creation_payload = api.create_exercise(group_id)
        exercise_id = creation_payload["id"]
        logging.info("Exercise created with id %s", exercise_id)
    else:
        logging.info("Reusing exercise with id %s", exercise_id)

    # Upload additional files (attachments) and associate them with the exercise
    text_id, text = load_active_text(content_soup)
    attachment_ids = set()

    logging.info("Uploading attachments")
    for path in load_additional_files(exercise_folder, text_id):
        attachment_ids.add(upload_file(api, path)["id"])

    if attachment_ids:
        api.add_exercise_attachments(exercise_id, list(attachment_ids))

    logging.info("Uploaded attachments associated with the exercise")

    # Prepare the exercise text
    attachments = api.get_exercise_attachments(exercise_id)
    url_map = {item["name"]: "{}/v1/uploaded-files/{}/download".format(
        api.api_url, item["id"]) for item in attachments}
    text = replace_file_references(text, url_map)

    # Set the details of the new exercise
    details = load_details(content_soup)
    details["localizedTexts"] = [{
        "locale": config.locale,
        "name": details["name"] or "",
        "description": details["description"] or "",
        "text": text or ""
    }]

    del details["name"]
    del details["description"]

    api.update_exercise(exercise_id, details)
    logging.info("Exercise details updated")

    # Upload exercise files and associate them with the exercise
    exercise_file_data = {}

    logging.info("Uploading supplementary exercise files")
    for name, path in load_exercise_files(exercise_folder):
        exercise_file_data[name] = upload_file(api, path, name)

    api.add_exercise_files(exercise_id, [data["id"]
                           for data in exercise_file_data.values()])
    logging.info("Uploaded exercise files associated with the exercise")

    # Configure environments
    extensions = list(load_allowed_extensions(content_soup))
    environments = [config.extension_to_runtime[ext] for ext in extensions]
    env_data = {item["id"]: item for item in api.get_runtime_environments()}
    env_configs = [
        {
            "runtimeEnvironmentId": env_id,
            "variablesTable": env_data[env_id]["defaultVariables"]
        } for env_id in environments
    ]

    api.update_environment_configs(exercise_id, env_configs)
    logging.info("Added environments %s", ", ".join(environments))

    # Configure tests
    tests = load_codex_test_config(
        Path(exercise_folder) / "testdata" / "config")

    api.set_exercise_tests(
        exercise_id, [{"name": test.name} for test in tests])
    test_id_map = {test["name"]: test["id"]
                   for test in api.get_exercise_tests(exercise_id)}
    logging.info("Exercise tests configured")

    # Upload custom judges
    custom_judges = set(get_custom_judges(tests))
    custom_judge_files = {}

    if custom_judges:
        logging.info("Uploading custom judges")
        for judge in custom_judges:
            judge_path = Path(exercise_folder).joinpath(
                "testdata").joinpath(judge)
            custom_judge_files[judge] = upload_file(
                api, judge_path, judge_path.name)

        api.add_exercise_files(
            exercise_id, [data["id"] for data in custom_judge_files.values()])
        logging.info("Uploaded judge files associated with the exercise")

    exercise_config = make_exercise_config(
        config,
        content_soup,
        [item["name"] for item in api.get_exercise_files(exercise_id)],
        api.get_pipelines(),
        tests,
        test_id_map
    )

    api.update_exercise_config(exercise_id, exercise_config)
    logging.info("Exercise config updated")

    # Configure test limits
    if hwgroup_id is None:
        hwgroup_id = api.get_hwgroups()[0]['id']

    for extension, environment_id in zip(extensions, environments):
        limits_config = {}

        for test in tests:
            key = extension if extension in test.limits.keys() else "default"
            limits_config[test_id_map[test.name]] = {
                "wall-time": test.limits[key].time_limit,
                "memory": test.limits[key].mem_limit
            }

        api.update_limits(exercise_id, environment_id,
                          hwgroup_id, limits_config)
        logging.info("Limits set for environment %s", environment_id)

    # Upload reference solutions
    for solution_id, solution in load_reference_solution_details(content_soup, config.extension_to_runtime):
        path = load_reference_solution_file(
            solution_id, content_soup, exercise_folder)
        solution["files"] = [upload_file(api, path)["id"]]
        payload = api.create_reference_solution(exercise_id, solution)

        logging.info("New reference solution created, with id %s",
                     payload["referenceSolution"]["id"])
