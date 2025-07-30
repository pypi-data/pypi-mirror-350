from __future__ import annotations


def get_nitwit_cache_root() -> str:
    import os

    cache_root = os.environ.get('NITWIT_CACHE_ROOT')
    if cache_root is not None and cache_root != '':
        return cache_root
    else:
        return os.path.expanduser('~/data/nitwit_cache')


def get_nitwit_cache_path(data: list[str], filetype: str = 'json') -> str:
    import os

    filename = '__'.join(data) + '.' + filetype
    return os.path.join(get_nitwit_cache_root(), *data[:-1], filename)
