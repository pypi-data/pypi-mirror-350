from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderRelationshipsService


@mark.unit
@mark.veevavault
class TestBinderRelationshipsServiceUnit:
    """
    Unit tests for BinderRelationshipsService using mocks
    """

    def test_retrieve_binder_relationship(self):
        """Test retrieving a specific relationship for a binder version"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "rel_123",
                "source_doc_id": "binder_456",
                "relationship_type__v": "supporting__v",
                "created_by__v": "user_789",
                "created_date__v": "2023-01-01T12:00:00Z",
                "target_doc_id__v": "doc_101",
                "target_major_version__v": 1,
                "target_minor_version__v": 0,
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            relationships_service = BinderRelationshipsService(client)

            # Call method to test
            result = relationships_service.retrieve_binder_relationship(
                binder_id="456",
                major_version=1,
                minor_version=0,
                relationship_id="rel_123",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/456/versions/1/0/relationships/rel_123"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "rel_123"
            assert result["relationship_type__v"] == "supporting__v"
            assert result["target_doc_id__v"] == "doc_101"

    def test_create_binder_relationship(self):
        """Test creating a relationship between a binder version and a document"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "rel_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            relationships_service = BinderRelationshipsService(client)

            # Call method to test
            result = relationships_service.create_binder_relationship(
                binder_id="456",
                major_version=1,
                minor_version=0,
                target_doc_id="doc_101",
                relationship_type="supporting__v",
                target_major_version=2,
                target_minor_version=0,
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/456/versions/1/0/relationships"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )

            # Verify data
            assert kwargs["data"]["target_doc_id__v"] == "doc_101"
            assert kwargs["data"]["relationship_type__v"] == "supporting__v"
            assert kwargs["data"]["target_major_version__v"] == 2
            assert kwargs["data"]["target_minor_version__v"] == 0

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "rel_123"

    def test_create_binder_relationship_without_target_version(self):
        """Test creating a relationship without specifying target version (applies to all versions)"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "rel_124",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            relationships_service = BinderRelationshipsService(client)

            # Call method to test without target versions
            result = relationships_service.create_binder_relationship(
                binder_id="456",
                major_version=1,
                minor_version=0,
                target_doc_id="doc_101",
                relationship_type="supporting__v",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args

            # Verify data doesn't include target version parameters
            assert "target_major_version__v" not in kwargs["data"]
            assert "target_minor_version__v" not in kwargs["data"]

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "rel_124"

    def test_delete_binder_relationship(self):
        """Test deleting a relationship from a binder version"""
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
            relationships_service = BinderRelationshipsService(client)

            # Call method to test
            result = relationships_service.delete_binder_relationship(
                binder_id="456",
                major_version=1,
                minor_version=0,
                relationship_id="rel_123",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/456/versions/1/0/relationships/rel_123"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestBinderRelationshipsServiceIntegration:
    """
    Integration tests for BinderRelationshipsService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_binder_relationship(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving a binder relationship with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        relationships_service = BinderRelationshipsService(authenticated_vault_client)

        # Skip - requires existing binder, version, and relationship
        pytest.skip(
            "Skipping as it requires an existing binder, version, and relationship ID."
        )

    def test_create_and_delete_binder_relationship(
        self, authenticated_vault_client, vault_config
    ):
        """Test creating and then deleting a binder relationship with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        relationships_service = BinderRelationshipsService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder and document IDs."
        )
