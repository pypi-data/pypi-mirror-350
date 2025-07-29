"""
CLI for collecting dapi file information at the base commit and then persisting
it for later use, when invoked in a buildkite CI runner for a github repo for a specific runtime:
`opendapi github buildkite base-collect`
"""

# pylint: disable=duplicate-code

import click

from opendapi.cli.common import get_opendapi_config_from_root
from opendapi.cli.context_agnostic import (
    collect_collected_files,
    persist_collected_files,
    server_sync_minimal_schemas,
)
from opendapi.cli.options import (
    SKIP_DBT_INTEGRATION_BASE_GENERATION_OPTION,
    SKIP_RUNTIME_INTEGRATION_BASE_GENERATION_OPTION,
    dbt_options,
    dev_options,
    generation_options,
    opendapi_run_options,
    runtime_options,
)
from opendapi.cli.repos.github.options import repo_options
from opendapi.cli.repos.github.runners.buildkite.options import (
    construct_change_trigger_event,
    runner_options,
)
from opendapi.defs import CommitType


@click.command()
# common options
@dbt_options
@dev_options
@generation_options
@opendapi_run_options
@runtime_options
# github repo options
@repo_options
# github repo github runner options
@runner_options
def cli(**kwargs):
    """
    CLI for collecting dapi file information at the base commit and then persisting
    it for later use, when invoked in a buildkite CI runner for a github repo:
    `opendapi local local base-collect`
    """

    runtime_skip_generation_at_base = kwargs.get(
        SKIP_RUNTIME_INTEGRATION_BASE_GENERATION_OPTION.name, False
    )

    dbt_skip_generation_at_base = kwargs.get(
        SKIP_DBT_INTEGRATION_BASE_GENERATION_OPTION.name, True
    )

    runtime = kwargs["runtime"]
    change_trigger_event = construct_change_trigger_event(kwargs)
    opendapi_config = get_opendapi_config_from_root(
        local_spec_path=kwargs.get("local_spec_path"),
        validate_config=True,
    )
    opendapi_config.assert_runtime_exists(runtime)
    collected_files = collect_collected_files(
        opendapi_config,
        change_trigger_event=change_trigger_event,
        commit_type=CommitType.BASE,
        runtime_skip_generation=runtime_skip_generation_at_base,
        dbt_skip_generation=dbt_skip_generation_at_base,
        minimal_schemas=server_sync_minimal_schemas(),
        runtime=runtime,
    )
    persist_collected_files(
        collected_files,
        opendapi_config,
        commit_type=CommitType.BASE,
        runtime=runtime,
    )
