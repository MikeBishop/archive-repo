from behave import *
import subprocess
import os
import json
import time

@given('a repo for "{repo}"')
def step_impl(context, repo):
    repo_dir = context.tempdir.name + "/repo"
    if not os.path.exists(repo_dir):
        checkout = subprocess.run(
            ["git", "clone", "https://github.com/" + repo, repo_dir]
        )
        checkout.check_returncode()
    context.repo_dir = repo_dir


@given('the output of the last tagged version for "{repo}"')
def step_impl(context, repo):
    filename = context.tempdir.name + "/known_good.json"

    if not os.path.exists(filename):
        get_tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True
        )
        get_tag.check_returncode()

        last_version = subprocess.run(
            ["git", "show", get_tag.stdout.strip() + ":archive.py"],
            capture_output=True,
            text=True,
        )
        last_version.check_returncode()

        last_version_run = subprocess.run(
            ["python3", "-", repo, os.environ["GH_TOKEN"], filename],
            input=last_version.stdout,
            text=True,
        )
        last_version_run.check_returncode()


@when('the current script is called on "{repo}"')
def step_impl(context, repo):
    filename = context.tempdir.name + "/current.json"
    if not os.path.exists(filename):
        this_version_run = subprocess.run(
            ["python3", "-m", "archive-repo", "archive", repo, os.environ["GH_TOKEN"], filename]
        )
        this_version_run.check_returncode()


@when('pr-branches is executed for "{repo}"')
def step_impl(context, repo):
    filename = context.tempdir.name + "/current.json"
    pr_branches_run = subprocess.run(
        ["python3", "-m", "archive-repo", "pr_branches", filename, repo, context.repo_dir]
    )
    pr_branches_run.check_returncode()


def read_temp_file(context, name):
    filename = context.tempdir.name + "/" + name + ".json"
    with open(filename) as read:
        return json.load(read)


@then("the output is a superset of the last version")
def step_impl(context):
    # Everything found in known_good must also appear current_result, except:
    # - Timestamp will change
    # - Magic may differ
    assert check_subset(
        read_temp_file(context, "known_good"),
        read_temp_file(context, "current"),
        exclude=["magic", "timestamp"],
    )


# Checks that everything in first occurs in second, except for the top-level keys in exclude
# If require_equal is set, everything in second also occurs in first.
def check_subset(first, second, exclude=[], mutual=False):
    if type(first) != type(second):
        return False

    elif isinstance(first, dict):
        if mutual and not check_subset(second.keys(), first.keys(), mutual=mutual):
            return False

        return all(
            key in second and check_subset(first[key], second[key], mutual=mutual)
            for key in first.keys()
            if key not in exclude
        )

    elif isinstance(first, list):
        if mutual and len(second) != len(first):
            return False
        return len(first) <= len(second) and all(
            check_subset(first[i], second[i], mutual=mutual) for i in range(len(first))
        )

    else:
        return first == second


@given("the {ref_type} file is available")
def step_impl(context, ref_type):
    # These reference files are explicitly included
    if ref_type == "Stale":
        context.reference = "tests/content/h2c_stale.json"
    elif ref_type == "Legacy":
        context.reference = "tests/content/h2c_legacy.json"
    # These reference files are created
    elif ref_type == "Wrong repo":
        filename = context.tempdir.name + "/quic.json"
        os.system(
            "sed 's/MikeBishop\/http2-certs/quicwg\/base-drafts/' tests/content/h2c_stale.json > "
            + filename
        )
        context.reference = filename
    elif ref_type == "Invalid magic":
        filename = context.tempdir.name + "/oogabooga.json"
        os.system(
            "sed 's/B8n2c@e8kvfx/00gaB00GA!/' tests/content/h2c_legacy.json > "
            + filename
        )
        context.reference = filename


@when('the script is called on "{repo}" with the reference file')
def step_impl(context, repo):
    context.execute_steps('When the current script is called on "' + repo + '"')
    assert os.path.exists(context.reference)
    run_with_ref = subprocess.run(
        [
            "python3",
            "-m",
            "archive-repo",
            "archive",
            repo,
            os.environ["GH_TOKEN"],
            "--reference",
            context.reference,
        ],
        capture_output=True,
        text=True,
    )
    run_with_ref.check_returncode()

    context.result = json.loads(run_with_ref.stdout)
    context.output = run_with_ref.stderr


@then("the output is the same")
def step_impl(context):
    assert check_subset(
        read_temp_file(context, "current"),
        context.result,
        exclude=["timestamp"],
        mutual=True,
    )


@then('the error "{error}" is found on stderr')
def step_impl(context, error):
    if error != "None":
        assert error in context.output


@then('a branch named "{branch}" pointing to "{hash}" is created')
def step_impl(context, branch, hash):
    git_commit = subprocess.run(
        ["git", "-C", context.repo_dir, "show-ref", "-s", "refs/heads/" + branch],
        capture_output=True,
        text=True,
    )
    git_commit.check_returncode()
    assert hash in git_commit.stdout
