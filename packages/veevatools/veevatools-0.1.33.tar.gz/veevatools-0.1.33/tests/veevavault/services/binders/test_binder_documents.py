from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderDocumentsService


@mark.unit
@mark.veevavault
class TestBinderDocumentsServiceUnit:
    """
    Unit tests for BinderDocumentsService using mocks
    """

    def test_add_document_to_binder(self):
        """Test adding a document to a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "node_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            documents_service = BinderDocumentsService(client)

            # Call method to test
            result = documents_service.add_document_to_binder(
                binder_id="123",
                document_id="456",
                parent_id="section_789",
                order=1,
                binding_rule="current",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/documents"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )

            # Verify data includes all parameters
            assert kwargs["data"]["document_id__v"] == "456"
            assert kwargs["data"]["parent_id__v"] == "section_789"
            assert kwargs["data"]["order__v"] == 1
            assert kwargs["data"]["binding_rule__v"] == "current"

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "node_123"}

    def test_add_document_to_binder_with_specific_version(self):
        """Test adding a document with specific version binding rule to a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "node_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            documents_service = BinderDocumentsService(client)

            # Call method to test with specific version binding
            result = documents_service.add_document_to_binder(
                binder_id="123",
                document_id="456",
                binding_rule="specific",
                major_version_number=1,
                minor_version_number=0,
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/documents"
            )
            assert kwargs["method"] == "POST"

            # Verify data includes all parameters including version numbers
            assert kwargs["data"]["document_id__v"] == "456"
            assert kwargs["data"]["binding_rule__v"] == "specific"
            assert kwargs["data"]["major_version_number__v"] == 1
            assert kwargs["data"]["minor_version_number__v"] == 0

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "node_123"}

    def test_move_document_in_binder(self):
        """Test moving a document to a different position within a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "node_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            documents_service = BinderDocumentsService(client)

            # Call method to test
            result = documents_service.move_document_in_binder(
                binder_id="123", section_id="node_456", order=3, parent_id="section_789"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/documents/node_456"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )

            # Verify data
            assert kwargs["data"]["order__v"] == 3
            assert kwargs["data"]["parent_id__v"] == "section_789"

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "node_123"}

    def test_remove_document_from_binder(self):
        """Test removing a document from a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "node_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            documents_service = BinderDocumentsService(client)

            # Call method to test
            result = documents_service.remove_document_from_binder(
                binder_id="123", section_id="node_456"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/documents/node_456"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "node_123"}


@mark.integration
@mark.veevavault
class TestBinderDocumentsServiceIntegration:
    """
    Integration tests for BinderDocumentsService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_add_document_to_binder(self, authenticated_vault_client, vault_config):
        """Test adding a document to a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        documents_service = BinderDocumentsService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder and document IDs."
        )

    def test_move_document_in_binder(self, authenticated_vault_client, vault_config):
        """Test moving a document within a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        documents_service = BinderDocumentsService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder and document node IDs."
        )

    def test_remove_document_from_binder(
        self, authenticated_vault_client, vault_config
    ):
        """Test removing a document from a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        documents_service = BinderDocumentsService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder and document node IDs."
        )
