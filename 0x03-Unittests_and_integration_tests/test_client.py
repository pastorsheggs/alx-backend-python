#!/usr/bin/env python3
"""test_client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @patch("client.get_json")
    def test_public_repos(self, mocked_get_json):
        """Test public_repos returns expected names"""
        mocked_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
        ]
        mocked_get_json.return_value = mocked_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mocked_repos_url:
            mocked_repos_url.return_value = "http://fake-url.com"

            client = GithubOrgClient("google")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mocked_get_json.assert_called_once()
            mocked_repos_url.assert_called_once()
