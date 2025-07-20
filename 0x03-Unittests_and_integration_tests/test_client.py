import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures

@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock patcher for requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == f"https://api.github.com/orgs/{fixtures.org_payload['login']}":
                return MockResponse(fixtures.org_payload)
            elif url == fixtures.org_payload["repos_url"]:
                return MockResponse(fixtures.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the mock patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )


class MockResponse:
    """Mock response class for .json()"""
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload
