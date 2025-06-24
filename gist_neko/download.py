import requests
import os
import subprocess
import shutil


def download_with_requests(gists, headers):
    for gist in gists:
        folder = name_folder(gist)
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"Downloading the gist '{folder}'...")
        else:
            print(f"Updating the gist '{folder}'...")
            shutil.rmtree(folder)
        files = gist["files"]
        for filename in files:
            gist_url = files[filename]["raw_url"]
            response = requests.get(gist_url, headers=headers)
            with open(f"{folder}/{filename}", "wb") as file:
                file.write(response.content)


def download_with_git(gists):
    for gist in gists:
        folder = name_folder(gist)
        gist_pull_url = f"git@gist.github.com:{gist['id']}.git"
        if not os.path.exists(folder):
            subprocess.call(["git", "clone", "--recursive", gist_pull_url, folder])
        else:
            subprocess.call(["git", "-C", folder, "pull", "--recurse-submodules"])


def name_folder(gist):
    return gist["description"] if gist["description"] != "" else gist["id"]


def get_all_gists(username, headers):
    gists = []
    page = 1

    while True:
        page_query = f"?per_page=100&page={page}"
        API_ENDPOINT = f"https://api.github.com/users/{username}/gists{page_query}"

        response = requests.get(API_ENDPOINT, headers=headers)

        if response.status_code != 200:
            print(response.status_code, response.text)
            break

        page_gists = response.json()

        if not page_gists:
            break

        gists.extend(page_gists)
        page += 1

    return gists


def download_gists(username, token, git_check):
    headers = {"Authorization": f"token {token}"} if token else None
    gists = get_all_gists(username, headers)

    if git_check:
        download_with_git(gists)
    else:
        download_with_requests(gists)
