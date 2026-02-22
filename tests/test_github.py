import unittest

from gist_neko.download import get_all_gists


class GithubIntegrationTests(unittest.TestCase):
    def test_fetches_public_gists_from_necraul_account(self):
        gists = get_all_gists(username="NecRaul", headers=None)

        self.assertIsInstance(gists, list)
        self.assertGreater(len(gists), 5)
        self.assertTrue(all(gist["owner"]["login"] == "NecRaul" for gist in gists))
