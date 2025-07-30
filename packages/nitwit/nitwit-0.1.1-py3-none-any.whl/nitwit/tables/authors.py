from __future__ import annotations

import typing

from .. import sources
from . import commits as commits_module

if typing.TYPE_CHECKING:
    import polars as pl


def collect_authors(
    repo_or_commits: str | list[str] | pl.DataFrame,
    collapse_across_repos: bool = True,
) -> pl.DataFrame:
    import polars as pl

    if isinstance(repo_or_commits, pl.DataFrame):
        commits = repo_or_commits

    else:
        if isinstance(repo_or_commits, str):
            raw_repos = [repo_or_commits]
        else:
            raw_repos = repo_or_commits

        repos = sources.resolve_repo_references(repo_or_commits)
        pieces = []
        for raw_source, source in zip(raw_repos, repos):
            commits = commits_module.collect_commits(
                repo=source, include_file_stats=True
            )
            pieces.append(commits)
        commits = pl.concat(pieces)

    return _collect_author_stats(commits, collapse_across_repos)


def _collect_author_stats(
    commits: pl.DataFrame, collapse_across_repos: bool
) -> pl.DataFrame:
    import polars as pl

    if collapse_across_repos:
        keys = ['author', 'email']
        n_repos = pl.col.repo_source.n_unique()
    else:
        keys = ['author', 'email', 'repo_author', 'repo_name', 'repo_source']
        n_repos = pl.lit(1)

    extra_columns = {}
    if 'n_changed_files' in commits.schema:
        extra_columns['n_changed_files'] = pl.col.n_changed_files.sum().cast(
            pl.Int64
        )
    if 'insertions' in commits.schema:
        extra_columns['insertions'] = pl.col.insertions.sum().cast(pl.Int64)
    if 'deletions' in commits.schema:
        extra_columns['deletions'] = pl.col.deletions.sum().cast(pl.Int64)

    authors = commits.group_by(keys).agg(
        first_commit_timestamp=pl.col.timestamp.min(),
        last_commit_timestamp=pl.col.timestamp.max(),
        n_commits=pl.col.hash.n_unique().cast(pl.Int64),
        **extra_columns,
        n_repos=n_repos,
    )
    return authors
