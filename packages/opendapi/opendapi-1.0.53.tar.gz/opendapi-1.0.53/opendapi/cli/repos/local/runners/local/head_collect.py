"""
CLI for collecting dapi file information at the current state
and then persisting it for later use when invoked locally:
`opendapi local local head-collect`
"""

# pylint: disable=duplicate-code

import click

from opendapi.cli.common import get_opendapi_config_from_root
from opendapi.cli.context_agnostic import (
    collect_collected_files,
    minimal_schemas_for_generate,
    persist_collected_files,
)
from opendapi.cli.options import (
    SKIP_DBT_INTEGRATION_HEAD_GENERATION_OPTION,
    SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION_OPTION,
    dbt_options,
    dev_options,
    generation_options,
    git_options,
    minimal_schema_options,
    opendapi_run_options,
    runtime_options,
)
from opendapi.cli.repos.local.runners.local.options import (
    construct_change_trigger_event,
)
from opendapi.defs import CommitType


@click.command()
@minimal_schema_options
@dbt_options
@dev_options
@generation_options
@git_options
@opendapi_run_options
@runtime_options
def cli(**kwargs):
    """
    CLI for collecting dapi file information at the current state
    and then persisting it for later use: `opendapi local local head-collect`
    """

    runtime_skip_generation_at_head = kwargs[
        SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION_OPTION.name
    ]

    dbt_skip_generation_at_head = kwargs[
        SKIP_DBT_INTEGRATION_HEAD_GENERATION_OPTION.name
    ]

    runtime = kwargs["runtime"]
    opendapi_config = get_opendapi_config_from_root(
        local_spec_path=kwargs.get("local_spec_path"),
        validate_config=True,
    )
    opendapi_config.assert_runtime_exists(runtime)

    collected_files = collect_collected_files(
        opendapi_config,
        change_trigger_event=construct_change_trigger_event(kwargs),
        commit_type=CommitType.CURRENT,
        runtime_skip_generation=runtime_skip_generation_at_head,
        dbt_skip_generation=dbt_skip_generation_at_head,
        minimal_schemas=minimal_schemas_for_generate(kwargs),
        runtime=runtime,
    )
    persist_collected_files(
        collected_files,
        opendapi_config,
        commit_type=CommitType.CURRENT,
        runtime=runtime,
    )
