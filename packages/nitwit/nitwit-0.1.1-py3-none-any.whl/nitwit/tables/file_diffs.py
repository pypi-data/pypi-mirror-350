from __future__ import annotations

import typing

if typing:
    import polars as pl

from .. import sources


def collect_commit_file_diffs(repo: str) -> pl.DataFrame:
    return (
        collect_file_diffs(repo)
        .group_by('hash')
        .agg(
            n_changed_files=pl.len(),
            insertions=pl.col.insertions.sum(),
            deletions=pl.col.deletions.sum(),
        )
    )


def collect_file_diffs(repo: str) -> pl.DataFrame:
    import polars as pl

    if isinstance(repo, str):
        raw_repos = [repo]
    else:
        raw_repos = repo
    repos = sources.resolve_repo_references(repo)
    pieces = []
    for raw_source, source in zip(raw_repos, repos):
        file_diffs = _collect_file_stats(repo)
        file_diffs = sources.add_repo_columns(file_diffs, raw_source)
        pieces.append(file_diffs)
    return pl.concat(pieces)


def _collect_file_stats(repo: str) -> pl.DataFrame:
    import subprocess

    cmd = [
        'git',
        '-C',
        repo,
        'log',
        '--all',
        '--numstat',
        '--format="  %H"',
    ]
    output = subprocess.check_output(cmd, universal_newlines=True).strip('\n')
    output = '\n'.join(line.strip('"') for line in output.split('\n'))

    # parse output
    hashes = []
    insertions = []
    deletions = []
    paths = []
    chunks = output.lstrip(' ').split('\n  ')
    for c, chunk in enumerate(chunks):
        if '\n' not in chunk:
            continue
        chunk_hash, files = chunk.split('\n\n')
        for file in files.split('\n'):
            file_insertions, file_deletions, file_path = file.split('\t')
            hashes.append(chunk_hash)
            insertions.append(file_insertions)
            deletions.append(file_deletions)
            paths.append(file_path)

    schema = {
        'hash': pl.String,
        'insertions': pl.String,
        'deletions': pl.String,
        'path': pl.String,
    }
    data = {
        'hash': hashes,
        'insertions': insertions,
        'deletions': deletions,
        'path': paths,
    }
    return (
        pl.DataFrame(data, schema=schema)
        .with_columns(
            insertions=pl.col.insertions.replace('-', None),
            deletions=pl.col.deletions.replace('-', None),
        )
        .with_columns(
            insertions=pl.col.insertions.cast(pl.Int64),
            deletions=pl.col.deletions.cast(pl.Int64),
        )
    )
