from __future__ import annotations

import typing

from . import github_endpoints

if typing.TYPE_CHECKING:
    import asyncio


def has_local_github_data(ref: dict[str, str], datatype: str) -> bool:
    import os

    return os.path.exists(get_local_github_path(ref=ref, datatype=datatype))


async def _async_load_local_github_data(
    ref: dict[str, str], datatype: str, semaphore: asyncio.Semaphore
) -> dict[str, typing.Any] | list[dict[str, typing.Any]] | None:
    import aiofiles  # type: ignore
    import json

    async with semaphore:
        path = get_local_github_path(ref=ref, datatype=datatype)
        async with aiofiles.open(path, 'r') as f:
            content = await f.read()
            return json.loads(content)  # type: ignore


async def _async_save_local_github_data(
    data: dict[str, typing.Any] | list[dict[str, typing.Any]] | None,
    ref: dict[str, str],
    datatype: str,
) -> None:
    import aiofiles
    import os
    import json

    path = get_local_github_path(ref=ref, datatype=datatype)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    async with aiofiles.open(path, 'w') as f:
        content = json.dumps(data)
        await f.write(content)


def get_local_github_path(ref: dict[str, str], datatype: str) -> str:
    from .. import cache

    path_keys = github_endpoints.get_endpoint_path_keys(datatype)
    data = [value.format(**ref).lower() for value in path_keys]
    return cache.get_nitwit_cache_path(data)
