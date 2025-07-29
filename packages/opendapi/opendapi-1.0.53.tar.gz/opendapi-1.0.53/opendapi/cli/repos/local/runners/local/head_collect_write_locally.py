"""
CLI for collecting dapi file information at the current state,
loading the base collected dapi file information,
and then writing the apppropriate final dapis
to the local directory, when invoked locally:
`opendapi local local head-collect-write-locally`
"""

# pylint: disable=duplicate-code

import click

from opendapi.cli.common import get_opendapi_config_from_root
from opendapi.cli.context_agnostic import (
    collect_collected_files,
    load_collected_files,
    minimal_schemas_for_generate,
    write_locally,
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
def cli(**kwargs):
    """
        CLI for collecting dapi file information at the current state,
    loading the base collected dapi file information,
    and then writing the apppropriate final dapis
    to the local directory: `opendapi local local head-collect-write-locally`
    """
    runtime_skip_generation_at_head = kwargs[
        SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION_OPTION.name
    ]

    dbt_skip_generation_at_head = kwargs[
        SKIP_DBT_INTEGRATION_HEAD_GENERATION_OPTION.name
    ]

    opendapi_config = get_opendapi_config_from_root(
        local_spec_path=kwargs.get("local_spec_path"),
        validate_config=True,
    )
    runtime = opendapi_config.assert_single_runtime()

    head_collected_files = collect_collected_files(
        opendapi_config,
        change_trigger_event=construct_change_trigger_event(kwargs),
        commit_type=CommitType.CURRENT,
        runtime_skip_generation=runtime_skip_generation_at_head,
        dbt_skip_generation=dbt_skip_generation_at_head,
        minimal_schemas=minimal_schemas_for_generate(kwargs),
        runtime=runtime,
    )
    base_collected_files = load_collected_files(
        opendapi_config,
        CommitType.BASE,
        runtime,
    )

    write_locally(
        opendapi_config,
        head_collected_files,
        base_collected_files,
        kwargs,
    )
