import re
import logging
from bs4 import BeautifulSoup
from pathlib import Path
from html2text import html2text


def load_content(exercise_folder):
    content = (Path(exercise_folder) / "content.xml").read_bytes()
    return BeautifulSoup(content, "lxml")


def load_details(soup):
    result = {}

    result["name"] = soup.select("data name")[0].get_text()
    result["version"] = soup.find("exercise")["version"]
    result["description"] = soup.select("data comment")[0].get_text() or "Lorem ipsum"
    result["difficulty"] = "easy"
    result["isPublic"] = True
    result["isLocked"] = True

    return result


def load_active_text(soup):
    text_entry = soup.select("text[active=1]")[0]
    content = text_entry.find("content").get_text()
    content = BeautifulSoup(content, "lxml")

    for node in content.select("code a"):
        node.parent.unwrap()

    return text_entry["id"], html2text(str(content))


def load_additional_files(exercise_folder, text_id):
    path = Path(exercise_folder) / "texts" / text_id
    return list(path.glob("*"))


def replace_file_references(text, url_map):
    """
    >>> replace_file_references("[link]($DIR/foo.zip)", {"foo.zip": "https://my.web.com/archive.zip"})
    '[link](https://my.web.com/archive.zip)'
    >>> replace_file_references("![kitten]($DIR/foo.jpg)", {"foo.jpg": "https://my.web.com/image.jpg"})
    '![kitten](https://my.web.com/image.jpg)'
    >>> replace_file_references("(see ![kitten]($DIR/foo.jpg))", {"foo.jpg": "https://my.web.com/image.jpg"})
    '(see ![kitten](https://my.web.com/image.jpg))'
    """

    def replace(match):
        filename = match.group(1)
        return "({})".format(url_map.get(filename, ""))

    return re.sub(r'\(\$DIR/(.*?)\)', replace, text)


def load_reference_solution_details(content_soup, extension_to_runtime):
    for solution in content_soup.select("solution"):
        yield solution["id"], {
            "note": solution.find("comment").get_text(),
            "runtimeEnvironmentId": extension_to_runtime[solution.find("extension").get_text()]
        }


def load_reference_solution_file(solution_id, content_soup, exercise_folder):
    extension = content_soup.select("solution[id={}] extension".format(solution_id))[0].get_text()
    return Path(exercise_folder) / "solutions" / solution_id / "source.{}".format(extension)


def load_exercise_files(exercise_folder):
    path = Path(exercise_folder) / "testdata"
    for file_node in path.iterdir():
        if file_node.name == "config" or (file_node.is_dir() and file_node.name == "attic"):
            continue
        if file_node.suffix in (".in", ".out") and file_node.is_dir():
            for child in file_node.iterdir():
                yield "{}.{}".format(file_node.stem, child.name), child
        else:
            yield file_node.name, file_node


def load_allowed_extensions(content_soup):
    for item in content_soup.select("extensions item"):
        yield item.get_text()


def get_custom_judges(tests):
    for test in tests:
        if test.has_custom_judge:
            yield test.custom_judge_binary


def make_exercise_config(config, content_soup, exercise_files, pipelines, tests, test_id_map):
    exercise_config = []

    input_files = [name for name in exercise_files if name.endswith(".in")]

    for extension in load_allowed_extensions(content_soup):
        environment = config.extension_to_runtime[extension]
        env_tests = []

        for test in tests:
            build_pipeline = None
            for pipeline in pipelines:
                params_match = pipeline["parameters"]["isCompilationPipeline"]
                env_matches = environment in pipeline["runtimeEnvironmentIds"]

                if params_match and env_matches:
                    build_pipeline = pipeline["id"]
                    break

            if build_pipeline is None:
                logging.error("No build pipeline found for test %d", int(test.number))
                break

            input_stdio = test.in_type == "stdio"
            output_stdio = test.out_type == "stdio"
            exec_parameter = "producesStdout" if output_stdio else "producesFiles"

            exec_pipeline = None
            for pipeline in pipelines:
                params_match = pipeline["parameters"]["isExecutionPipeline"] and pipeline["parameters"][exec_parameter]
                env_matches = environment in pipeline["runtimeEnvironmentIds"]

                if params_match and env_matches:
                    exec_pipeline = pipeline["id"]
                    break

            if exec_pipeline is None:
                logging.error("No execution pipeline found for test %d", test.number)
                break

            if not input_stdio:
                test_inputs = [name for name in input_files if name.startswith("{}.".format(test.number))]
                test_input_names = [test.in_file] if test.in_type == "file" else [name[name.index(".") + 1 : ] for name in test_inputs]
            else:
                test_inputs = ["{}.in".format(test.number)]
                test_input_names = ["{}.in".format(test.number)]

            variables = [{
                "name": "stdin-file",
                "type": "remote-file",
                "value": test_inputs[0] if test_inputs else ""
            }, {
                "name": "input-files",
                "type": "remote-file[]",
                "value": test_inputs
            }, {
                "name": "judge-type",
                "type": "string",
                "value": config.judges.get(test.judge, test.judge)
            }, {
                "name": "run-args",
                "type": "string[]",
                "value": convert_args(test)
            }, {
                "name": "stdin-file",
                "type": "remote-file",
                "value": test_inputs[0] if input_stdio else ""
            }, ]

            if "$TDIR/$TEST.ok" in test.judge_args:
                variables.append({
                    "name": "expected-output",
                    "type": "remote-file",
                    "value": "{}.out".format(test.number)
                })
            else:  # Test uses a custom judge that does not need an example output
                variables.append({
                    "name": "expected-output",
                    "type": "remote-file",
                    "value": "{}.in".format(test.number)
                })

            if test.has_custom_judge:
                custom_judge = Path(test.custom_judge_binary).name
                custom_judge_args = test.custom_judge_args[:-2]  # TODO temporary solution - removes $PDIR/$TEST.in $TDIR/$TEST.out from the end
                judge_type = ""

            else:
                custom_judge = ""
                custom_judge_args = ""
                judge_type = config.judges.get(test.judge, test.judge)

            variables.append({
                "name": "custom-judge",
                "type": "remote-file",
                "value": custom_judge
            })

            variables.append({
                "name": "judge-args",
                "type": "string[]",
                "value": custom_judge_args
            })

            variables.append({
                "name": "judge-type",
                "type": "string",
                "value": judge_type
            })

            variables.append({
                "name": "run-args",
                "type": "string[]",
                "value": convert_args(test)
            })

            variables.append({
                "name": "actual-inputs",
                "type": "file[]",
                "value": test_input_names
            })

            if not output_stdio:
                variables.append({
                    "name": "actual-output",
                    "type": "file",
                    "value": test.out_file or "{}.actual.out".format(test.number)
                })

            env_tests.append({
                "name": test_id_map[test.name],
                "pipelines": [
                    {
                        "name": build_pipeline,
                        "variables": [{
                            "name": "extra-files",
                            "type": "remote-file[]",
                            "value": []
                        }, {
                            "name": "extra-file-names",
                            "type": "file[]",
                            "value": []
                        }]
                    },
                    {
                        "name": exec_pipeline,
                        "variables": variables
                    }
                ]
            })

        exercise_config.append({
            "name": environment,
            "tests": env_tests
        })

    return exercise_config


def upload_file(api, path, filename=None):
    filename = filename or path.name
    logging.info("Uploading {}".format(filename) if filename is None else "Uploading {} as {}".format(path.name, filename))

    payload = api.upload_file(filename, path.open("rb"))

    logging.info("Uploaded with id %s", payload["id"])

    return payload


def convert_args(test):
    if "./$PROBLEM" not in test.cmd_args:
        return []

    program_index = test.cmd_args.index("./$PROBLEM")
    return test.cmd_args[program_index + 1 :]
