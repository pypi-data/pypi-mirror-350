from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import aiohttp
    import aiolimiter

from . import github_endpoints
from . import github_cache


async def async_get_github_data(
    refs: dict[str, str] | list[dict[str, str]],
    datatype: str,
    github_token: str | None = None,
    load_from_cache: bool = True,
    save_to_cache: bool = True,
    ratelimit: float | None = None,
    max_open_files: int | None = None,
    preburst: bool | None = None,
    params: dict[str, str] | None = None,
) -> list[dict[str, typing.Any] | list[dict[str, typing.Any]] | None]:
    import asyncio
    import aiohttp

    if isinstance(refs, dict):
        refs = [refs]

    if github_token is None:
        github_token = _get_github_token()

    # get ratelimiter (preburst necessary due to aiolimiter idiosyncrasies)
    ratelimiter = _get_github_ratelimiter(
        ratelimit=ratelimit, token=github_token
    )

    if preburst is None:
        preburst = len(refs) > ratelimiter.max_rate
    if preburst:
        await _preburst_ratelimit(ratelimiter)
    if max_open_files is None:
        max_open_files = 1000
    file_semaphore = asyncio.Semaphore(max_open_files)
    async with aiohttp.ClientSession() as session:
        coroutines = []
        for ref in refs:
            if load_from_cache and github_cache.has_local_github_data(
                ref=ref, datatype=datatype
            ):
                coroutine = github_cache._async_load_local_github_data(
                    ref=ref,
                    datatype=datatype,
                    semaphore=file_semaphore,
                )
            else:
                coroutine = _async_github_request(
                    ref=ref,
                    datatype=datatype,
                    session=session,
                    github_token=github_token,
                    save_to_cache=save_to_cache,
                    ratelimiter=ratelimiter,
                    params=params,
                )
            coroutines.append(coroutine)
        return await asyncio.gather(*coroutines)


_warnings = {'github_token_default': False}


def _get_github_token() -> str | None:
    import os

    if not _warnings['github_token_default']:
        print(
            'no value set for GITHUB_TOKEN, specify 1) env variable or 2) github_token keyword argument, otherwise ratelimit will be much lower'  # noqa: E501
        )
    _warnings['github_token_default'] = True

    return os.environ.get('GITHUB_TOKEN')


_ratelimiters: dict[
    tuple[str, int | float | None], aiolimiter.AsyncLimiter
] = {}


def _get_github_ratelimiter(
    token: str | None = None,
    ratelimit: int | float | None = None,
) -> aiolimiter.AsyncLimiter:
    import aiolimiter

    if token is None:
        if ratelimit is None:
            ratelimiter: aiolimiter.AsyncLimiter | None
            ratelimiter = aiolimiter.AsyncLimiter(60, 3600)
        else:
            ratelimiter = aiolimiter.AsyncLimiter(ratelimit, 1)
    else:
        ratelimiter = _ratelimiters.get((token, ratelimit))
        if ratelimiter is None:
            ratelimiter = aiolimiter.AsyncLimiter(4400, 3600)
            _ratelimiters[(token, ratelimit)] = ratelimiter

    return ratelimiter


async def _preburst_ratelimit(ratelimiter: aiolimiter.AsyncLimiter) -> None:
    for i in range(int(ratelimiter.max_rate)):
        async with ratelimiter:
            pass


async def _async_github_request(
    ref: dict[str, str],
    datatype: str,
    session: aiohttp.ClientSession,
    save_to_cache: bool,
    ratelimiter: aiolimiter.AsyncLimiter,
    github_token: str | None = None,
    params: dict[str, str] | None = None,
    max_retries: int = 3,
) -> dict[str, typing.Any] | list[dict[str, typing.Any]] | None:
    import aiohttp

    url = github_endpoints.get_endpoint_url(datatype).format(**ref)
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if github_token is not None:
        headers['Authorization'] = 'token ' + github_token

    # perform request
    for retry in range(max_retries):
        async with ratelimiter:
            try:
                async with session.get(
                    url, headers=headers, params=params
                ) as response:
                    should_retry, result = await _handle_response(
                        response, ref, retry, datatype
                    )
            except aiohttp.ServerDisconnectedError:
                continue
        if not should_retry:
            break
    else:
        raise Exception(
            'failed request for '
            + str(ref)
            + ' after '
            + str(max_retries)
            + ' retries'
        )

    # save to cache
    if save_to_cache:
        await github_cache._async_save_local_github_data(
            data=result, ref=ref, datatype=datatype
        )

    return result


async def _handle_response(
    response: aiohttp.ClientResponse,
    ref: dict[str, str],
    retry: int,
    datatype: str,
) -> tuple[bool, dict[str, typing.Any] | list[dict[str, typing.Any]] | None]:
    import asyncio

    if response.status == 200:
        result: dict[str, typing.Any] | None = await response.json()
        return False, result
    elif (
        response.status == 403
        and response.headers['X-RateLimit-Remaining'] == '0'
    ):
        import datetime

        timestamp = datetime.datetime.fromtimestamp(
            int(response.headers['X-RateLimit-Reset'])
        )
        wait = timestamp - datetime.datetime.now()
        minutes, seconds = divmod(wait.seconds, 60)
        msg = (
            'rate limit exceeded, wait',
            minutes,
            'minutes and',
            seconds,
            'seconds until',
            timestamp,
        )
        raise Exception(' '.join(str(item) for item in msg))
    elif (
        response.status == 403
        and (await response.json())['message'] == 'Repository access blocked'
    ):
        return False, None
    elif response.status in [404, 451]:
        return False, None
    elif response.status == 409:
        if (
            datatype == 'commits'
            and (await response.json())['message'] == 'Git Repository is empty.'
        ):
            return False, []
        else:
            await asyncio.sleep(4 ** (retry + 1))
            return True, None
    elif response.status in [500, 502, 503, 504]:
        await asyncio.sleep(4 ** (retry + 1))
        return True, None
    else:
        raise Exception(
            'HTTP error for '
            + str(ref)
            + ', '
            + str(response.status)
            + ': '
            + str(await response.text())
        )
