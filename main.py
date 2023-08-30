import requests
import os

public_access_token = ""
user = "NecRaul"

API_ENDPOINT = f"https://api.github.com/users/{user}/gists"

def download_gists(gists):
    for gist in gists:
        gist_id = gist["id"]
        if not os.path.exists(gist_id):
            os.mkdir(gist_id)
        files = gist["files"]
        for filename in files:
            gist_url = files[filename]["raw_url"]
            response = requests.get(gist_url, headers=headers)
            with open(f"{gist_id}/{filename}", "wb") as file:
                file.write(response.content)

headers = {
    "Authorization": f"token {public_access_token}",
}

response = requests.get(API_ENDPOINT, headers=headers)


if response.status_code == 200:
    download_gists(response.json())
else:
    print(response.status_code, response.text)