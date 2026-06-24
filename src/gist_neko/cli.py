import argparse
import json
import sys
from pathlib import Path

from gist_neko import __version__, config, github
from gist_neko.models import Config, FiltersConfig


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download specified user's all gists at once",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: %(prog)s -u NecRaul -g",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    config_group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group()
    )
    config_group.add_argument("--config", help="load configuration from file")
    config_group.add_argument(
        "--no-config", action="store_true", help="ignore configuration file"
    )
    config_group.add_argument(
        "--init-config",
        nargs="?",
        const=None,
        default=argparse.SUPPRESS,
        help="create default configuration file",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="show effective configuration and exit",
    )
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
        help="Visibility levels to include (multiple allowed).",
    )
    parser.add_argument(
        "--fork",
        choices=["yes", "no", "both"],
        default="both",
        help="Filter fork gists.",
    )

    args: argparse.Namespace = parser.parse_args()

    if hasattr(args, "init_config"):
        path: Path = config.save_config(config.DEFAULT_CONFIG, args.init_config)
        print(f"Config created at {path}", file=sys.stderr)
        if args.show_config:
            print(json.dumps(config.DEFAULT_CONFIG, indent=2))
        return

    cfg: Config = config.load_effective_config(
        path=args.config, no_config=args.no_config
    )

    if args.show_config:
        print(json.dumps(cfg, indent=2))
        return

    cli_environment: bool | None = getattr(args, "environment", None)
    use_environment: bool = (
        cli_environment if cli_environment is not None else cfg["github"]["environment"]
    )

    if use_environment:
        cfg: Config = config.apply_environment_overrides(cfg)

    cfg: Config = config.apply_cli_overrides(cfg, args)

    username: str | None = cfg["github"]["username"]
    token: str | None = cfg["github"]["token"]
    git_enabled: bool = cfg["download"]["git"]["enabled"]
    filters: FiltersConfig = cfg["filters"]

    if not username:
        parser.error("Pass your Github username with -u.")

    github.download_gists(username, token, git_enabled, filters)
