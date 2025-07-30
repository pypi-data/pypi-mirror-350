from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import polars as pl


def add_repo_columns(df: pl.DataFrame, repo: str) -> pl.DataFrame:
    import os
    import polars as pl

    if repo.endswith('.git'):
        repo = repo[:-4]
    repo = repo.rstrip('/')
    repo_author = os.path.basename(os.path.dirname(repo))
    repo_name = os.path.basename(repo)
    return df.with_columns(
        repo_author=pl.lit(repo_author),
        repo_name=pl.lit(repo_name),
        repo_source=pl.lit(repo),
    )


def resolve_repo_references(repos: str | list[str]) -> list[str]:
    if isinstance(repos, str):
        repos = [repos]
    return [resolve_repo_reference(repo) for repo in repos]


def resolve_repo_reference(repo: str) -> str:
    """resolve repo reference into local path to repository .git path"""
    if repo.startswith('https://'):
        raise NotImplementedError()
    else:
        return get_repo_git_dir(repo)


def get_repo_git_dir(repo_path: str) -> str:
    import os
    import subprocess

    repo_path = os.path.expanduser(repo_path)
    cmd = ['git', '-C', repo_path, 'rev-parse', '--absolute-git-dir']
    return subprocess.check_output(cmd, universal_newlines=True).rstrip('\n')
