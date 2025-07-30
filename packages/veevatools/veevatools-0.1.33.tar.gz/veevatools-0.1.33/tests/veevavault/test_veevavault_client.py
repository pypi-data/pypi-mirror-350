from pytest import mark, fixture
import pytest
import json
import requests
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
class TestVaultClientUnit:
    """
    Unit tests for VaultClient class using mocks (no real API calls)
    """

    def test_init(self):
        """Test client initialization with default values"""
        client = VaultClient()

        # Verify default properties
        assert client.vaultURL is None
        assert client.vaultUserName is None
        assert client.vaultPassword is None
        assert client.sessionId is None
        assert client.vaultId is None
        assert client.LatestAPIversion == "v25.1"

    def test_session_id_property(self):
        """Test session_id property getter and setter"""
        client = VaultClient()

        # Test setter
        client.session_id = "test-session-id"

        # Verify both properties are set
        assert client.sessionId == "test-session-id"
        assert client._session_id == "test-session-id"

        # Test getter
        assert client.session_id == "test-session-id"

    @patch("requests.request")
    def test_api_call_get_success(self, mock_request):
        """Test successful GET API call"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client with basic configuration
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Make API call
        result = client.api_call("api/v25.1/test")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "GET"
        assert kwargs["url"] == "https://test.veevavault.com/api/v25.1/test"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response
        assert result == {"responseStatus": "SUCCESS"}

    @patch("requests.request")
    def test_api_call_post_with_data(self, mock_request):
        """Test POST API call with data"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client with basic configuration
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Test data
        test_data = {"param1": "value1", "param2": "value2"}

        # Make API call with POST and data
        result = client.api_call(
            "api/v25.1/object/action", method="POST", data=test_data
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["url"] == "https://test.veevavault.com/api/v25.1/object/action"
        assert kwargs["data"] == test_data

        # Verify response
        assert result == {"responseStatus": "SUCCESS"}

    @patch("requests.request")
    def test_api_call_with_custom_headers(self, mock_request):
        """Test API call with custom headers"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client with basic configuration
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Custom headers
        custom_headers = {
            "Content-Type": "application/json",
            "X-Custom-Header": "custom-value",
        }

        # Make API call with custom headers
        result = client.api_call("api/v25.1/test", headers=custom_headers)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["X-Custom-Header"] == "custom-value"
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response
        assert result == {"responseStatus": "SUCCESS"}

    @patch("requests.request")
    def test_api_call_with_raw_response(self, mock_request):
        """Test API call with raw response option"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_request.return_value = mock_response

        # Create client with basic configuration
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"

        # Make API call with raw_response=True
        result = client.api_call("api/v25.1/test", raw_response=True)

        # Verify raw response is returned
        assert result == mock_response
        # Verify json() was not called
        mock_response.json.assert_not_called()

    @patch("requests.request")
    def test_api_call_error_handling(self, mock_request):
        """Test API call error handling"""
        # Set up mock to raise HTTPError
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found"
        )
        mock_request.return_value = mock_response

        # Create client with basic configuration
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"

        # Make API call that should raise exception
        with pytest.raises(Exception) as exc_info:
            client.api_call("api/v25.1/nonexistent")

        # Verify correct exception message
        assert "HTTP error occurred" in str(exc_info.value)

    @patch("veevavault.services.authentication.AuthenticationService")
    def test_authenticate_delegation(self, mock_auth_service):
        """Test authenticate method delegates to AuthenticationService"""
        # Set up mock authentication service
        mock_auth_instance = MagicMock()
        mock_auth_instance.authenticate.return_value = {"responseStatus": "SUCCESS"}
        mock_auth_service.return_value = mock_auth_instance

        # Create client and call authenticate
        client = VaultClient()
        result = client.authenticate(
            vaultURL="https://test.veevavault.com",
            vaultUserName="test_user",
            vaultPassword="test_password",
        )

        # Verify authentication service was called correctly
        mock_auth_instance.authenticate.assert_called_once_with(
            vaultURL="https://test.veevavault.com",
            vaultUserName="test_user",
            vaultPassword="test_password",
            sessionId=None,
            vaultId=None,
            if_return=False,
        )

        # Verify result is passed through
        assert result == {"responseStatus": "SUCCESS"}


@mark.integration
@mark.veevavault
class TestVaultClientIntegration:
    """
    Integration tests for VaultClient class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_authenticate(self, vault_client, vault_config):
        """Test authentication with real credentials"""
        # Skip if running in mock mode
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Authenticate with real credentials
        response = vault_client.authenticate(
            vaultURL=vault_config.url,
            vaultUserName=vault_config.username,
            vaultPassword=vault_config.password,
            if_return=True,
        )

        # Verify authentication was successful
        assert vault_client.sessionId is not None
        assert response["sessionId"] is not None

    def test_session_keep_alive(self, authenticated_vault_client):
        """Test session keep-alive with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Call session keep-alive
        response = authenticated_vault_client.session_keep_alive()

        # Verify keep-alive was successful
        assert response["responseStatus"] == "SUCCESS"

    def test_validate_session_user(self, authenticated_vault_client):
        """Test validate session user with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Validate session user
        response = authenticated_vault_client.validate_session_user()

        # Verify validation was successful
        assert response["responseStatus"] == "SUCCESS"
        # Check for users array which contains user information
        assert "users" in response
        # Verify the first user has expected fields
        assert "user" in response["users"][0]
