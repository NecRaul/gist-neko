import unittest
from typing import Any
from unittest.mock import MagicMock, patch

import requests

from gist_neko import config, github
from gist_neko.models import FiltersConfig


class _FakeResponse:
    def __init__(
        self, payload: list[dict[str, Any]], status_code: int, text: str = ""
    ) -> None:
        self._payload: list[dict[str, Any]] = payload
        self.status_code: int = status_code
        self.text: str = text

    def json(self) -> list[dict[str, Any]]:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(
                f"{self.status_code} {self.text}",
                response=MagicMock(status_code=self.status_code),
            )


def fake_gist(
    gist_id: int,
    description: str = "test gist",
    public: bool = True,
) -> dict[str, Any]:
    return {
        "id": gist_id,
        "description": description,
        "public": public,
    }


class DownloadTests(unittest.TestCase):
    def test_get_gists_uses_public_endpoint_without_token(self) -> None:
        calls: list[tuple[str, dict[str, str] | None, dict[str, Any] | None]] = []
        filters: FiltersConfig = config.DEFAULT_CONFIG["filters"]
        headers: dict[str, str] | None = None

        responses: list[_FakeResponse] = [
            _FakeResponse(
                payload=[
                    fake_gist(1, "first"),
                    fake_gist(2, "second"),
                ],
                status_code=200,
            ),
            _FakeResponse(payload=[], status_code=200),
        ]

        def fake_get(
            url: str,
            headers: dict[str, str] | None = None,
            params: dict[str, Any] | None = None,
        ) -> _FakeResponse:
            calls.append((url, headers, params))
            return responses.pop(0)

        with patch.object(requests.Session, "get", side_effect=fake_get):
            with requests.Session() as session:
                gists: list[dict[str, Any]] = github.get_gists(
                    session, "alice", headers=headers
                )
                filtered_gists: list[dict[str, Any]] = github.filter_gists(
                    gists, filters
                )

        self.assertEqual(
            filtered_gists,
            [
                fake_gist(1, "first"),
                fake_gist(2, "second"),
            ],
        )
        self.assertEqual(
            calls,
            [
                (
                    "https://api.github.com/users/alice/gists",
                    headers,
                    {"per_page": 100, "page": 1},
                ),
                (
                    "https://api.github.com/users/alice/gists",
                    headers,
                    {"per_page": 100, "page": 2},
                ),
            ],
        )

    def test_get_gists_forwards_headers_with_authentication_token(self) -> None:
        calls: list[tuple[str, dict[str, str] | None, dict[str, Any] | None]] = []
        filters: FiltersConfig = config.DEFAULT_CONFIG["filters"]
        headers: dict[str, str] | None = {"Authorization": "token abc123"}

        responses: list[_FakeResponse] = [
            _FakeResponse(
                payload=[fake_gist(1, "private", public=False)], status_code=200
            ),
            _FakeResponse(payload=[], status_code=200),
        ]

        def fake_get(
            url: str,
            headers: dict[str, str] | None = None,
            params: dict[str, Any] | None = None,
        ) -> _FakeResponse:
            calls.append((url, headers, params))
            return responses.pop(0)

        with patch.object(requests.Session, "get", side_effect=fake_get):
            with requests.Session() as session:
                gists: list[dict[str, Any]] = github.get_gists(
                    session, "alice", headers=headers
                )
                filtered_gists: list[dict[str, Any]] = github.filter_gists(
                    gists, filters
                )

        self.assertEqual(filtered_gists, [fake_gist(1, "private", public=False)])
        self.assertEqual(
            calls,
            [
                (
                    "https://api.github.com/users/alice/gists",
                    headers,
                    {"per_page": 100, "page": 1},
                ),
                (
                    "https://api.github.com/users/alice/gists",
                    headers,
                    {"per_page": 100, "page": 2},
                ),
            ],
        )

    def test_get_gists_stops_and_returns_collected_on_error(self) -> None:
        calls: list[tuple[str, dict[str, str] | None, dict[str, Any] | None]] = []
        headers: dict[str, str] | None = None

        responses: list[_FakeResponse] = [
            _FakeResponse(payload=[fake_gist(1, "first")], status_code=200),
            _FakeResponse(payload=[], status_code=500, text="boom"),
        ]

        def fake_get(
            url: str,
            headers: dict[str, str] | None = None,
            params: dict[str, Any] | None = None,
        ) -> _FakeResponse:
            calls.append((url, headers, params))
            return responses.pop(0)

        with patch.object(requests.Session, "get", side_effect=fake_get):
            with requests.Session() as session:
                with self.assertRaises(requests.HTTPError):
                    github.get_gists(session, "alice", headers=headers)
