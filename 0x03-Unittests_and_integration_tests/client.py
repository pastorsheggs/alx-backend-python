#!/usr/bin/env python3
"""GithubOrgClient module"""

from utils import get_json
from functools import cached_property


class GithubOrgClient:
    """GithubOrgClient class to fetch data from GitHub organizations"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org):
        self.org_name = org

    def org(self):
        """Fetch organization info"""
        url = self.ORG_URL.format(org=self.org_name)
        return get_json(url)

    @cached_property
    def _public_repos_url(self):
        """Get the URL for public repos"""
        return self.org().get("repos_url")

    def public_repos(self):
        """Fetch list of public repo names"""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

