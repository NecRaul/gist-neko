from typing import Any, TypeAlias, TypedDict


class GithubConfig(TypedDict, total=False):
    username: str | None
    token: str | None
    environment: bool


class GitDownloadConfig(TypedDict, total=False):
    enabled: bool
    clone_args: list[str]
    pull_args: list[str]


class DownloadConfig(TypedDict, total=False):
    git: GitDownloadConfig


class FiltersConfig(TypedDict, total=False):
    visibility: list[str]
    fork: str


class Config(TypedDict, total=False):
    github: GithubConfig
    download: DownloadConfig
    filters: FiltersConfig


ConfigDict: TypeAlias = dict[str, Any]
Gist: TypeAlias = dict[str, Any]
