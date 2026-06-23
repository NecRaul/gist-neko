import requests


def matches_visibility(gist, option):
    if "both" in option:
        return True

    visibility = "public" if gist["public"] else "private"
    return visibility in option


def matches_fork(gist, option):
    if option == "both":
        return True

    response = requests.get(f"https://api.github.com/gists/{gist['id']}")
    response.raise_for_status()
    is_fork = "fork_of" in response.json()
    return is_fork == (option == "yes")
