from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderUpdateService


@mark.unit
@mark.veevavault
class TestBinderUpdateServiceUnit:
    """
    Unit tests for BinderUpdateService using mocks
    """

    def test_update_binder(self):
        """Test updating an existing binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "123"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            update_service = BinderUpdateService(client)

            # Test data
            update_data = {"name__v": "Updated Binder Name", "status__v": "active__v"}

            # Call method to test
            result = update_service.update_binder("123", update_data)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == update_data

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "123"

    def test_reclassify_binder(self):
        """Test reclassifying a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "123"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            update_service = BinderUpdateService(client)

            # Test data
            reclassify_data = {
                "type__v": "new_type__v",
                "subtype__v": "new_subtype__v",
                "lifecycle__v": "new_lifecycle__v",
            }

            # Call method to test
            result = update_service.reclassify_binder("123", reclassify_data)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )

            # Verify reclassify=true was added to the data
            assert kwargs["data"]["reclassify"] == "true"
            assert kwargs["data"]["type__v"] == "new_type__v"
            assert kwargs["data"]["subtype__v"] == "new_subtype__v"
            assert kwargs["data"]["lifecycle__v"] == "new_lifecycle__v"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "123"

    def test_update_binder_version(self):
        """Test updating a specific version of a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "123"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            update_service = BinderUpdateService(client)

            # Test data
            update_data = {
                "name__v": "Updated Version Name",
                "description__v": "Updated description for version 1.0",
            }

            # Call method to test
            result = update_service.update_binder_version("123", 1, 0, update_data)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/versions/1/0"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == update_data

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "123"

    def test_refresh_binder_auto_filing(self):
        """Test refreshing the auto-filing rules for an eTMF binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            update_service = BinderUpdateService(client)

            # Call method to test
            result = update_service.refresh_binder_auto_filing("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/actions"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"]["action"] == "refresh_auto_filing"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestBinderUpdateServiceIntegration:
    """
    Integration tests for BinderUpdateService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_update_binder(self, authenticated_vault_client, vault_config):
        """Test updating a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        update_service = BinderUpdateService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder ID."
        )

    def test_update_binder_version(self, authenticated_vault_client, vault_config):
        """Test updating a binder version with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        update_service = BinderUpdateService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder ID and version."
        )

    def test_refresh_binder_auto_filing(self, authenticated_vault_client, vault_config):
        """Test refreshing auto-filing with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        update_service = BinderUpdateService(authenticated_vault_client)

        # Skip - would modify actual data and specific to eTMF Vaults
        pytest.skip(
            "Skipping to prevent modifying data in production. Only applicable for eTMF Vaults."
        )
