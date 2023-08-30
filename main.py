import requests

public_access_token = ""
user = "NecRaul"

headers = {
    "Authorization": f"token {public_access_token}",
}

response = requests.get(f"https://api.github.com/users/{user}/gists", headers=headers)

for gist in response.json():
    gist_id = gist["id"]
    files = gist["files"]
    print(gist_id, files)