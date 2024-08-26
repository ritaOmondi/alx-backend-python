#!/usr/bin/env python3
""" Unittest module """

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method returns the expected list of repos"""
    expected_repos = ['repo1', 'repo2', 'repo3']
    mock_get_json.return_value = [
        {'name': 'repo1'}, {'name': 'repo2'}, {'name': 'repo3'}
    ]

    with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
        mock_public_repos_url.return_value = 'https://api.github.com/orgs/test_org/repos'
        client = GithubOrgClient('test_org')
        self.assertEqual(client.public_repos(), expected_repos)

    mock_get_json.assert_called_once_with('https://api.github.com/orgs/test_org/repos')
    mock_public_repos_url.assert_called_once()
    """
    @patch('client.get_json')
    def test_org(self, org_name, mock_json):
        """ Test method returns correct output """
        endpoint = 'https://api.github.com/orgs/{}'.format(org_name)
        spec = GithubOrgClient(data)
        spec.org()
        mock_json.assert_called_once_with(endpoint)

    @parameterized.expand([
        ("random-url", {'repos_url': 'http://some_url.com'})
    ])
    """
    def test_public_repos_url(self, name, result):
        """ Test method returns correct output """
        with patch('client.GithubOrgClient.org',
                   PropertyMock(return_value=result)):
            response = GithubOrgClient(name)._public_repos_url
            self.assertEqual(response, result.get('repos_url'))
