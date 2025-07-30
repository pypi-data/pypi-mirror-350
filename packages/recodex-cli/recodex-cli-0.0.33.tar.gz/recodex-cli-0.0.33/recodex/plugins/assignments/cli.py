import click
import sys
import os
import datetime
import json
from ruamel.yaml import YAML

from recodex.api import ApiClient
from recodex.decorators import pass_api_client
from recodex.utils import asciiize_string


def safe_get_solution_points(solution):
    submission = solution["lastSubmission"]
    if submission is None:
        return -1
    evaluation = submission["evaluation"]
    if evaluation is None:
        return -1
    return evaluation["points"] + solution["bonusPoints"]


def getAssignmentName(assignment):
    if "localizedTexts" not in assignment or len(assignment["localizedTexts"]) == 0:
        # There is no "localizedTexts" key or empty array :(
        return "unknown"
    known_languages = ("en", "cs")
    # Try known languages (in given order)
    for lang in known_languages:
        for item in assignment["localizedTexts"]:
            if item["locale"] == lang:
                return item["name"]
    # Something weird happened, return first name we got
    return assignment["localizedTexts"][0]["name"]


@click.group()
def cli():
    """
    Tools for working with assignments (exercise instances)
    """


@cli.command()
@click.option("download_dir", "-d")
@click.argument("assignment_id")
@pass_api_client
def download_best_solutions(api: ApiClient, download_dir, assignment_id):
    """
    Download the best solution of this assignment from each user.
    """
    if download_dir is None:
        download_dir = "."
    if not os.path.exists(download_dir) or not os.path.isdir(download_dir):
        click.echo(
            "Download path '{}' must exist and must be a directory.".format(download_dir))
        return

    # Get assignment metadata and best solution for each student ...
    assignment = api.get_assignment(assignment_id)
    if assignment is None:
        click.echo("Assignment not found.")
        return
    click.echo("Downloading best solutions of '{}' to '{}' ...".format(
        getAssignmentName(assignment), download_dir))
    best_solutions = api.get_assignment_best_solutions(assignment_id)

    # Iterate over students
    for student in api.get_group_students(assignment["groupId"]):
        # Try to find best solution for the student
        best = best_solutions[student["id"]]
        if best:
            # File name comprise user name in plain ASCII and its ID for uniqueness
            file_name = "{}-{}-{}.zip".format(
                asciiize_string(student["name"]["lastName"]),
                asciiize_string(student["name"]["firstName"]), student["id"])
            points = safe_get_solution_points(best)
            created = datetime.datetime.fromtimestamp(
                best["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("Saving {} ... {} points, {}".format(
                file_name, points, created))
            api.download_solution(
                best['id'], "{}/{}".format(download_dir, file_name))


@cli.command()
@click.argument("assignment_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_solutions(api: ApiClient, assignment_id, useJson):
    """
    Get assignment solutions (including points, score, ...) of all users.
    """

    solutions = api.get_assignment_solutions(assignment_id)
    if useJson is True:
        json.dump(solutions, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml = YAML(typ="safe")
        yaml.dump(solutions, sys.stdout)
    else:
        for solution in solutions:
            flags = []
            if (solution["accepted"]):
                flags.append("accepted")
            if (solution["isBestSolution"]):
                flags.append("best")
            points = solution["overriddenPoints"] if solution["overriddenPoints"] else solution["actualPoints"]
            click.echo("{} {} {}+{}/{} {}".format(solution["id"], solution["authorId"],
                       points, solution["bonusPoints"], solution["maxPoints"], ", ".join(flags)))

@cli.command()
@click.argument("exercise_id")
@click.argument("group_id")
@pass_api_client
def create(api: ApiClient, exercise_id, group_id):
    """
    Creates an assignment of an exercise in specified group with default values.

    Use update subcommand to modify the values.
    """

    assignment = api.create_assignment(exercise_id, group_id)
    click.echo(assignment['id'])

@cli.command()
@click.argument("assignment_id")
@click.option("--publish", "publish", default=None, is_flag=False, flag_value=True, help="False or True or timestamp to be visible from")
@click.option("--deadline1", "deadline1", default=0, help="Timestamp of first deadline")
@click.option("--maxPoints1", "max_points1", default=0, help="Points limit before first deadline")
@click.option("--deadline2", "deadline2", default=0, help="Timestamp of second deadline")
@click.option("--maxPoints2", "max_points2", default=0, help="Points limit before second deadline")
@click.option("--interpolatePoints/--no-interpolatePoints", "interpolate_points", default=None, help="Whether to interpolate points between deadlines")
@click.option("--minPercent", "min_percent", default=0.0, help="Minimal solution correctness")
@click.option("--submissionsCount", "submissions_count", default=0, help="Maximal number of submissions")
@click.option("--solutionFiles", "solution_files", default=0, help="Maximal number of files in submission")
@click.option("--solutionSize", "solution_size", default=0, help="Maximal total size of all files submitted")
@click.option("--showLimitRatios/--no-showLimitRatios", "show_limit_ratios", default=None, help="Whether to show memory and time")
@click.option("--showLimitValues/--no-showLimitValues", "show_limit_values", default=None, help="Whether to show absolute measurements")
@click.option("--showJudgeStdout/--no-showJudgeStdout", "show_judge_stdout", default=None, help="Whether to show stdout from judge")
@click.option("--showJudgeStderr/--no-showJudgeStderr", "show_judge_stderr", default=None, help="Whether to show stderr from judge")
@click.option("--notify/--no-notify", "notify", default=None, help="Whether to send email notification once assignment is public")
@click.option("--bonus/--no-bonus", "is_bonus", default=None, help="Whether the assignment is bonus")
@click.option("--exam/--no-exam", "is_exam", default=None, help="Whether the assignment is exam")
@pass_api_client
def update(api: ApiClient, assignment_id, publish,
           deadline1, max_points1, deadline2, max_points2, interpolate_points, min_percent,
           submissions_count, solution_files, solution_size,
           show_limit_ratios, show_limit_values, show_judge_stdout, show_judge_stderr,
           notify, is_bonus, is_exam):
    """
    Updates settings of specified assignment. If the option is not provided the value is not updated.
    """

    def bool_or_argument(value, arg):
        return value if value is not None else arg

    assignment = api.get_assignment(assignment_id)

    if publish is None:
        is_public = assignment['isPublic']
        visible_from = assignment['visibleFrom']
    elif (lower := publish.lower()) in ['true', 'false']:
        is_public = lower == "true"
        visible_from = None
    else:
        is_public = True
        visible_from = int(publish)

    updates = {
        'version': assignment['version'],
        'isPublic': is_public,
        'localizedTexts': assignment['localizedTexts'],
        'firstDeadline': deadline1 or assignment['firstDeadline'],
        'maxPointsBeforeFirstDeadline': max_points1 or assignment['maxPointsBeforeFirstDeadline'],
        'submissionsCountLimit': submissions_count or assignment['submissionsCountLimit'],
        'solutionFilesLimit': solution_files or assignment['solutionFilesLimit'],
        'solutionSizeLimit': solution_size or assignment['solutionSizeLimit'],
        'allowSecondDeadline': bool(deadline2 or assignment['secondDeadline']),
        'visibleFrom': visible_from,
        'canViewLimitRatios': bool_or_argument(show_limit_ratios, assignment['canViewLimitRatios']),
        'canViewMeasuredValues': bool_or_argument(show_limit_values, assignment['canViewMeasuredValues']),
        'canViewJudgeStdout': bool_or_argument(show_judge_stdout, assignment['canViewJudgeStdout']),
        'canViewJudgeStderr': bool_or_argument(show_judge_stderr, assignment['canViewJudgeStderr']),
        'secondDeadline': deadline2 or assignment['secondDeadline'],
        'maxPointsBeforeSecondDeadline': max_points2 or assignment['maxPointsBeforeSecondDeadline'],
        'maxPointsDeadlineInterpolation': bool_or_argument(interpolate_points, assignment['maxPointsDeadlineInterpolation']),
        'isBonus': bool_or_argument(is_bonus, assignment['isBonus']),
        'pointsPercentualThreshold': min_percent or assignment['pointsPercentualThreshold'],
        'isExam': bool_or_argument(is_exam, assignment['isExam'])
    }

    if notify is not None:
        updates = updates | { 'sendNotification': notify }

    api.set_assignment(assignment['id'], **updates)
