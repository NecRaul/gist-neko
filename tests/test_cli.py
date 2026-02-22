import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from gist_neko import cli


class CliTests(unittest.TestCase):
    def test_main_uses_explicit_cli_arguments(self):
        called = {}

        def fake_download_gists(username, token, git_check):
            called["args"] = (username, token, git_check)

        with (
            patch.object(cli, "download_gists", side_effect=fake_download_gists),
            patch.object(
                sys, "argv", ["gist-neko", "-u", "alice", "-t", "token123", "-g"]
            ),
        ):
            cli.main()

        self.assertEqual(called["args"], ("alice", "token123", True))

    def test_main_uses_environment_variables_when_enabled(self):
        called = {}

        def fake_download_gists(username, token, git_check):
            called["args"] = (username, token, git_check)

        with (
            patch.object(cli, "download_gists", side_effect=fake_download_gists),
            patch.dict(
                "os.environ",
                {
                    "GITHUB_USERNAME": "env-user",
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "env-token",
                },
                clear=False,
            ),
            patch.object(sys, "argv", ["gist-neko", "-e"]),
        ):
            cli.main()

        self.assertEqual(called["args"], ("env-user", "env-token", False))

    def test_main_prints_hint_if_username_missing(self):
        output = io.StringIO()

        with patch.object(sys, "argv", ["gist-neko"]), redirect_stdout(output):
            cli.main()

        self.assertIn("Pass your Github username with -u.", output.getvalue())
