import io
import sys
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

from gist_neko import cli, config
from gist_neko.models import FiltersConfig


class CliTests(unittest.TestCase):
    def test_main_uses_explicit_cli_arguments(self) -> None:
        called: dict[str, tuple[str, str | None, bool, FiltersConfig]] = {}
        filters: FiltersConfig = config.DEFAULT_CONFIG["filters"]

        def fake_download_gists(
            username: str, token: str | None, git_enabled: bool, filters: FiltersConfig
        ) -> None:
            called["args"] = (username, token, git_enabled, filters)

        with (
            patch.object(cli.github, "download_gists", side_effect=fake_download_gists),
            patch.object(
                sys,
                "argv",
                ["gist-neko", "-u", "alice", "-t", "token123", "-g", "--no-config"],
            ),
        ):
            cli.main()

        self.assertEqual(called["args"], ("alice", "token123", True, filters))

    def test_main_uses_environment_variables_when_enabled(self) -> None:
        called: dict[str, tuple[str, str | None, bool, FiltersConfig]] = {}
        filters: FiltersConfig = config.DEFAULT_CONFIG["filters"]

        def fake_download_gists(
            username: str, token: str | None, git_enabled: bool, filters: FiltersConfig
        ) -> None:
            called["args"] = (username, token, git_enabled, filters)

        with (
            patch.object(cli.github, "download_gists", side_effect=fake_download_gists),
            patch.dict(
                "os.environ",
                {
                    "GITHUB_USERNAME": "env-user",
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "env-token",
                },
                clear=False,
            ),
            patch.object(sys, "argv", ["gist-neko", "-e", "--no-config"]),
        ):
            cli.main()

        self.assertEqual(called["args"], ("env-user", "env-token", True, filters))

    def test_main_prints_hint_if_username_missing(self) -> None:
        stderr: io.StringIO = io.StringIO()

        with (
            patch.object(sys, "argv", ["gist-neko", "--no-config"]),
            redirect_stderr(stderr),
            self.assertRaises(SystemExit) as ctx,
        ):
            cli.main()

        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("Pass your Github username with -u.", stderr.getvalue())
