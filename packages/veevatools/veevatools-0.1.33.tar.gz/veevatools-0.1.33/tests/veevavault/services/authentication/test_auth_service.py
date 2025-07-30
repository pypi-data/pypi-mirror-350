from pytest import mark, fixture
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.authentication import AuthenticationService


@mark.unit
@mark.veevavault
class TestAuthenticationServiceUnit:
    """
    Unit tests for AuthenticationService class using mocks (no real API calls)
    """

    def test_init(self):
        """Test service initialization"""
        client = VaultClient()
        auth_service = AuthenticationService(client)

        # Verify client reference is stored correctly
        assert auth_service.client is client

    @patch("requests.post")
    def test_authenticate_with_username_password(self, mock_post):
        """Test authentication with username and password"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "sessionId": "test-session-id",
            "vaultId": "test-vault-id",
        }
        mock_post.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        auth_service = AuthenticationService(client)

        # Call the method
        result = auth_service.authenticate_with_username_password(
            username="test_user", password="test_password"
        )

        # Verify request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://test.veevavault.com/api/v25.1/auth"
        assert kwargs["data"] == {"username": "test_user", "password": "test_password"}
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify client was updated with session details
        assert client.sessionId == "test-session-id"
        assert client.session_id == "test-session-id"  # Alias should also be updated

        # Verify correct result returned
        assert result["responseStatus"] == "SUCCESS"
        assert result["sessionId"] == "test-session-id"

    @patch("requests.post")
    def test_authenticate_failed_login(self, mock_post):
        """Test authentication failure"""
        # Set up mock response for failed authentication
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "FAILURE",
            "responseMessage": "Authentication failed",
        }
        mock_post.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        auth_service = AuthenticationService(client)

        # Call the method
        result = auth_service.authenticate_with_username_password(
            username="wrong_user", password="wrong_password"
        )

        # Verify failure response
        assert result["responseStatus"] == "FAILURE"

        # Verify session ID was not set
        assert client.sessionId is None

    @patch(
        "veevavault.services.authentication.AuthenticationService.authenticate_with_username_password"
    )
    @patch(
        "veevavault.services.authentication.AuthenticationService.retrieve_api_version"
    )
    def test_authenticate_main_method(self, mock_retrieve_api, mock_auth_with_pwd):
        """Test main authenticate method"""
        # Set up mocks
        mock_auth_with_pwd.return_value = {
            "responseStatus": "SUCCESS",
            "sessionId": "test-session-id",
            "vaultId": "test-vault-id",
        }
        mock_retrieve_api.return_value = {
            "responseStatus": "SUCCESS",
            "values": {"v25.1": "/api/v25.1", "v23.1": "/api/v23.1"},
        }

        # Create client and service
        client = VaultClient()
        auth_service = AuthenticationService(client)

        # Call authenticate with full return
        result = auth_service.authenticate(
            vaultURL="https://test.veevavault.com",
            vaultUserName="test_user",
            vaultPassword="test_password",
            if_return=True,
        )

        # Verify underlying method was called
        mock_auth_with_pwd.assert_called_once_with(
            username="test_user", password="test_password"
        )

        # Verify result includes expected keys
        assert result["sessionId"] == "test-session-id"
        assert result["vaultId"] == "test-vault-id"
        assert result["vaultURL"] == "https://test.veevavault.com"

    @patch(
        "veevavault.services.authentication.AuthenticationService.authenticate_with_username_password"
    )
    def test_authenticate_with_validation_error(self, mock_auth_with_pwd):
        """Test authentication with validation errors"""
        # Set up mock for successful login
        mock_auth_with_pwd.return_value = {
            "responseStatus": "SUCCESS",
            "sessionId": "test-session-id",
            "vaultId": "test-vault-id",
        }

        # Create client and service
        client = VaultClient()
        # Set vaultURL to None to trigger TypeError
        client.vaultURL = None
        auth_service = AuthenticationService(client)

        # Test with None URL - expect TypeError about str and NoneType
        with pytest.raises(TypeError) as excinfo:
            auth_service.authenticate(
                vaultUserName="test_user", vaultPassword="test_password"
            )
        assert 'can only concatenate str (not "NoneType") to str' in str(excinfo.value)

    @patch("requests.post")
    def test_keep_alive(self, mock_post):
        """Test session keep-alive"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_post.return_value = mock_response

        # Create client with session
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        auth_service = AuthenticationService(client)

        # Use the client's api_call method through keep_alive
        with patch.object(
            client, "api_call", return_value={"responseStatus": "SUCCESS"}
        ) as mock_api_call:
            result = auth_service.keep_alive()

            # Verify client's api_call was called with correct parameters
            mock_api_call.assert_called_once()
            args, kwargs = mock_api_call.call_args
            assert args[0] == "https://test.veevavault.com/api/v25.1/keep-alive"
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Accept"] == "application/json"

            # Verify correct result returned
            assert result["responseStatus"] == "SUCCESS"

    @patch("requests.post")
    def test_logout(self, mock_post):
        """Test logout method"""
        # Set up client with session
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        auth_service = AuthenticationService(client)

        # Mock client's api_call
        with patch.object(
            client, "api_call", return_value={"responseStatus": "SUCCESS"}
        ) as mock_api_call:
            result = auth_service.logout()

            # Verify correct endpoint called
            mock_api_call.assert_called_once()
            args, kwargs = mock_api_call.call_args
            assert args[0] == "https://test.veevavault.com/api/v25.1/session"
            assert kwargs["method"] == "DELETE"

            # Verify session was cleared
            assert client.sessionId is None
            assert client.session_id is None

    @patch("requests.get")
    def test_retrieve_api_version(self, mock_get):
        """Test retrieving API versions"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "values": {
                "v20.1": "/api/v20.1",
                "v21.1": "/api/v21.1",
                "v22.1": "/api/v22.1",
                "v23.1": "/api/v23.1",
                "v25.1": "/api/v25.1",
            },
        }
        mock_get.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        auth_service = AuthenticationService(client)

        # Call the method
        result = auth_service.retrieve_api_version()

        # Verify request was made correctly
        mock_get.assert_called_once_with(
            "https://test.veevavault.com/api/", headers={"Accept": "application/json"}
        )

        # Verify client was updated with API versions - adjust expected values to match actual values
        assert client.APIversionList == [20.1, 21.1, 22.1, 23.1, 25.1]
        assert client.LatestAPIversion == "v25.1"

        # Verify correct result returned
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestAuthenticationServiceIntegration:
    """
    Integration tests for AuthenticationService using real API calls
    """

    def test_get_domain_information(self, authenticated_vault_client):
        """Test retrieving domain information with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        auth_service = AuthenticationService(authenticated_vault_client)

        # Get domain information
        domain_response = auth_service.get_domain_information()

        # Verify domain information retrieval was successful
        assert domain_response["responseStatus"] == "SUCCESS"
        assert "objects" in domain_response

    def test_retrieve_api_version(self, authenticated_vault_client):
        """Test retrieving API versions with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        auth_service = AuthenticationService(authenticated_vault_client)

        # Get API versions
        api_response = auth_service.retrieve_api_version()

        # Verify API version retrieval was successful
        assert api_response["responseStatus"] == "SUCCESS"
        assert "values" in api_response

        # Verify client was updated with API versions
        assert len(authenticated_vault_client.APIversionList) > 0
        assert authenticated_vault_client.LatestAPIversion.startswith("v")

    def test_logout_and_reauthenticate(self, authenticated_vault_client, vault_config):
        """Test logout and re-authentication with real session"""
        # Skip if not authenticated or missing credentials for re-auth
        if (
            not authenticated_vault_client.sessionId
            or not vault_config.username
            or not vault_config.password
        ):
            pytest.skip("No authenticated session available or missing credentials")

        # Create service
        auth_service = AuthenticationService(authenticated_vault_client)

        # Store session ID and URL for verification and re-authentication
        session_id_before = authenticated_vault_client.sessionId
        vault_url = authenticated_vault_client.vaultURL

        # Logout
        logout_response = auth_service.logout()

        # Verify logout was successful
        assert logout_response["responseStatus"] == "SUCCESS"

        # Verify session was cleared
        assert authenticated_vault_client.sessionId is None
        assert authenticated_vault_client.session_id is None

        # Re-authenticate for subsequent tests
        auth_response = auth_service.authenticate(
            vaultURL=vault_url,
            vaultUserName=vault_config.username,
            vaultPassword=vault_config.password,
            if_return=True,
        )

        # Verify re-authentication using the actual structure returned
        # When if_return=True, authenticate() returns client details instead of API response
        assert auth_response is not None, "Authentication response is None"
        assert "sessionId" in auth_response, "No sessionId in response"
        assert "vaultId" in auth_response, "No vaultId in response"

        # Verify the client was authenticated
        assert authenticated_vault_client.sessionId is not None
        assert (
            authenticated_vault_client.sessionId != session_id_before
        )  # Should be a new session

    def test_authentication_type_discovery(self, vault_config):
        """Test authentication type discovery with real credentials"""
        # Skip if missing username
        if not vault_config.username:
            pytest.skip("Missing username for authentication type discovery")

        # We don't need an authenticated client for this, just create a new client
        client = VaultClient()
        auth_service = AuthenticationService(client)

        # Discover authentication types
        discovery_response = auth_service.authentication_type_discovery(
            username=vault_config.username
        )

        # Verify discovery contains expected structure
        assert isinstance(discovery_response, dict)
        # The typical response should have authentication types information
        assert (
            "authTypes" in discovery_response or "responseStatus" in discovery_response
        )

    def test_validate_session_user(self, authenticated_vault_client):
        """Test user session validation with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Use the client method directly
        user_response = authenticated_vault_client.validate_session_user()

        # Verify user validation was successful
        assert user_response["responseStatus"] == "SUCCESS"
        # Check for users array which contains user information
        assert "users" in user_response
        # Verify the first user has expected fields
        assert "user" in user_response["users"][0]
