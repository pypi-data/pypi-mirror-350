import logging
from typing import Any, Dict

import requests


class GitHubAPIClient:
    """
    Client for interacting with the GitHub API.
    Handles authentication and common API requests.
    """

    def __init__(self, github_token: str, repo_owner: str, repo_name: str) -> None:
        self.github_token: str = github_token
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
        }
        self.base_api_url: str = (
            f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        )

    def _get_json_response(self, url: str) -> Dict[str, Any]:
        """
        Generic method to fetch JSON response from a given API URL and handle errors.
        """
        logging.info(f"Fetching URL: {url}")
        response: requests.Response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error fetching {url}: {e}")
            raise
        return response.json()

    def get_workflow_runs(
        self, workflow_filename: str, baseline_branch: str
    ) -> Dict[str, Any]:
        """
        Fetches the most recent successful workflow run for the baseline branch.
        """
        url: str = (
            f"{self.base_api_url}/actions/workflows/{workflow_filename}.yml/runs"
            f"?branch={baseline_branch}&status=success&per_page=1"
        )
        return self._get_json_response(url)

    def get_artifacts_for_run(self, run_id: int) -> Dict[str, Any]:
        """
        Fetches artifacts for a specific workflow run ID.
        """
        url: str = f"{self.base_api_url}/actions/runs/{run_id}/artifacts"
        return self._get_json_response(url)

    def download_artifact(self, artifact_id: int) -> requests.Response:
        """
        Downloads a specific artifact by its ID.
        Returns the response object to handle streaming or content access.
        """
        download_url: str = f"{self.base_api_url}/actions/artifacts/{artifact_id}/zip"
        logging.info(f"Downloading artifact from: {download_url}")
        response: requests.Response = requests.get(download_url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error downloading artifact: {e}")
            raise
        return response
