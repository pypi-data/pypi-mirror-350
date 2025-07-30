from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderDeletionService


@mark.unit
@mark.veevavault
class TestBinderDeletionServiceUnit:
    """
    Unit tests for BinderDeletionService using mocks
    """

    def test_delete_binder(self):
        """Test deleting a binder"""
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
            deletion_service = BinderDeletionService(client)

            # Call method to test
            result = deletion_service.delete_binder("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "123"}

    def test_delete_binder_version(self):
        """Test deleting a specific version of a binder"""
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
            deletion_service = BinderDeletionService(client)

            # Call method to test
            result = deletion_service.delete_binder_version("123", 0, 1)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/versions/0/1"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "123"}


@mark.integration
@mark.veevavault
class TestBinderDeletionServiceIntegration:
    """
    Integration tests for BinderDeletionService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_delete_binder(self, authenticated_vault_client, vault_config):
        """Test deleting a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        deletion_service = BinderDeletionService(authenticated_vault_client)

        # Skip - would delete actual data
        pytest.skip(
            "Skipping to prevent deleting data in production. Requires existing binder ID."
        )

    def test_delete_binder_version(self, authenticated_vault_client, vault_config):
        """Test deleting a binder version with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        deletion_service = BinderDeletionService(authenticated_vault_client)

        # Skip - would delete actual data
        pytest.skip(
            "Skipping to prevent deleting data in production. Requires existing binder ID and version."
        )
