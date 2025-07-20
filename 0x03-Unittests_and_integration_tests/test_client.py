#!/usr/bin/env python3
"""Unit and Integration tests for client.py"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class(
    (
        "org_payload",
        "repos_payload",
        "expected_repos",
        "apache2_repos",
    ),
    [
        (
            TEST_PAYLOAD["org_payload"],
            TEST_PAYLOAD["repos_payload"],
            TEST_PAYLOAD["expected_repos"],
            TEST_PAYLOAD["apache2_repos"],
        )
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient.public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set side_effects for different URLs"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect to simulate requests.get().json() based on URL
        def side_effect(url):
            mock_response = MagicMock()
            if url.endswith("orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method with integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )
