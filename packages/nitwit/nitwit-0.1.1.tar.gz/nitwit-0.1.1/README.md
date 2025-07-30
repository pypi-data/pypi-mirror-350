
# nitwit

tools for converting git repository data into data tables

## Python Interface

```python
# specify repo(s), using path(s) or url(s)
repo = '/path/to/git/repo'
repo = 'https://github.com/author_name/repo_name'
repo = [
    '/path/to/git/repo1',
    '/path/to/git/repo2',
    'https://github.com/author_name1/repo_name2',
    'https://github.com/author_name1/repo_name2',
]

commits = nitwit.commits(repo)
authors = nitwit.authors(repo)
file_diffs = nitwit.file_diffs(repo)
```

## Table Schemas

#### `commits`

```
- hash: String
- author: String
- email: String
- timestamp: DateTime('ms')
- message: String
- parents: String
- committer: String
- committer_email: String
- commit_timestamp: DateTime('ms')
- tree_hash: String
- repo: String
```

#### `authors`

```
- name: String
- email: String
- n_commits: Int64
- n_changed_files: Int64
- insertions: Int64
- deletions: Int64
- first_commit_timestamp: DateTime('ms')
- last_commit_timestamp: DateTime('ms')
- n_repos: Int64
```

#### `file_diffs`

```
- hash: String
- insertions: Int64
- deletions: Int64
- path: String
- repo: String
```

#### `repos`

```
- repo: String
- n_files: Int64
- n_commits: Int64
- n_authors: Int64
- first_commit_timestamp: DateTime('ms')
- last_commit_timestamp: DateTime('ms')
```

#### `github_user_metadata`

```
- login: String
- id: Int64
- node_id: String
- avatar_url: String
- gravatar_id: String
- url: String
- html_url: String
- followers_url: String
- following_url: String
- gists_url: String
- starred_url: String
- subscriptions_url: String
- organizations_url: String
- repos_url: String
- events_url: String
- received_events_url: String
- type: String
- user_view_type: String
- site_admin: Boolean
- name: String
- company: String
- blog: String
- location: String
- email: String
- hireable: Boolean
- bio: String
- twitter_username: String
- public_repos: Int64
- public_gists: Int64
- followers: Int64
- following: Int64
- created_at: DateTime('ms')
- updated_at: DateTime('ms')
```

#### `github_repo_metadata`

```
- id: Int64
- node_id: String
- name: String
- full_name: String
- private: Boolean
- owner: Struct
    - login: String
    - id: Int64
    - node_id: String
    - avatar_url: String
    - gravatar_id: String
    - url: String
    - html_url: String
    - followers_url: String
    - following_url: String
    - gists_url: String
    - starred_url: String
    - subscriptions_url: String
    - organizations_url: String
    - repos_url: String
    - events_url: String
    - received_events_url: String
    - type: String
    - user_view_type: String
    - site_admin: Boolean
- html_url: String
- description: String
- fork: Boolean
- url: String
- forks_url: String
- keys_url: String
- collaborators_url: String
- teams_url: String
- hooks_url: String
- issue_events_url: String
- events_url: String
- assignees_url: String
- branches_url: String
- tags_url: String
- blobs_url: String
- git_tags_url: String
- git_refs_url: String
- trees_url: String
- statuses_url: String
- languages_url: String
- stargazers_url: String
- contributors_url: String
- subscribers_url: String
- subscription_url: String
- commits_url: String
- git_commits_url: String
- comments_url: String
- issue_comment_url: String
- contents_url: String
- compare_url: String
- merges_url: String
- archive_url: String
- downloads_url: String
- issues_url: String
- pulls_url: String
- milestones_url: String
- notifications_url: String
- labels_url: String
- releases_url: String
- deyments_url: String
- created_at: String
- updated_at: String
- pushed_at: String
- git_url: String
- ssh_url: String
- clone_url: String
- svn_url: String
- homepage: String
- size: Int64
- stargazers_count: Int64
- watchers_count: Int64
- language: String
- has_issues: Boolean
- has_projects: Boolean
- has_downloads: Boolean
- has_wiki: Boolean
- has_pages: Boolean
- has_discussions: Boolean
- forks_count: Int64
- mirror_url: Null
- archived: Boolean
- disabled: Boolean
- open_issues_count: Int64
- license: Struct
    - key: String
    - name: String
    - spdx_id: String
    - url: String
    - node_id: String
- allow_forking: Boolean
- is_temte: Boolean
- web_commit_signoff_required: Boolean
- topics: List(String)
- visibility: String
- forks: Int64
- open_issues: Int64
- watchers: Int64
- default_branch: String
- permissions: Struct
    - admin: Boolean
    - maintain: Boolean
    - push: Boolean
    - triage: Boolean
    - pull: Boolean
- custom_properties: Struct
    - last_reviewed: String
    - team: List(String)
- organization: Struct
    - login: String
    - id: Int64
    - node_id: String
    - avatar_url: String
    - gravatar_id: String
    - url: String
    - html_url: String
    - followers_url: String
    - following_url: String
    - gists_url: String
    - starred_url: String
    - subscriptions_url: String
    - organizations_url: String
    - repos_url: String
    - events_url: String
    - received_events_url: String
    - type: String
    - user_view_type: String
    - site_admin: Boolean
- network_count: Int64
- subscribers_count: Int64
```
