"""
Houses options for invocation of a Github remote repo
on a Github hosted runner, in addition for the change_trigger_event construction
"""

import click

from opendapi.adapters.git import (
    ChangeTriggerEvent,
    get_commit_timestamp_str,
    get_merge_base,
)
from opendapi.cli.common import get_root_dir_validated
from opendapi.utils import read_yaml_or_json


def construct_change_trigger_event(kwargs: dict) -> ChangeTriggerEvent:
    """
    Construct the ChangeTriggerEvent given that this a Github remote repo
    on a Github hosted runner
    """
    github_event_name = kwargs["github_event_name"]
    github_event_path = kwargs["github_event_path"]
    github_event = read_yaml_or_json(github_event_path)

    after_change_sha = (
        github_event["after"]
        if github_event_name == "push"
        else github_event["pull_request"]["head"]["sha"]
    )
    base_branch_sha = (
        github_event["before"]
        if github_event_name == "push"
        else github_event["pull_request"]["base"]["sha"]
    )
    before_change_sha = get_merge_base(
        get_root_dir_validated(), after_change_sha, base_branch_sha
    )

    return ChangeTriggerEvent(
        where="github",
        event_type=github_event_name,
        repo_api_url=github_event["repository"]["url"],
        repo_html_url=github_event["repository"]["html_url"],
        repo_owner=github_event["repository"]["owner"]["login"],
        before_change_sha=before_change_sha,
        after_change_sha=after_change_sha,
        after_change_sha_timestamp=get_commit_timestamp_str(
            get_root_dir_validated(), after_change_sha
        ),
        git_ref=(
            github_event["ref"]
            if github_event_name == "push"
            else github_event["pull_request"]["head"]["ref"]
        ),
        pull_request_number=(
            github_event["pull_request"]["number"]
            if github_event_name == "pull_request"
            else None
        ),
        workspace=kwargs["github_workspace"],
        head_sha=kwargs.get("github_head_sha") or None,
        repository=kwargs["github_repository"],
        repo_full_name=github_event["repository"]["full_name"],
        pull_request_link=(
            github_event["pull_request"]["html_url"]
            if github_event_name == "pull_request"
            else None
        ),
        original_pr_author=(
            github_event["pull_request"].get("user", {}).get("login")
            if github_event_name == "pull_request"
            else None
        ),
    )


def runner_options(func: click.core.Command) -> click.core.Command:
    """
    Common options for a Github hosted runner
    """
    options = [
        click.option(
            "--github-event-name",
            type=click.Choice(
                ["push", "pull_request", "schedule", "workflow_dispatch"],
                case_sensitive=True,
            ),
            envvar="GITHUB_EVENT_NAME",
            show_envvar=False,
            required=True,
        ),
        click.option(
            "--github-run-attempt",
            envvar="GITHUB_RUN_ATTEMPT",
            show_envvar=False,
            type=int,
            required=True,
        ),
        click.option(
            "--github-run-id",
            envvar="GITHUB_RUN_ID",
            show_envvar=False,
            type=int,
        ),
        click.option(
            "--github-run-number",
            envvar="GITHUB_RUN_NUMBER",
            show_envvar=False,
            type=int,
        ),
        click.option(
            "--github-head-sha",
            envvar="GITHUB_HEAD_SHA",
            show_envvar=False,
        ),
        click.option(
            "--github-repository",
            envvar="GITHUB_REPOSITORY",
            show_envvar=False,
        ),
        click.option(
            "--github-workspace",
            envvar="GITHUB_WORKSPACE",
            show_envvar=False,
        ),
        click.option(
            "--github-step-summary",
            envvar="GITHUB_STEP_SUMMARY",
            show_envvar=False,
        ),
        click.option(
            "--github-event-path",
            envvar="GITHUB_EVENT_PATH",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func
