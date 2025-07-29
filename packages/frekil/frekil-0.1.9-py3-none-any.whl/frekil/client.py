"""
Main client class for interacting with the Frekil API
"""

import requests

from .auth.api_key import APIKeyAuth
from .api.projects import ProjectsAPI
from .api.allocations import AllocationsAPI
from .exceptions.base import FrekilAPIError, FrekilClientError


class FrekilClient:
    """
    Main client for interacting with the Frekil API.

    Args:
        api_key (str): Your Frekil API key
        base_url (str, optional): Base URL for the Frekil API.
            Defaults to production API.
    """

    def __init__(self, api_key, base_url="https://prod.notatehq.com/api/sdk"):
        self.base_url = base_url.rstrip("/")
        self.auth = APIKeyAuth(api_key)
        self.session = self._create_session()

        # API endpoints
        self.projects = ProjectsAPI(self)
        self.allocations = AllocationsAPI(self)

    def _create_session(self):
        """Create a requests session with the API key authentication"""
        session = requests.Session()
        session.headers.update(
            {
                "X-API-Key": self.auth.api_key,
                "User-Agent": f"frekil-python-sdk/{self.__version__}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        return session

    def request(self, method, endpoint, **kwargs):
        """
        Make a request to the Frekil API

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            **kwargs: Additional arguments to pass to requests

        Returns:
            dict: API response

        Raises:
            FrekilAPIError: If the API returns an error
            FrekilClientError: If there is a client-side error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, **kwargs)

            if 400 <= response.status_code < 500:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", response.text)
                except ValueError:
                    error_message = response.text
                raise FrekilClientError(
                    f"Client error: {error_message}", response=response
                )
            elif 500 <= response.status_code < 600:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", response.text)
                except ValueError:
                    error_message = response.text
                raise FrekilAPIError(
                    f"API server error: {error_message}", response=response
                )

            if response.content:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            raise FrekilClientError(f"Request failed: {e}")

    def get(self, endpoint, params=None):
        """Convenience method for GET requests"""
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, json=None):
        """Convenience method for POST requests"""
        return self.request("POST", endpoint, data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        """Convenience method for PUT requests"""
        return self.request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint, params=None):
        """Convenience method for DELETE requests"""
        return self.request("DELETE", endpoint, params=params)

    @property
    def __version__(self):
        from . import __version__

        return __version__
