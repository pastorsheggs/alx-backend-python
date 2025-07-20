#!/usr/bin/env python3
"""Integration test for GithubOrgClient.public_repos"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mock the .json() response depending on URL
        def side_effect(url):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/test_org":
                mock_resp.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/test_org/repos":
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with Apache 2.0 license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
