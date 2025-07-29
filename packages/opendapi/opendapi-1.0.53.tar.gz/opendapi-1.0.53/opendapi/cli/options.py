"""Shared options used by OpenDAPI CLI."""

import functools
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar

import click

from opendapi.adapters.dapi_server import DAPIServerConfig
from opendapi.utils import decode_base64_to_json, encode_json_to_base64

S = TypeVar("S")
T = TypeVar("T")


def construct_dapi_server_config(kwargs: dict) -> DAPIServerConfig:
    """Construct the DAPI server configuration from the CLI arguments."""
    return DAPIServerConfig(
        server_host=kwargs["dapi_server_host"],
        api_key=kwargs["dapi_server_api_key"],
        mainline_branch_name=kwargs["mainline_branch_name"],
        register_on_merge_to_mainline=kwargs["register_on_merge_to_mainline"],
        suggest_changes=kwargs["suggest_changes"],
        enrich_batch_size=kwargs["enrich_batch_size"],
        ignore_suggestions_cache=kwargs["ignore_suggestions_cache"],
        register_batch_size=kwargs["register_batch_size"],
        analyze_impact_batch_size=kwargs["analyze_impact_batch_size"],
        pr_sync_batch_size=kwargs["pr_sync_batch_size"],
        revalidate_all_files=kwargs["revalidate_all_files"],
        require_committed_changes=kwargs["require_committed_changes"],
        woven_integration_mode=kwargs["woven_integration_mode"],
        woven_configuration=kwargs["woven_configuration"],
        feature_validate_dapi_batch_size=kwargs["feature_validate_dapi_batch_size"],
        server_sync_batch_size=kwargs["server_sync_batch_size"],
        base_generated_dbt_fallback_batch_size=kwargs[
            "base_generated_dbt_fallback_batch_size"
        ],
        s3_persist_threadpool_size=kwargs["s3_persist_threadpool_size"],
    )


def _load_base64_json(
    ctx: click.Context,  # pylint: disable=unused-argument
    param: click.Option,  # pylint: disable=unused-argument
    value: Optional[str],
) -> Optional[dict]:
    """Decode a base64 encoded JSON string."""
    return None if value is None else decode_base64_to_json(value)


def _safe_encode_base64_json(value: Optional[dict]) -> str:
    """Encode a JSON object to a base64 string."""
    return encode_json_to_base64(value)


@dataclass
class ParamNameWithOption:
    """Dataclass to hold the name and option for a parameter."""

    option: Callable[[Callable], click.Option]
    convert_to_argument: Callable[[S], T] = lambda x: x

    @functools.cached_property
    def __click_params(self):
        """Get thewrapped click params"""
        return self.option(lambda: True).__click_params__[0]

    @property
    def name(self) -> str:
        """Get the name of the parameter from the option."""
        return self.__click_params.name

    @property
    def envvar(self) -> str:
        """Get the environment variable name of the parameter from the option."""
        return self.__click_params.envvar

    @property
    def callback(self) -> Optional[Callable[[click.Context, click.Option, T], S]]:
        """Return the callback of the option if applicable"""
        return self.__click_params.callback  # pragma: no cover

    def extract_from_kwargs(self, kwargs: dict) -> Optional[Any]:
        """Extract the value from the kwargs."""
        return kwargs.get(self.name)

    def set_as_envvar_if_none(self, kwargs: dict, value: S):
        """Set the value as an environment variable if it does not exist in kwargs."""
        if kwargs.get(self.name) is None:
            os.environ[self.envvar] = self.convert_to_argument(value)


TEAMS_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--teams-minimal-schema",
        envvar="TEAMS_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton teams file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

DATASTORES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--datastores-minimal-schema",
        envvar="DATASTORES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton datastores file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

PURPOSES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--purposes-minimal-schema",
        envvar="PURPOSES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton purposes file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

DAPI_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--dapi-minimal-schema",
        envvar="DAPI_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton dapi files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

SUBJECTS_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--subjects-minimal-schema",
        envvar="SUBJECTS_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton subject files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

CATEGORIES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--categories-minimal-schema",
        envvar="CATEGORIES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton categories files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)


def minimal_schema_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the minimal schema."""
    for option in (
        CATEGORIES_PARAM_NAME_WITH_OPTION.option,
        DAPI_PARAM_NAME_WITH_OPTION.option,
        DATASTORES_PARAM_NAME_WITH_OPTION.option,
        PURPOSES_PARAM_NAME_WITH_OPTION.option,
        SUBJECTS_PARAM_NAME_WITH_OPTION.option,
        TEAMS_PARAM_NAME_WITH_OPTION.option,
        click.option(
            "--skip-server-minimal-schemas",
            envvar="SKIP_SERVER_MINIMAL_SCHEMAS",
            show_envvar=True,
            is_flag=True,
            default=False,
            help="Do not require minimal schemas for the DAPI files",
        ),
    ):
        func = option(func)
    return func


def features_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for features."""
    for option in (
        click.option(
            "--feature-to-status",
            envvar="FEATURE_TO_STATUS",
            show_envvar=True,
            default=None,
            help="Base64 encoded JSON of features to their status",
            callback=_load_base64_json,
        ),
    ):
        func = option(func)
    return func


def dev_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for most commands."""
    options = [
        click.option(
            "--local-spec-path",
            default=None,
            envvar="LOCAL_SPEC_PATH",
            help="Use specs in the local path instead of the DAPI server",
            show_envvar=False,
        ),
        click.option(
            "--always-write-generated-dapis",
            is_flag=True,
            default=False,
            envvar="ALWAYS_WRITE_GENERATED_DAPIS",
            help="Write the generated dapis even if they have not changed",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def dapi_server_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the dapi server commands."""
    options = [
        click.option(
            "--dapi-server-host",
            envvar="DAPI_SERVER_HOST",
            show_envvar=True,
            default="https://api.wovencollab.com",
            help="The host of the DAPI server",
        ),
        click.option(
            "--dapi-server-api-key",
            envvar="DAPI_SERVER_API_KEY",
            show_envvar=True,
            help="The API key for the DAPI server",
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--base-commit-sha",
        envvar="BASE_COMMIT_SHA",
        show_envvar=True,
        default=None,
        help="The SHA of the base commit",
    )
)

HEAD_COMMIT_SHA_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--head-commit-sha",
        envvar="HEAD_COMMIT_SHA",
        show_envvar=True,
        default=None,
        help="The SHA of the head commit",
    )
)


def git_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the git commands."""
    for option in (
        BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION.option,
        HEAD_COMMIT_SHA_PARAM_NAME_WITH_OPTION.option,
    ):
        func = option(func)
    return func


def opendapi_run_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the client commands for debugging."""
    options = [
        click.option(
            "--mainline-branch-name",
            default="main",
            envvar="MAINLINE_BRANCH_NAME",
            show_envvar=True,
            help="The name of the mainline branch to compare against",
        ),
        click.option(
            "--enrich-batch-size",
            default=5,
            envvar="ENRICH_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--register-batch-size",
            default=30,
            envvar="REGISTER_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--analyze-impact-batch-size",
            default=15,
            envvar="ANALYZE_IMPACT_BATCH_SIZE",
            help="Batch size for analyzing impact of DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--pr-sync-batch-size",
            default=5,
            envvar="PR_SYNC_BATCH_SIZE",
            help="Batch size for syncing PR and DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--feature-validate-dapi-batch-size",
            default=5,
            envvar="FEATURE_VALIDATE_DAPI_BATCH_SIZE",
            help="Batch size for validating DAPI files for features",
            show_envvar=False,
        ),
        click.option(
            "--server-sync-batch-size",
            default=15,
            envvar="SERVER_SYNC_BATCH_SIZE",
            help="Batch size for syncing opendapi information with the server",
            show_envvar=False,
        ),
        click.option(
            "--base-generated-dbt-fallback-batch-size",
            default=5,
            envvar="BASE_GENERATED_DBT_FALLBACK_BATCH_SIZE",
            help="Batch size for fetching generated dapis for the base commit for dbt",
            show_envvar=False,
        ),
        click.option(
            "--s3-persist-threadpool-size",
            default=8,
            envvar="S3_PERSIST_THREADPOOL_SIZE",
            help="Threadpool size for persisting DAPI files to S3",
            show_envvar=False,
        ),
        click.option(
            "--suggest-changes",
            is_flag=True,
            default=True,
            envvar="SUGGEST_CHANGES",
            show_envvar=True,
            help="Suggest changes to the DAPI files",
        ),
        click.option(
            "--revalidate-all-files",
            is_flag=True,
            default=False,
            envvar="REVALIDATE_ALL_FILES",
            help="Revalidate all files, not just the ones that have changed",
            show_envvar=True,
        ),
        click.option(
            "--require-committed-changes",
            is_flag=True,
            default=False,
            envvar="REQUIRE_COMMITTED_CHANGES",
            help="Do not Overwrite uncommitted DAPI files with server suggestions",
            show_envvar=True,
        ),
        click.option(
            "--ignore-suggestions-cache",
            is_flag=True,
            default=False,
            envvar="IGNORE_SUGGESTIONS_CACHE",
            help="Ignore suggestions cache and fetch fresh suggestions",
            show_envvar=False,
        ),
        click.option(
            "--register-on-merge-to-mainline",
            is_flag=True,
            default=True,
            envvar="REGISTER_ON_MERGE_TO_MAINLINE",
            help="Register DAPI files on merge to mainline branch",
            show_envvar=False,
        ),
        click.option(
            "--woven-integration-mode",
            type=click.Choice(["shadow", "active", "disabled"], case_sensitive=True),
            default="active",
            envvar="WOVEN_INTEGRATION_MODE",
            help="Woven Integration Mode",
            show_envvar=False,
        ),
        click.option(
            "--woven-configuration",
            type=click.Choice(["done", "in_progress"], case_sensitive=True),
            default="done",
            envvar="WOVEN_CONFIGURATION",
            help="Is Woven's configuration done or in progress",
            show_envvar=False,
        ),
        click.option(
            "--skip-client-config",
            is_flag=True,
            default=False,
            envvar="SKIP_CLIENT_CONFIG",
            help="Skip fetching client config from the server",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def cicd_param_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the CICD parameters."""
    options = [
        click.option(
            "--woven-cicd-id",
            envvar="WOVEN_CICD_ID",
            show_envvar=True,
            help="The Woven CICD ID",
            type=str,
            required=True,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def dbt_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the third-party integrations."""
    options = [
        click.option(
            "--dbt-cloud-url",
            envvar="DAPI_DBT_CLOUD_URL",
            show_envvar=True,
            help="The host of the dbt Cloud integration",
            default=None,
            type=str,
        ),
        click.option(
            "--dbt-cloud-api-key",
            envvar="DAPI_DBT_CLOUD_API_KEY",
            show_envvar=True,
            help="The API key for the dbt cloud integration",
        ),
        click.option(
            "--dbt-cloud-retry-count",
            envvar="DAPI_DBT_CLOUD_RETRY_COUNT",
            show_envvar=True,
            help="The retry count for dbt cloud integration",
        ),
        click.option(
            "--dbt-cloud-retry-interval",
            envvar="DAPI_DBT_CLOUD_RETRY_INTERVAL",
            show_envvar=True,
            help="The retry interval for dbt cloud integration",
        ),
        click.option(
            "--dapi-dbt-fast-fail",
            envvar="DAPI_DBT_FAST_FAIL",
            show_envvar=True,
            default=False,
            help="Fast fail if the opendapi dbt cloud job fails",
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


SKIP_RUNTIME_INTEGRATION_BASE_GENERATION_OPTION = ParamNameWithOption(
    option=click.option(
        "--skip-runtime-integration-base-generation",
        is_flag=True,
        envvar="SKIP_RUNTIME_INTEGRATION_BASE_GENERATION",
        help="Skip the generation step for runtime integrations at the base commit",
        show_envvar=False,
    ),
)

SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION_OPTION = ParamNameWithOption(
    option=click.option(
        "--skip-runtime-integration-head-generation",
        is_flag=True,
        envvar="SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION",
        help="Skip the generation step for runtime integrations at the head commit",
        show_envvar=False,
    ),
)

SKIP_DBT_INTEGRATION_BASE_GENERATION_OPTION = ParamNameWithOption(
    option=click.option(
        "--skip-dbt-integration-base-generation",
        is_flag=True,
        default=True,
        envvar="SKIP_DBT_INTEGRATION_BASE_GENERATION",
        help="Skip the generation step for dbt integrations at the base commit",
        show_envvar=False,
    ),
)

SKIP_DBT_INTEGRATION_HEAD_GENERATION_OPTION = ParamNameWithOption(
    option=click.option(
        "--skip-dbt-integration-head-generation",
        type=bool,
        # Since click is meant to decorate a (usually) explicitly-typed function,
        # all options must have a value - either from the user or default - to be able
        # to invoke the decorated function.
        # Therefore, if this default was False we would not be able to differentiate
        # between a user passing in False, or it being False due to the default,
        # and we need to know this since if it was not passed in we may use fallback logic
        # (i.e. in the DBT push case). We therefore make the default None.
        default=None,
        envvar="SKIP_DBT_INTEGRATION_HEAD_GENERATION",
        help="Skip the generation step for dbt integrations at the head commit",
        show_envvar=False,
        required=False,
    ),
    convert_to_argument=lambda x: str(x).lower(),
)


def generation_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the generation commands."""
    options = [
        SKIP_RUNTIME_INTEGRATION_BASE_GENERATION_OPTION.option,
        SKIP_RUNTIME_INTEGRATION_HEAD_GENERATION_OPTION.option,
        SKIP_DBT_INTEGRATION_BASE_GENERATION_OPTION.option,
        SKIP_DBT_INTEGRATION_HEAD_GENERATION_OPTION.option,
    ]
    for option in reversed(options):
        func = option(func)
    return func


def runtime_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for commands that deal with multiple runtimes"""
    options = [
        click.option(
            "--runtime",
            type=str,
            envvar="RUNTIME",
            help="The runtime to use for generation",
            show_envvar=False,
            required=True,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func
