import requests
import os
import subprocess
import shutil


def with_request(gist, headers):
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


def with_git(gist):
    folder = name_folder(gist)
    gist_pull_url = f"git@gist.github.com:{gist['id']}.git"
    if not os.path.exists(folder):
        subprocess.call(["git", "clone", "--recursive", gist_pull_url, folder])
    else:
        subprocess.call(["git", "-C", folder, "pull", "--recurse-submodules"])


def name_folder(gist):
    return gist["description"] if gist["description"] != "" else gist["id"]


def download_gists(username, token, git_check):
    API_ENDPOINT = f"https://api.github.com/users/{username}/gists"

    headers = {
        "Authorization": f"token {token}",
    }

    if not token:
        headers = None

    response = requests.get(API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        for gist in response.json():
            with_request(gist, headers) if not git_check else with_git(gist)
    else:
        print(response.status_code, response.text)
