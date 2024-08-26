#!/usr/bin/env python3
""" Unittest and Integration Test module """

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """ Unit tests for GithubOrgClient """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_public_repos(self, org_name, mock_get_json):
        """Test the public_repos method returns the expected list of repos"""
        expected_repos = ['repo1', 'repo2', 'repo3']
        mock_get_json.return_value = [
            {'name': 'repo1'}, {'name': 'repo2'}, {'name': 'repo3'}
        ]

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = f'https://api.github.com/orgs/{org_name}/repos'
            client = GithubOrgClient(org_name)
            self.assertEqual(client.public_repos(), expected_repos)

        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}/repos')
        mock_public_repos_url.assert_called_once()

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """ Test org method returns correct output """
        org_name = "test_org"
        endpoint = f'https://api.github.com/orgs/{org_name}'
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(endpoint)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Test the has_license method """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ("random_org", {'repos_url': 'http://some_url.com'}),
    ])
    def test_public_repos_url(self, org_name, result):
        """ Test _public_repos_url returns the correct URL """
        with patch('client.GithubOrgClient.org', PropertyMock(return_value=result)):
            response = GithubOrgClient(org_name)._public_repos_url
            self.assertEqual(response, result.get('repos_url'))


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for GithubOrgClient """

    @classmethod
    def setUpClass(cls):
        """ Set up class method to mock external requests """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = cls.get_side_effect

    @classmethod
    def tearDownClass(cls):
        """ Tear down class method to stop the patcher """
        cls.get_patcher.stop()

    @classmethod
    def get_side_effect(cls, url):
        """ Method to mock requests.get().json() depending on URL """
        if url == "https://api.github.com/orgs/google":
            return MockResponse(org_payload)
        if url == "https://api.github.com/orgs/google/repos":
            return MockResponse(repos_payload)
        return None

    def test_public_repos(self):
        """ Test public_repos method of GithubOrgClient """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """ Test public_repos method with license filtering """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


class MockResponse:
    """ MockResponse to simulate requests.get().json() """
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


if __name__ == "__main__":
    unittest.main()

