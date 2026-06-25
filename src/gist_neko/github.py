import shutil
import subprocess
from pathlib import Path

import requests

from gist_neko import util
from gist_neko.models import FiltersConfig, Gist


def download_with_requests(
    gists: list[Gist], headers: dict[str, str] | None, directory: Path
) -> None:
    gist_count: int = len(gists)
    count_digit: int = len((str(gist_count)))
    util.validate_directory(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i, gist in enumerate(gists, start=1):
        gist_name: str = name_gist(gist)
        gist_path: Path = directory / gist_name
        util.validate_directory(gist_path)
        if not gist_path.exists():
            print(f"[{i:>{count_digit}}/{gist_count}] Downloading '{gist_path}'...")
        else:
            shutil.rmtree(gist_path)
            print(f"[{i:>{count_digit}}/{gist_count}] Updating '{gist_path}'...")
        gist_path.mkdir(parents=True, exist_ok=True)
        files: dict[str, dict[str, str]] = gist["files"]
        for filename in files:
            gist_url: str = files[filename]["raw_url"]
            response: requests.Response = requests.get(
                gist_url, headers=headers, timeout=30
            )
            response.raise_for_status()
            safe_filename: str = Path(filename).name
            (gist_path / safe_filename).write_bytes(response.content)


def download_with_git(gists: list[Gist], directory: Path) -> None:
    gist_count: int = len(gists)
    count_digit: int = len((str(gist_count)))
    util.validate_directory(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i, gist in enumerate(gists, start=1):
        gist_pull_url: str = f"git@gist.github.com:{gist['id']}.git"
        gist_name: str = name_gist(gist)
        gist_path: Path = directory / gist_name
        util.validate_directory(gist_path)
        if not gist_path.exists():
            print(f"[{i:>{count_digit}}/{gist_count}]", end=" ", flush=True)
            subprocess.call(["git", "clone", "--recursive", gist_pull_url, gist_path])
        else:
            print(f"[{i:>{count_digit}}/{gist_count}] Pulling '{gist_name}'...")
            subprocess.call(["git", "-C", gist_path, "pull", "--recurse-submodules"])


def name_gist(gist: Gist) -> str:
    return gist["description"] if gist["description"] != "" else gist["id"]


def github_get_all(endpoint: str, headers: dict[str, str] | None) -> list[Gist]:
    items: list[Gist] = []
    page = 1

    while True:
        response: requests.Response = requests.get(
            endpoint, headers=headers, params={"per_page": 100, "page": page}
        )
        response.raise_for_status()
        page_items: list[Gist] = response.json()
        if not page_items:
            break
        items.extend(page_items)
        page += 1

    return items


def get_gists(username: str, headers: dict[str, str] | None) -> list[Gist]:
    endpoint = f"https://api.github.com/users/{username}/gists"

    return github_get_all(endpoint, headers)


def filter_gists(gists: list[Gist], filters: FiltersConfig) -> list[Gist]:
    return [
        gist
        for gist in gists
        if util.matches_visibility(gist, filters["visibility"])
        and util.matches_fork(gist, filters["fork"])
    ]


def download_gists(
    username: str,
    token: str | None,
    git_enabled: bool,
    filters: FiltersConfig,
    directory: Path,
) -> None:
    headers: dict[str, str] | None = (
        {"Authorization": f"token {token}"} if token else None
    )
    gists: list[Gist] = get_gists(username, headers)
    filtered_gists: list[Gist] = filter_gists(gists, filters)

    if git_enabled:
        download_with_git(filtered_gists, directory)
    else:
        download_with_requests(filtered_gists, headers, directory)
