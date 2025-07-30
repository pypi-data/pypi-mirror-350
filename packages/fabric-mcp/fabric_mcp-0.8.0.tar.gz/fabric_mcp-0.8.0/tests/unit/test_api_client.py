"""Unit tests for fabric_mcp.api_client module."""

import os
from unittest.mock import Mock, patch

import httpx
import pytest
from httpx_retries import RetryTransport

from fabric_mcp.api_client import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, FabricApiClient


class TestFabricApiClient:
    """Test cases for FabricApiClient class."""

    def test_init_with_defaults(self):
        """Test client initialization with default values."""
        client = FabricApiClient()

        assert client.base_url == DEFAULT_BASE_URL
        assert client.api_key is None
        assert client.timeout == DEFAULT_TIMEOUT
        assert isinstance(client.client, httpx.Client)

    def test_init_with_parameters(self):
        """Test client initialization with explicit parameters."""
        base_url = "http://example.com:9000"
        api_key = "test-api-key"
        timeout = 60

        client = FabricApiClient(base_url=base_url, api_key=api_key, timeout=timeout)

        assert client.base_url == base_url
        assert client.api_key == api_key
        assert client.timeout == timeout

    @patch.dict(
        os.environ,
        {"FABRIC_BASE_URL": "http://env.example.com", "FABRIC_API_KEY": "env-key"},
    )
    def test_init_with_environment_variables(self):
        """Test client initialization using environment variables."""
        client = FabricApiClient()

        assert client.base_url == "http://env.example.com"
        assert client.api_key == "env-key"

    def test_init_parameters_override_environment(self):
        """Test that explicit parameters override environment variables."""
        with patch.dict(
            os.environ,
            {"FABRIC_BASE_URL": "http://env.example.com", "FABRIC_API_KEY": "env-key"},
        ):
            client = FabricApiClient(
                base_url="http://param.example.com", api_key="param-key"
            )

            assert client.base_url == "http://param.example.com"
            assert client.api_key == "param-key"

    def test_init_without_api_key_logs_warning(self, caplog: pytest.LogCaptureFixture):
        """Test that initialization without API key logs a warning."""
        with patch.dict(os.environ, {}, clear=True):
            FabricApiClient()

            assert "Fabric API key not provided" in caplog.text

    def test_init_with_api_key_no_warning(self, caplog: pytest.LogCaptureFixture):
        """Test that initialization with API key doesn't log warning."""
        FabricApiClient(api_key="test-key")

        assert "Fabric API key not provided" not in caplog.text

    def test_client_configuration(self):
        """Test that httpx client is properly configured."""
        client = FabricApiClient(api_key="test-key")

        # Check headers
        assert "User-Agent" in client.client.headers
        assert "FabricMCPClient" in client.client.headers["User-Agent"]
        assert client.client.headers[FabricApiClient.FABRIC_API_HEADER] == "test-key"

        # Check timeout - httpx uses Timeout objects
        assert client.client.timeout.read == DEFAULT_TIMEOUT

        # Check base URL - httpx normalizes URLs
        assert str(client.client.base_url) == DEFAULT_BASE_URL

        # Check that retry transport is configured
        transport = getattr(client.client, "_transport")
        assert isinstance(transport, RetryTransport)

    def test_client_without_api_key_no_header(self):
        """Test that client without API key doesn't set auth header."""
        with patch.dict(os.environ, {}, clear=True):
            client = FabricApiClient()

            assert FabricApiClient.FABRIC_API_HEADER not in client.client.headers

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_basic(self, mock_client_class: Mock):
        """Test basic _request method functionality."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        request_method = getattr(client, "_request")
        result = request_method("GET", "/test")

        assert result == mock_response
        mock_client.request.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_with_all_parameters(self, mock_client_class: Mock):
        """Test _request method with all parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        params = {"param1": "value1"}
        json_data = {"key": "value"}
        headers = {"Custom-Header": "value"}

        # pylint: disable=protected-access
        request_method = getattr(client, "_request")
        result = request_method(
            "POST", "/test", params=params, json_data=json_data, headers=headers
        )

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/test"
        assert call_args[1]["params"] == params
        assert call_args[1]["json"] == json_data
        assert "Custom-Header" in call_args[1]["headers"]

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_masks_sensitive_headers_in_logs(
        self, mock_client_class: Mock, caplog: pytest.LogCaptureFixture
    ):
        """Test that sensitive headers are masked in debug logs."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {FabricApiClient.FABRIC_API_HEADER: "secret-key"}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()

        with caplog.at_level("DEBUG"):
            # pylint: disable=protected-access
            request_method = getattr(client, "_request")
            request_method("GET", "/test")

        # Check that the secret is masked in logs
        log_text = caplog.text
        assert "secret-key" not in log_text
        assert "***REDACTED***" in log_text

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_handles_request_error(self, mock_client_class: Mock):
        """Test _request method handles httpx.RequestError."""
        mock_client = Mock()
        mock_client.request.side_effect = httpx.RequestError("Connection failed")
        mock_client.headers = {}
        mock_client_class.return_value = mock_client
        client = FabricApiClient()

        with pytest.raises(httpx.RequestError):
            # pylint: disable=protected-access
            request_method = getattr(client, "_request")
            request_method("GET", "/test")

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_handles_http_status_error(self, mock_client_class: Mock):
        """Test _request method handles httpx.HTTPStatusError."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=Mock(), response=mock_response
        )
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client
        client = FabricApiClient()

        with pytest.raises(httpx.HTTPStatusError):
            # pylint: disable=protected-access
            request_method = getattr(client, "_request")
            request_method("GET", "/test")

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_get_method(self, mock_client_class: Mock):
        """Test GET convenience method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        params = {"param1": "value1"}

        result = client.get("/test", params=params)

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["method"] == "GET"
        assert call_args[1]["params"] == params

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_post_method(self, mock_client_class: Mock):
        """Test POST convenience method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 201
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        json_data = {"key": "value"}

        result = client.post("/test", json_data=json_data)

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["json"] == json_data

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_put_method(self, mock_client_class: Mock):
        """Test PUT convenience method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        json_data = {"key": "updated_value"}

        result = client.put("/test", json_data=json_data)

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["method"] == "PUT"
        assert call_args[1]["json"] == json_data

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_delete_method(self, mock_client_class: Mock):
        """Test DELETE convenience method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 204
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client

        client = FabricApiClient()

        result = client.delete("/test")

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["method"] == "DELETE"

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_close_method(self, mock_client_class: Mock):
        """Test close method."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        client = FabricApiClient()
        client.close()

        mock_client.close.assert_called_once()

    def test_redacted_headers_constant(self):
        """Test that REDACTED_HEADERS contains expected headers."""
        expected_headers = ["Authorization", FabricApiClient.FABRIC_API_HEADER]
        assert FabricApiClient.REDACTED_HEADERS == expected_headers

    def test_fabric_api_header_constant(self):
        """Test that FABRIC_API_HEADER has expected value."""
        assert FabricApiClient.FABRIC_API_HEADER == "X-API-Key"

    @patch("fabric_mcp.api_client.httpx.Client")
    def test_request_method_with_raw_data(self, mock_client_class: Mock):
        """Test _request method with raw data parameter."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response
        mock_client.headers = {}
        mock_client_class.return_value = mock_client
        client = FabricApiClient()

        # Test with raw data (not json_data) to hit line 127
        # pylint: disable=protected-access
        request_method = getattr(client, "_request")
        result = request_method("POST", "/test", data=b"raw data")

        assert result == mock_response
        call_args = mock_client.request.call_args
        assert call_args[1]["data"] == b"raw data"
