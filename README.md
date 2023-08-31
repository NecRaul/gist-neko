# gist-neko

CLI for downloading all gists from a specified user.

## Requirements

`requests` is used for CUrl command.

If you want to build this on your own, you can install the requirements with

```Python
pip install -r requirements.txt
```

or install the package by running

```Python
pip install gist-neko
```

Python's native `os` (used to check for whether a folder exists or not), `argparse` (parse return request and set command argument), `subprocess` (call `git clone` and `git pull` on gists) and `setuptools` (used to build the script) packages are also used.

## How it works

I send requests to `https://api.github.com/gists/`, depending on the arguments passed to the script, I either download all the gists in specified user's account with either `requests` or `git`.

You can run the script with

```Python
gist-neko
    -u <github-username>
    -t <github-personal-access-token> (optional - you will just download the public gists instead of all gists)
    -g (optional - typing -g <anything> means you will be downloading using git)
```
