from __future__ import annotations

import typing

from . import github_requests
from .. import references

if typing.TYPE_CHECKING:
    from typing_extensions import Unpack

    class GithubRequestParams(typing.TypedDict):
        github_token: str | None
        load_from_cache: bool
        save_to_cache: bool
        ratelimit: float | None
        max_open_files: int | None
        preburst: bool | None


async def async_get_github_repos_metadata(
    repos: str | list[str],
    **github_request_params: Unpack[GithubRequestParams],
) -> list[dict[str, typing.Any] | None]:
    if isinstance(repos, str):
        repos = [repos]
    return await github_requests.async_get_github_data(  # type: ignore
        [references.parse_repo_reference(ref) for ref in repos],
        datatype='repo',
        **github_request_params,
    )


async def async_get_github_commits(
    repos: str | list[str],
    n_commits: int = 100,
    **github_request_params: Unpack[GithubRequestParams],
) -> list[list[dict[str, typing.Any]] | None]:
    if isinstance(repos, str):
        repos = [repos]
    return await github_requests.async_get_github_data(  # type: ignore
        [references.parse_repo_reference(ref) for ref in repos],
        datatype='commits',
        params={'per_page': str(n_commits)},
        **github_request_params,
    )


async def async_get_github_users_metadata(
    usernames: str | list[str],
    **github_request_params: Unpack[GithubRequestParams],
) -> list[dict[str, typing.Any] | None]:
    if isinstance(usernames, str):
        usernames = [usernames]
    return await github_requests.async_get_github_data(  # type: ignore
        [{'username': value} for value in usernames],
        datatype='user',
        **github_request_params,
    )
