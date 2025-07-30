from __future__ import annotations

import typing

if typing.TYPE_CHECKING:

    class ParsedRepoReference(typing.TypedDict):
        host: str
        owner: str
        name: str


def parse_repo_reference(ref: str) -> dict[str, str]:
    if ref.startswith('https://'):
        return parse_repo_url(ref)
    elif ref.startswith('/'):
        return parse_repo_path(ref)
    else:
        raise Exception('invalid repo: ' + str(ref))


def parse_repo_url(url: str) -> dict[str, str]:
    if not url.startswith('https://'):
        raise Exception('url must start with https://')
    host, owner, name, *_ = url.split('https://')[1].split('/')
    return {'host': host, 'owner': owner, 'name': name}


def parse_repo_path(path: str) -> dict[str, str]:
    *_, host, owner, name = path.rstrip('/').split('/')
    return {'host': host, 'owner': owner, 'name': name}
