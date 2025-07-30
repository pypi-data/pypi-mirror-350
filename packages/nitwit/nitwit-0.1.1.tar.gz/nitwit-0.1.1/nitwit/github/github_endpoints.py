from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import polars as pl


def get_endpoint_url(datatype: str) -> str:
    return {
        'repo': 'https://api.github.com/repos/{owner}/{name}',
        'commits': 'https://api.github.com/repos/{owner}/{name}/commits',
        'user': 'https://api.github.com/users/{username}',
    }[datatype]


def get_endpoint_path_keys(datatype: str) -> list[str]:
    return {
        'repo': ['github_repos', 'metadata', '{owner}', '{name}'],
        'commits': ['github_repos', 'commits', '{owner}', '{name}'],
        'user': ['github_users', 'metadata', '{username}'],
    }[datatype]


def get_endpoint_schema(datatype: str) -> dict[str, pl.Datatype]:
    import polars as pl

    return {
        'repo': {
            'id': pl.Int64,
            'node_id': pl.String,
            'name': pl.String,
            'full_name': pl.String,
            'private': pl.Boolean,
            'owner': pl.Struct(
                {
                    'login': pl.String,
                    'id': pl.Int64,
                    'node_id': pl.String,
                    'avatar_url': pl.String,
                    'gravatar_id': pl.String,
                    'url': pl.String,
                    'html_url': pl.String,
                    'followers_url': pl.String,
                    'following_url': pl.String,
                    'gists_url': pl.String,
                    'starred_url': pl.String,
                    'subscriptions_url': pl.String,
                    'organizations_url': pl.String,
                    'repos_url': pl.String,
                    'events_url': pl.String,
                    'received_events_url': pl.String,
                    'type': pl.String,
                    'user_view_type': pl.String,
                    'site_admin': pl.Boolean,
                }
            ),
            'html_url': pl.String,
            'description': pl.String,
            'fork': pl.Boolean,
            'url': pl.String,
            'forks_url': pl.String,
            'keys_url': pl.String,
            'collaborators_url': pl.String,
            'teams_url': pl.String,
            'hooks_url': pl.String,
            'issue_events_url': pl.String,
            'events_url': pl.String,
            'assignees_url': pl.String,
            'branches_url': pl.String,
            'tags_url': pl.String,
            'blobs_url': pl.String,
            'git_tags_url': pl.String,
            'git_refs_url': pl.String,
            'trees_url': pl.String,
            'statuses_url': pl.String,
            'languages_url': pl.String,
            'stargazers_url': pl.String,
            'contributors_url': pl.String,
            'subscribers_url': pl.String,
            'subscription_url': pl.String,
            'commits_url': pl.String,
            'git_commits_url': pl.String,
            'comments_url': pl.String,
            'issue_comment_url': pl.String,
            'contents_url': pl.String,
            'compare_url': pl.String,
            'merges_url': pl.String,
            'archive_url': pl.String,
            'downloads_url': pl.String,
            'issues_url': pl.String,
            'pulls_url': pl.String,
            'milestones_url': pl.String,
            'notifications_url': pl.String,
            'labels_url': pl.String,
            'releases_url': pl.String,
            'deployments_url': pl.String,
            'created_at': pl.String,
            'updated_at': pl.String,
            'pushed_at': pl.String,
            'git_url': pl.String,
            'ssh_url': pl.String,
            'clone_url': pl.String,
            'svn_url': pl.String,
            'homepage': pl.String,
            'size': pl.Int64,
            'stargazers_count': pl.Int64,
            'watchers_count': pl.Int64,
            'language': pl.String,
            'has_issues': pl.Boolean,
            'has_projects': pl.Boolean,
            'has_downloads': pl.Boolean,
            'has_wiki': pl.Boolean,
            'has_pages': pl.Boolean,
            'has_discussions': pl.Boolean,
            'forks_count': pl.Int64,
            'mirror_url': pl.Null,
            'archived': pl.Boolean,
            'disabled': pl.Boolean,
            'open_issues_count': pl.Int64,
            'license': pl.Struct(
                {
                    'key': pl.String,
                    'name': pl.String,
                    'spdx_id': pl.String,
                    'url': pl.String,
                    'node_id': pl.String,
                }
            ),
            'allow_forking': pl.Boolean,
            'is_template': pl.Boolean,
            'web_commit_signoff_required': pl.Boolean,
            'topics': pl.List(pl.String),
            'visibility': pl.String,
            'forks': pl.Int64,
            'open_issues': pl.Int64,
            'watchers': pl.Int64,
            'default_branch': pl.String,
            'permissions': pl.Struct(
                {
                    'admin': pl.Boolean,
                    'maintain': pl.Boolean,
                    'push': pl.Boolean,
                    'triage': pl.Boolean,
                    'pull': pl.Boolean,
                }
            ),
            'custom_properties': pl.Struct(
                {'last_reviewed': pl.String, 'team': pl.List(pl.String)}
            ),
            'organization': pl.Struct(
                {
                    'login': pl.String,
                    'id': pl.Int64,
                    'node_id': pl.String,
                    'avatar_url': pl.String,
                    'gravatar_id': pl.String,
                    'url': pl.String,
                    'html_url': pl.String,
                    'followers_url': pl.String,
                    'following_url': pl.String,
                    'gists_url': pl.String,
                    'starred_url': pl.String,
                    'subscriptions_url': pl.String,
                    'organizations_url': pl.String,
                    'repos_url': pl.String,
                    'events_url': pl.String,
                    'received_events_url': pl.String,
                    'type': pl.String,
                    'user_view_type': pl.String,
                    'site_admin': pl.Boolean,
                }
            ),
            'network_count': pl.Int64,
            'subscribers_count': pl.Int64,
        },
        'user': {
            'login': pl.String,
            'id': pl.Int64,
            'node_id': pl.String,
            'avatar_url': pl.String,
            'gravatar_id': pl.String,
            'url': pl.String,
            'html_url': pl.String,
            'followers_url': pl.String,
            'following_url': pl.String,
            'gists_url': pl.String,
            'starred_url': pl.String,
            'subscriptions_url': pl.String,
            'organizations_url': pl.String,
            'repos_url': pl.String,
            'events_url': pl.String,
            'received_events_url': pl.String,
            'type': pl.String,
            'user_view_type': pl.String,
            'site_admin': pl.Boolean,
            'name': pl.String,
            'company': pl.String,
            'blog': pl.String,
            'location': pl.String,
            'email': pl.String,
            'hireable': pl.Boolean,
            'bio': pl.String,
            'twitter_username': pl.String,
            'public_repos': pl.Int64,
            'public_gists': pl.Int64,
            'followers': pl.Int64,
            'following': pl.Int64,
            'created_at': pl.Datetime(time_unit='ms', time_zone='UTC'),
            'updated_at': pl.Datetime(time_unit='ms', time_zone='UTC'),
        },
        'commits': {
            'sha': pl.String,
            'node_id': pl.String,
            'commit': pl.Struct(
                {
                    'author': pl.Struct(
                        {
                            'name': pl.String,
                            'email': pl.String,
                            'date': pl.String,
                        }
                    ),
                    'committer': pl.Struct(
                        {
                            'name': pl.String,
                            'email': pl.String,
                            'date': pl.String,
                        }
                    ),
                    'message': pl.String,
                    'tree': pl.Struct({'sha': pl.String, 'url': pl.String}),
                    'url': pl.String,
                    'comment_count': pl.Int64,
                    'verification': pl.Struct(
                        {
                            'verified': pl.Boolean,
                            'reason': pl.String,
                            'signature': pl.String,
                            'payload': pl.String,
                            'verified_at': pl.String,
                        }
                    ),
                }
            ),
            'url': pl.String,
            'html_url': pl.String,
            'comments_url': pl.String,
            'author': pl.Struct(
                {
                    'login': pl.String,
                    'id': pl.Int64,
                    'node_id': pl.String,
                    'avatar_url': pl.String,
                    'gravatar_id': pl.String,
                    'url': pl.String,
                    'html_url': pl.String,
                    'followers_url': pl.String,
                    'following_url': pl.String,
                    'gists_url': pl.String,
                    'starred_url': pl.String,
                    'subscriptions_url': pl.String,
                    'organizations_url': pl.String,
                    'repos_url': pl.String,
                    'events_url': pl.String,
                    'received_events_url': pl.String,
                    'type': pl.String,
                    'user_view_type': pl.String,
                    'site_admin': pl.Boolean,
                }
            ),
            'committer': pl.Struct(
                {
                    'login': pl.String,
                    'id': pl.Int64,
                    'node_id': pl.String,
                    'avatar_url': pl.String,
                    'gravatar_id': pl.String,
                    'url': pl.String,
                    'html_url': pl.String,
                    'followers_url': pl.String,
                    'following_url': pl.String,
                    'gists_url': pl.String,
                    'starred_url': pl.String,
                    'subscriptions_url': pl.String,
                    'organizations_url': pl.String,
                    'repos_url': pl.String,
                    'events_url': pl.String,
                    'received_events_url': pl.String,
                    'type': pl.String,
                    'user_view_type': pl.String,
                    'site_admin': pl.Boolean,
                }
            ),
            'parents': pl.List(
                pl.Struct(
                    {'sha': pl.String, 'url': pl.String, 'html_url': pl.String}
                )
            ),
        },
    }[datatype]
