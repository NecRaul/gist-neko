# gist-neko

CLI for downloading all gists from a specified user.

## Requirements

`requests` is used for getting information from the Github API and downloading the gists (if you don't use git).

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
    -e (optional - typing -e <anything> means you will be using environment variables. This overrides -u and -t)
    -g (optional - typing -g <anything> means you will be downloading using git)
    -gu <github-username> (this will put <github-username> as environment variable)
    -gpat <github-personal-access-token> (this will put <github-personal-access-token> as environment variable)
```

### Examples

#### Setting Environment Variables (Only works on Windows)

This will set the specified **Github username** and **personal access token** as your `GITHUB_USERNAME` and `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable respectively.

```Python
gist-neko -gu <github-username> -gpat <github-personal-access-token>
```

This will set the specified **Github username** as your `GITHUB_USERNAME` environment variable.

```Python
gist-neko -gu <github-username>
```

This will set the specified **personal access token** as your `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable.

```Python
gist-neko -gpat <github-personal-access-token>
```

#### Public Gists without Environment Variables

This will use the specified **Github username** and download all **public gists** using `requests`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token>
```

This will use the specified **Github username** and download all **public gists** using `git`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token> -g <anything>
```

#### Public and Private Gists without Environment Variables

This will use the specified **Github username** and **personal access token** and download all **public and private gists** using `requests`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token>
```

This will use the specified **Github username** and **personal access token** and download all **public and private gists** using `git`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token> -g <anything>
```

#### Public and Private Gists with Environment Variables

This will use the **Github username** and **personal access token** in the **environment variables** and download all **public and private gists** using `requests`.

```Python
gist-neko -e <anything>
```

This will use the **Github username** and **personal access token** in the **environment variables** and download all **public and private gists** using `git`.

```Python
gist-neko -e <anything> -g <anything>
```

#### Public and Private Gists with Environment Variables (Overriding passed Username and Personal Access Token)

This will **ignore** the passed **Github username** and **personal access token** instead using **environment variables** and download all **public and private gists** using `requests`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token> -e <anything>
```

This will **ignore** the passed **Github username** and **personal access token** instead using **environment variables** and download all **public and private gists** using `git`.

```Python
gist-neko -u <github-username> -t <github-personal-access-token> -e <anything> -g <anything>
```

### Simplified Examples

If you want to only download your gists (public), you can do

```Python
gist-neko -u <your-username>
```

If you want to only download your gists (public and private), you can either do

```Python
gist-neko -u <your-username> -t <your-personal-access-token>
```

or you can put your information on environment variables and do

```Python
gist-neko -e <anything>
```

If you want to download other people's gists (public), you can do

```Python
gist-neko -u <their-username>
```

If you want to download other people's gists (public and private), you can do

```Python
gist-neko -u <their-username> -t <their-personal-access-token>
```

#### Elephant in the room

`-gu` and `-gpat` doesn't work on Linux. Why you might ask?

First of all, I suck at Linux.

Second of all, the code I wrote should technically work but gives me the file not found error despite `~/.bashrc` being there.

I'll try to fix it as soon as possible (if I don't forget).
