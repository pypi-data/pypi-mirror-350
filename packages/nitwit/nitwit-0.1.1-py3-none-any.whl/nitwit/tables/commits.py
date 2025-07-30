from __future__ import annotations

import typing

if typing:
    import polars as pl

from .. import cache
from .. import sources
from . import file_diffs


def collect_commits(
    repo: str | list[str],
    include_file_stats: bool = False,
    _extra_log_args: list[str] | None = None,
    load_from_cache: bool = True,
    save_to_cache: bool = True,
) -> pl.DataFrame:
    if isinstance(repo, str):
        raw_repos = [repo]
    else:
        raw_repos = repo
    repos = sources.resolve_repo_references(raw_repos)

    pieces = []
    for raw_source, source in zip(raw_repos, repos):
        piece = _collect_commits_single(
            raw_source=raw_source,
            source=source,
            include_file_stats=include_file_stats,
            _extra_log_args=_extra_log_args,
            load_from_cache=load_from_cache,
            save_to_cache=save_to_cache,
        )
        pieces.append(piece)

    return pl.concat(pieces)


def _collect_commits_single(
    raw_source: str,
    source: str,
    include_file_stats: bool = False,
    _extra_log_args: list[str] | None = None,
    load_from_cache: bool = True,
    save_to_cache: bool = True,
) -> pl.DataFrame:
    import json
    import os
    import polars as pl
    import shutil

    # load from cache
    path = _get_commits_path(source, include_file_stats)
    if load_from_cache and os.path.exists(path):
        return pl.read_parquet(path)

    # collect basics
    commits = _collect_commit_basics(source, _extra_log_args)

    # collect file stats
    if include_file_stats:
        stats = file_diffs.collect_commit_file_diffs(source)
        commits = commits.join(stats, on='hash', how='left')

    # add additional columns
    commits = sources.add_repo_columns(commits, source)

    # save to cache
    if save_to_cache:
        tmp_path = path + '_tmp'
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        commits.write_parquet(tmp_path)
        shutil.move(tmp_path, path)

        index_path = path.replace('.parquet', '.json')
        tmp_index_path = index_path + '_tmp'
        with open(tmp_index_path, 'w') as f:
            json.dump({'source': source}, f)
        shutil.move(tmp_index_path, index_path)

    return commits


def _get_commits_path(source: str, include_file_stats: bool) -> str:
    import hashlib
    import os

    stats_flag = 'with_stats' if include_file_stats else 'without_stats'
    full_path = os.path.abspath(os.path.expanduser(source))
    hash_name = hashlib.md5(full_path.encode()).hexdigest()
    return cache.get_nitwit_cache_path(
        ['commits', stats_flag, hash_name], 'parquet'
    )


def _collect_commit_basics(
    repo: str, _extra_log_args: list[str] | None
) -> pl.DataFrame:
    import io
    import subprocess
    import polars as pl

    schema = {
        'hash': pl.String,
        'author': pl.String,
        'email': pl.String,
        'timestamp': pl.Int64,
        'message': pl.String,
        'parents': pl.String,
        'committer': pl.String,
        'committer_email': pl.String,
        'commit_timestamp': pl.Int64,
        'tree_hash': pl.String,
    }
    datetime = pl.Datetime('ms', time_zone='UTC')

    COMMIT_SEP = '\u001e'
    SEP = '\u001f'

    cmd = [
        'git',
        '-C',
        repo,
        'log',
        '--all',
        '--format='
        + COMMIT_SEP
        + '%H|%an|%ae|%at|%s|%P|%cn|%ce|%ct|%T'.replace('|', SEP),
        '--no-abbrev-commit',
    ]
    if _extra_log_args is not None:
        cmd.extend(_extra_log_args)
    output_bytes = subprocess.check_output(cmd)
    output = output_bytes.decode('utf-8', errors='replace')

    if output == '':
        return pl.DataFrame(schema=schema).with_columns(
            is_merge=pl.lit(False),
            timestamp=(pl.col.timestamp * 1000).cast(datetime),
            commit_timestamp=(pl.col.commit_timestamp * 1000).cast(datetime),
        )

    commits = output.split(COMMIT_SEP)[1:]
    cleaned_commits = []
    for commit in commits:
        commit = commit.replace('\n', ' ').rstrip(' ')
        fields = commit.split(SEP)
        if len(fields) < 10:
            continue
        elif len(fields) > 10:
            fields[4] = ' '.join(fields[4 : len(fields) - 5])
            fields = fields[:4] + [fields[4]] + fields[-5:]
        cleaned_commits.append(SEP.join(fields))
    cleaned = '\n'.join(cleaned_commits)

    df = pl.read_csv(
        io.StringIO(cleaned),
        schema=schema,
        has_header=False,
        separator=SEP,
        quote_char=None,
        truncate_ragged_lines=False,
    )

    df = df.with_columns(is_merge=pl.col.parents.str.contains(' '))

    df = df.with_columns(
        timestamp=(pl.col.timestamp * 1000).cast(datetime),
        commit_timestamp=(pl.col.commit_timestamp * 1000).cast(datetime),
    )

    return df
