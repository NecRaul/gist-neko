import requests
import os

public_access_token = ""
user = "NecRaul"

headers = {
    "Authorization": f"token {public_access_token}",
}

response = requests.get(f"https://api.github.com/users/{user}/gists", headers=headers)

for gist in response.json():
    gist_id = gist["id"]
    if not os.path.exists(gist_id):
        os.mkdir(gist_id)
    files = gist["files"]
    for filename in files:
        gist_url = files[filename]["raw_url"]
        response = requests.get(gist_url, headers=headers)
        with open(f"{gist_id}/{filename}", "wb") as file:
            file.write(response.content)