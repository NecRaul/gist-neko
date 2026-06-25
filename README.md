# gist-neko

CLI for syncing gists from a specified GitHub user.

## Installation

### Via PyPI (Recommended)

#### With pip (Basic)

```sh
pip install gist-neko
```

#### With pipx (Isolated)

```sh
pipx install gist-neko
```

#### With uv (Best)

The most efficient way to install or run `gist-neko`.

```sh
# Permanent isolated installation
uv tool install gist-neko

# Run once without installing
uvx gist-neko -u <github-username>

# Run in scripts or ad-hoc environments
uv run --with gist-neko gist-neko -u <github-username> -t <github-personal-access-token>
```

### From Source (Development)

```sh
# Clone the repository and navigate to it
git clone git@github.com:NecRaul/gist-neko.git
cd gist-neko

# Install environment and all development dependencies (mandatory and optional)
uv sync --dev

# Install pre-commit hook
uv run pre-commit install

# Optional: Run all linters and type checkers manually
uv run pre-commit run --all-files

# Run the local version
uv run gist-neko -u <github-username> --git
```

## Usage

`gist-neko` acts as a sync tool. If a gist folder doesn't exist, it clones it, if it does, it updates it.

```sh
# Sync public gists with `requests`
gist-neko -u <github-username>

# Sync public and private gists with `requests` (using a personal access token)
gist-neko -u <github-username> -t <github-personal-access-token>

# Use 'git clone/pull' instead of 'requests' (preserves history, branches and submodules)
gist-neko -u <github-username> -g

# Use 'git' with a personal access token for private gist syncing
gist-neko -u <github-username> -t <github-personal-access-token> --git

# Sync gists to a specific directory
gist-neko -u <github-username> -d /path/to/gists

# Include only public gists
gist-neko -u <github-username> --visibility public

# Exclude forked gists
gist-neko -u <github-username> --fork no

# Include only forked gists
gist-neko -u <github-username> --fork yes

# Combine filters: public non-fork gists to a specific directory
gist-neko -u <github-username> -d /path/to/gists --visibility public --fork no
```

### Options

```sh
-h, --help                             Display usage information and exit
-v, --version                          Show program version and exit

    --config          FILE             Load configuration from file
    --no-config                        Ignore configuration file
    --init-config     [FILE]           Create a default configuration file
    --show-config                      Show effective configuration and exit

-u, --username       USERNAME          GitHub username to fetch gists from
-t, --token          TOKEN             GitHub personal access token for private gists

-e, --environment                      Read username and token from environment variables
    --no-environment                   Do not read username and token from environment variables

-g, --git                              Download gists using git instead of archive downloads
    --no-git                           Download gists using archive downloads instead of git

    --visibility      VIS [...]        Visibility levels to include:
                                       public, private, both

    --fork            {yes,no,both}    Filter fork gists
```

### Configuration

`gist-neko` supports a JSON configuration file to set defaults for all options. You can create a default config, inspect the effective configuration, and override or ignore the config file at runtime.

- Default path
  - Linux/BSD: `$XDG_CONFIG_HOME/necraul/gist-neko.json` or `~/.config/necraul/gist-neko.json`
  - MacOS: `~/Library/Application Support/necraul/gist-neko.json`
  - Windows: `%APPDATA%/necraul/gist-neko.json`
- Basic structure
  - `github`: credentials and whether to read from environment variables.
  - `download`: target directory and git engine settings including extra args for `clone` and `pull`.
  - `filters`: control which gists are included by visibility and fork status.

```json
{
  "github": {
    "username": null,
    "token": null,
    "environment": false
  },
  "download": {
    "directory": ".",
    "git": {
      "enabled": true,
      "clone_args": ["--recursive"],
      "pull_args": ["--recurse-submodules"]
    }
  },
  "filters": {
    "visibility": ["public", "private"],
    "fork": "both"
  }
}
```

```sh
# Create a default configuration file at the default path
gist-neko --init-config

# Create a default configuration file at a custom path
gist-neko --init-config config.json

# Show the effective configuration (defaults merged with the config file)
gist-neko --show-config

# Create a default configuration file at the default path and print it
gist-neko --init-config --show-config

# Create a default configuration file at a custom path and print it
gist-neko --init-config /path/to/config.json --show-config

# Show the effective configuration using a custom config file
gist-neko --config config.json --show-config

# Use a custom configuration file
gist-neko --config /path/to/config.json

# Ignore the configuration file and use only CLI flags
gist-neko --no-config -u <github-username>

# Override config's directory at runtime
gist-neko -d /path/to/gists
```

### Environment Variables

You can save your credentials to environment variables to avoid passing them manually in every command.

For persistence, add these exports to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`).

```sh
# Set your credentials as environment variables
export GITHUB_USERNAME="NecRaul"
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_necraul"
export GITHUB_GISTS_DIRECTORY="/path/to/gists"

# Run using the stored environment variables
gist-neko --environment

# Run without using environment variables
gist-neko --no-environment

# Run using the git engine
gist-neko --git

# Run without using the git engine
gist-neko --no-git

# Run using environment variables with the git engine
gist-neko -e --git

# Run using environment variables without the git engine
gist-neko -e --no-git

# Run without environment variables with the git engine
gist-neko --no-environment --git

# Run without environment variables without the git engine
gist-neko --no-environment --no-git

# Pass the GitHub username and personal access token environment variables directly within the command
GITHUB_USERNAME="NecRaul" GITHUB_PERSONAL_ACCESS_TOKEN="ghp_necraul" gist-neko --environment

# Pass the directory environment variable directly within the command
GITHUB_GISTS_DIRECTORY="/path/to/gists" gist-neko --environment
```

> [!TIP]
> `--environment` and `--git` enable a feature, while `--no-environment` and `--no-git` disable it.

## Dependencies

- [requests](https://github.com/psf/requests): fetch data from the GitHub API and handle downloads.

## How it works

The tool queries the `https://api.github.com/users/{username}/gists` endpoint. It retrieves public Gists when unauthenticated, or both public and private Gists when an authentication token is provided.

Once the gist list is retrieved, `gist-neko` automates the synchronization process using one of two engines:

- Requests Engine (via `--no-git`): Fetches the gist as a compressed snapshot. This is fast but does not include **history**, **branches** or **submodules**.
- Git Engine (via `-g` or `--git` flag): Uses your local **git** installation to perform a full **clone** or **pull**. This preserves the complete **history**, **branches** and **submodules**.

### The Manual Way

Without this tool, you would need to manually parse JSON responses, manage authentication headers, and write logic to differentiate between new clones and existing updates:

```sh
# A simplified version of the logic gist-neko automates
# It fetches the id and description, then loops through them
curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/users/NecRaul/gists |
    jq -r '.[] | "\(.description // .id) \(.id)"' | while read -r name id; do
    if [ ! -d "$name" ]; then
        git clone --recursive "git@gist.github.com:$id.git" "$name"
    else
        echo "Pulling '$name'..."
        git -C "$name" pull --recurse-submodules
    fi
done
```

### The gist-neko way

- Dynamic API Routing: Automatically identifies the correct GitHub endpoint. It uses `/users/{username}/gists` for browsing, ensuring that when authenticated, you get the full list of both public and private gists you have permission to view.
- State-Aware Syncing: Instead of a simple download, it checks your local file system using the gist's description or ID as the folder name. If a gist already exists, it intelligently switches to an "update" mode (using `git pull` or overwriting via `requests`) to keep your local mirror current.
- Hybrid Engine Support:
  - Lightweight Mode: Uses `requests` to pull gist snapshots quickly without needing `git` installed or **SSH keys** configured.
  - Developer Mode (`--git`): Interfaces directly with your local `git` binary to handle **full history**, **branch tracking**, and **submodule recursion**.
- Gist Filtering: Supports fine-grained control over which gists are synced, filtering by visibility and fork status.
- Subprocess Management: Uses Python's `subprocess` module to provide a robust bridge between the GitHub API and your local shell, handling directory navigation and command execution automatically.
