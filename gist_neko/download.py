import requests
import os
import subprocess


def with_request(gist, headers):
    gist_id = gist["id"]
    if not os.path.exists(gist_id):
        os.mkdir(gist_id)
    files = gist["files"]
    for filename in files:
        gist_url = files[filename]["raw_url"]
        response = requests.get(gist_url, headers=headers)
        with open(f"{gist_id}/{filename}", "wb") as file:
            file.write(response.content)


def with_git(gist):
    gist_id = gist["id"]
    gist_pull_url = f"git@gist.github.com:{gist_id}.git"
    if not os.path.exists(gist_id):
        subprocess.call(["git", "clone", gist_pull_url])
    else:
        subprocess.call(["git", "-C", gist_id, "pull"])


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
