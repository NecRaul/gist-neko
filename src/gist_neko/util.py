from pathlib import Path
from typing import cast

import requests

from gist_neko.models import Config, Gist


def matches_visibility(gist: Gist, filter: list[str]) -> bool:
    if "both" in filter:
        return True

    visibility: str = "public" if gist["public"] else "private"
    return visibility in filter


def matches_fork(gist: Gist, filter: str) -> bool:
    if filter == "both":
        return True

    response: requests.Response = requests.get(
        f"https://api.github.com/gists/{gist['id']}"
    )
    response.raise_for_status()
    is_fork: bool = "fork_of" in response.json()
    return is_fork == (filter == "yes")


def remove_none(data: Config) -> Config:
    if isinstance(data, dict):
        return cast(
            Config,
            {
                key: remove_none(value) if isinstance(value, dict) else value  # ty:ignore[invalid-argument-type]
                for key, value in data.items()
                if value is not None
            },
        )
    return data


def validate_directory(path: Path) -> None:
    if path.exists() and not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")
