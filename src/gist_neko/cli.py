import argparse
import os

from .download import download_gists
from .version import __version__


def main():
    parser = argparse.ArgumentParser(
        description="Download specified user's all gists at once",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: %(prog)s -u NecRaul -g",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Github username to fetch gists from.",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Github public access token for private gists.",
    )
    parser.add_argument(
        "-e",
        "--environment",
        action=argparse.BooleanOptionalAction,
        help="Read the username and token from environment variables.",
    )
    parser.add_argument(
        "-g",
        "--git",
        action=argparse.BooleanOptionalAction,
        help="Download gists using git instead of archive downloads.",
    )
    parser.add_argument(
        "--visibility",
        nargs="+",
        choices=["public", "private", "both"],
        default=["both"],
        help="Visibility levels to include (multiple allowed).",
    )
    parser.add_argument(
        "--fork",
        choices=["yes", "no", "both"],
        default="both",
        help="Filter fork gists.",
    )

    args = parser.parse_args()

    if args.environment:
        username = os.getenv("GITHUB_USERNAME")
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    else:
        username = args.username
        token = args.token

    git_check = args.git
    options = {
        "visibility": args.visibility,
        "fork": args.fork,
    }

    if not username:
        print("Pass your Github username with -u.")
    else:
        download_gists(username, token, git_check, options)
