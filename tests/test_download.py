import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import requests

from gist_neko import download


class _FakeResponse:
    def __init__(self, status_code: int, payload, text: str = ""):
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        return self._payload


class DownloadTests(unittest.TestCase):
    def test_get_all_gists_uses_public_endpoint_without_token(self):
        self.assertEqual(requests.__name__, "requests")
        calls: list[tuple[str, dict | None]] = []

        responses = [
            _FakeResponse(
                200,
                [
                    {"id": "1", "description": "first"},
                    {"id": "2", "description": "second"},
                ],
            ),
            _FakeResponse(200, []),
        ]

        def fake_get(url, headers=None):
            calls.append((url, headers))
            return responses.pop(0)

        with patch.object(download.requests, "get", side_effect=fake_get):
            gists = download.get_all_gists("alice", headers=None)

        self.assertEqual(
            gists,
            [
                {"id": "1", "description": "first"},
                {"id": "2", "description": "second"},
            ],
        )
        self.assertEqual(
            calls,
            [
                ("https://api.github.com/users/alice/gists?per_page=100&page=1", None),
                ("https://api.github.com/users/alice/gists?per_page=100&page=2", None),
            ],
        )

    def test_get_all_gists_forwards_headers_with_authentication_token(self):
        calls: list[tuple[str, dict | None]] = []
        headers = {"Authorization": "token abc123"}

        responses = [
            _FakeResponse(200, [{"id": "1", "description": "private"}]),
            _FakeResponse(200, []),
        ]

        def fake_get(url, headers=None):
            calls.append((url, headers))
            return responses.pop(0)

        with patch.object(download.requests, "get", side_effect=fake_get):
            gists = download.get_all_gists("alice", headers=headers)

        self.assertEqual(gists, [{"id": "1", "description": "private"}])
        self.assertEqual(
            calls,
            [
                (
                    "https://api.github.com/users/alice/gists?per_page=100&page=1",
                    headers,
                ),
                (
                    "https://api.github.com/users/alice/gists?per_page=100&page=2",
                    headers,
                ),
            ],
        )

    def test_get_all_gists_stops_and_returns_collected_on_error(self):
        responses = [
            _FakeResponse(200, [{"id": "1", "description": "first"}]),
            _FakeResponse(500, [], text="boom"),
        ]

        def fake_get(url, headers=None):
            return responses.pop(0)

        output = io.StringIO()
        with (
            patch.object(download.requests, "get", side_effect=fake_get),
            redirect_stdout(output),
        ):
            gists = download.get_all_gists("alice", headers=None)

        self.assertEqual(gists, [{"id": "1", "description": "first"}])
        self.assertIn("500 boom", output.getvalue())
