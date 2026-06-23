import requests


def matches_visibility(gist, filter):
    if "both" in filter:
        return True

    visibility = "public" if gist["public"] else "private"
    return visibility in filter


def matches_fork(gist, filter):
    if filter == "both":
        return True

    response = requests.get(f"https://api.github.com/gists/{gist['id']}")
    response.raise_for_status()
    is_fork = "fork_of" in response.json()
    return is_fork == (filter == "yes")


def remove_none(data):
    if isinstance(data, dict):
        return {
            key: remove_none(value) for key, value in data.items() if value is not None
        }
    return data
