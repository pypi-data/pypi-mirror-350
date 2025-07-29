"""
Tests for the FrekilClient class
"""
import unittest
from unittest import mock

from frekil import FrekilClient
from frekil.exceptions import FrekilClientError, FrekilAPIError


class TestFrekilClient(unittest.TestCase):
    """Tests for the FrekilClient class"""

    def setUp(self):
        """Set up a client instance for each test"""
        self.api_key = "test-api-key"
        self.client = FrekilClient(api_key=self.api_key)

    def test_init(self):
        """Test that the client is initialized correctly"""
        self.assertEqual(self.client.auth.api_key, self.api_key)
        self.assertEqual(self.client.base_url, "https://prod.notatehq.com/api/sdk")

        # Test custom base URL
        custom_url = "https://staging.notatehq.com/api/sdk"
        client = FrekilClient(api_key=self.api_key, base_url=custom_url)
        self.assertEqual(client.base_url, custom_url)

        # Test base URL normalization
        client = FrekilClient(
            api_key=self.api_key, base_url="https://prod.notatehq.com/api/sdk/"
        )
        self.assertEqual(client.base_url, "https://prod.notatehq.com/api/sdk")

    def test_headers(self):
        """Test that the client sets the correct headers"""
        session = self.client.session
        self.assertEqual(session.headers["X-API-Key"], self.api_key)
        self.assertEqual(session.headers["Content-Type"], "application/json")
        self.assertEqual(session.headers["Accept"], "application/json")
        self.assertTrue(session.headers["User-Agent"].startswith("frekil-python-sdk/"))

    @mock.patch("requests.Session.request")
    def test_request_success(self, mock_request):
        """Test successful request"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"key": "value"}'
        mock_response.json.return_value = {"key": "value"}
        mock_request.return_value = mock_response

        result = self.client.request("GET", "test-endpoint")

        mock_request.assert_called_once_with(
            "GET", "https://prod.notatehq.com/api/sdk/test-endpoint"
        )
        self.assertEqual(result, {"key": "value"})

    @mock.patch("requests.Session.request")
    def test_request_client_error(self, mock_request):
        """Test client error handling"""
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid request"}
        mock_request.return_value = mock_response

        with self.assertRaises(FrekilClientError):
            self.client.request("GET", "test-endpoint")

    @mock.patch("requests.Session.request")
    def test_request_server_error(self, mock_request):
        """Test server error handling"""
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_request.return_value = mock_response

        with self.assertRaises(FrekilAPIError):
            self.client.request("GET", "test-endpoint")

    @mock.patch("frekil.client.FrekilClient.request")
    def test_convenience_methods(self, mock_request):
        """Test convenience methods"""
        mock_request.return_value = {"key": "value"}

        # Test GET
        self.client.get("test-endpoint", params={"param": "value"})
        mock_request.assert_called_with(
            "GET", "test-endpoint", params={"param": "value"}
        )

        # Test POST
        self.client.post("test-endpoint", json={"data": "value"})
        mock_request.assert_called_with(
            "POST", "test-endpoint", data=None, json={"data": "value"}
        )

        # Test PUT
        self.client.put("test-endpoint", json={"data": "value"})
        mock_request.assert_called_with(
            "PUT", "test-endpoint", data=None, json={"data": "value"}
        )

        # Test DELETE
        self.client.delete("test-endpoint", params={"param": "value"})
        mock_request.assert_called_with(
            "DELETE", "test-endpoint", params={"param": "value"}
        )


if __name__ == "__main__":
    unittest.main()
