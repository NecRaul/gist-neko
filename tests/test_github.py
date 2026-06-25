import unittest

import requests

from gist_neko import config, github
from gist_neko.models import FiltersConfig, Gist


class GitHubIntegrationTests(unittest.TestCase):
    def test_fetches_public_gists_from_necraul_account(self) -> None:
        filters: FiltersConfig = config.DEFAULT_CONFIG["filters"]
        with requests.Session() as session:
            gists: list[Gist] = github.get_gists(
                session, username="NecRaul", headers=None
            )
            filtered_gists: list[Gist] = github.filter_gists(gists, filters)

        self.assertIsInstance(filtered_gists, list)
        self.assertGreater(len(filtered_gists), 5)
        self.assertTrue(
            all(gist["owner"]["login"] == "NecRaul" for gist in filtered_gists)
        )
