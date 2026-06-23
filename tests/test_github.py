import unittest

from gist_neko import config, download


class GithubIntegrationTests(unittest.TestCase):
    def test_fetches_public_gists_from_necraul_account(self):
        filters = config.DEFAULT_CONFIG.get("filters")
        gists = download.get_gists(username="NecRaul", headers=None)
        filtered_gists = download.filter_gists(gists, filters)

        self.assertIsInstance(filtered_gists, list)
        self.assertGreater(len(filtered_gists), 5)
        self.assertTrue(
            all(gist["owner"]["login"] == "NecRaul" for gist in filtered_gists)
        )
