import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from gist_neko import config, download


class _FakeResponse:
    def __init__(self, payload, status_code: int, text: str = ""):
        self._payload = payload
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._payload


def fake_gist(
    gist_id,
    description="test gist",
    public=True,
):
    return {
        "id": gist_id,
        "description": description,
        "public": public,
    }


class DownloadTests(unittest.TestCase):
    def test_get_gists_uses_public_endpoint_without_token(self):
        calls: list[tuple[str, dict | None]] = []
        filters = config.DEFAULT_CONFIG.get("filters")
        headers = None

        responses = [
            _FakeResponse(
                payload=[
                    fake_gist(1, "first"),
                    fake_gist(2, "second"),
                ],
                status_code=200,
            ),
            _FakeResponse(payload=[], status_code=200),
        ]

        def fake_get(url, headers=None):
            calls.append((url, headers))
            return responses.pop(0)

        with patch.object(download.requests, "get", side_effect=fake_get):
            gists = download.get_gists("alice", headers=headers)
            filtered_repos = download.filter_gists(gists, filters)

        self.assertEqual(
            filtered_repos,
            [
                fake_gist(1, "first"),
                fake_gist(2, "second"),
            ],
        )
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

    def test_get_gists_forwards_headers_with_authentication_token(self):
        calls: list[tuple[str, dict | None]] = []
        filters = config.DEFAULT_CONFIG.get("filters")
        headers = {"Authorization": "token abc123"}

        responses = [
            _FakeResponse(
                payload=[fake_gist(1, "private", public=False)], status_code=200
            ),
            _FakeResponse(payload=[], status_code=200),
        ]

        def fake_get(url, headers=None):
            calls.append((url, headers))
            return responses.pop(0)

        with patch.object(download.requests, "get", side_effect=fake_get):
            gists = download.get_gists("alice", headers=headers)
            filtered_gists = download.filter_gists(gists, filters)

        self.assertEqual(filtered_gists, [fake_gist(1, "private", public=False)])
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

    def test_get_gists_stops_and_returns_collected_on_error(self):
        calls: list[tuple[str, dict | None]] = []
        filters = config.DEFAULT_CONFIG.get("filters")
        headers = None
        responses = [
            _FakeResponse(payload=[fake_gist(1, "first")], status_code=200),
            _FakeResponse(payload=[], status_code=500, text="boom"),
        ]

        def fake_get(url, headers=None):
            calls.append((url, headers))
            return responses.pop(0)

        stdout = io.StringIO()
        with (
            patch.object(download.requests, "get", side_effect=fake_get),
            redirect_stdout(stdout),
        ):
            gists = download.get_gists("alice", headers=headers)
            filtered_gists = download.filter_gists(gists, filters)

        self.assertEqual(filtered_gists, [fake_gist(1, "first")])
        self.assertIn("500 boom", stdout.getvalue())
