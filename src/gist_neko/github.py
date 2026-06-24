import shutil
import subprocess
from pathlib import Path

import requests

from gist_neko import util


def download_with_requests(gists, headers):
    gist_count = len(gists)
    count_digit = len((str(gist_count)))
    for i, gist in enumerate(gists, start=1):
        gist_name = name_gist(gist)
        gist_dir = Path(gist_name)
        if not gist_dir.exists():
            gist_dir.mkdir()
            print(f"[{i:>{count_digit}}/{gist_count}] Downloading '{gist_name}'...")
        else:
            shutil.rmtree(gist_dir)
            gist_dir.mkdir()
            print(f"[{i:>{count_digit}}/{gist_count}] Updating '{gist_name}'...")
        files = gist["files"]
        for filename in files:
            gist_url = files[filename]["raw_url"]
            response = requests.get(gist_url, headers=headers, timeout=30)
            response.raise_for_status()
            safe_filename = Path(filename).name
            (gist_dir / safe_filename).write_bytes(response.content)


def download_with_git(gists):
    gist_count = len(gists)
    count_digit = len((str(gist_count)))
    for i, gist in enumerate(gists, start=1):
        gist_name = name_gist(gist)
        gist_pull_url = f"git@gist.github.com:{gist['id']}.git"
        if not Path(gist_name).exists():
            print(f"[{i:>{count_digit}}/{gist_count}]", end=" ", flush=True)
            subprocess.call(["git", "clone", "--recursive", gist_pull_url, gist_name])
        else:
            print(f"[{i:>{count_digit}}/{gist_count}] Pulling '{gist_name}'...")
            subprocess.call(["git", "-C", gist_name, "pull", "--recurse-submodules"])


def name_gist(gist):
    return gist["description"] if gist["description"] != "" else gist["id"]


def github_get_all(endpoint, headers):
    items = []
    page = 1

    while True:
        response = requests.get(
            endpoint, headers=headers, params={"per_page": 100, "page": page}
        )

        response.raise_for_status()

        page_items = response.json()

        if not page_items:
            break

        items.extend(page_items)
        page += 1

    return items


def get_gists(username, headers):
    endpoint = f"https://api.github.com/users/{username}/gists"

    return github_get_all(endpoint, headers)


def filter_gists(gists, filters):
    return [
        gist
        for gist in gists
        if util.matches_visibility(gist, filters["visibility"])
        and util.matches_fork(gist, filters["fork"])
    ]


def download_gists(username, token, git_enabled, filters):
    headers = {"Authorization": f"token {token}"} if token else None
    gists = get_gists(username, headers)
    filtered_gists = filter_gists(gists, filters)

    if git_enabled:
        download_with_git(filtered_gists)
    else:
        download_with_requests(filtered_gists, headers)
