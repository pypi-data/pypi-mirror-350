from __future__ import annotations

import typing

from . import github_getters
from . import github_endpoints

if typing.TYPE_CHECKING:
    from typing_extensions import Unpack
    import polars as pl

    Entry = dict[str, typing.Any]
    EntryList = list[typing.Union[Entry, None]]
    EntryListList = list[list[Entry]]


def _result_to_dataframe(
    result: EntryList | EntryListList,
    schema: dict[str, pl.Datatype],
    nested: bool = False,
) -> pl.DataFrame:
    import polars as pl

    result = [value for value in result if value is not None]  # type: ignore
    if nested:
        result = [item for subresult in result for item in subresult]  # type: ignore
    timestamp_columns = [
        pl.col(name).str.to_datetime().cast(pl.Datetime('ms'))
        for name, dtype in schema.items()
        if dtype == pl.Datetime('ms')
    ]
    return pl.DataFrame(result).with_columns(*timestamp_columns)


async def async_collect_github_users(
    usernames: str | list[str],
    **github_request_params: Unpack[github_getters.GithubRequestParams],
) -> pl.DataFrame:
    result = await github_getters.async_get_github_users_metadata(
        usernames=usernames, **github_request_params
    )
    return _result_to_dataframe(
        result, github_endpoints.get_endpoint_schema('user')
    )


async def async_collect_github_repos(
    repos: str | list[str],
    **github_request_params: Unpack[github_getters.GithubRequestParams],
) -> pl.DataFrame:
    result = await github_getters.async_get_github_repos_metadata(
        repos=repos, **github_request_params
    )
    return _result_to_dataframe(
        result, github_endpoints.get_endpoint_schema('repo')
    )


async def async_collect_github_commits(
    repos: str | list[str],
    **github_request_params: Unpack[github_getters.GithubRequestParams],
) -> pl.DataFrame:
    result = await github_getters.async_get_github_commits(
        repos=repos, **github_request_params
    )
    return _result_to_dataframe(
        result,  # type: ignore
        github_endpoints.get_endpoint_schema('commits'),
        nested=True,
    )
