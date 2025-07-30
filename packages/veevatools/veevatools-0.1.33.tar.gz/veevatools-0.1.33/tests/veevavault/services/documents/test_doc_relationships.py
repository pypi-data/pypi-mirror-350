from pytest import mark, fixture
import pytest
import requests
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.relationships_service import (
    DocumentRelationshipsService,
)


@mark.unit
@mark.veevavault
class TestDocumentRelationshipsServiceUnit:
    """
    Unit tests for DocumentRelationshipsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_type_relationships(self, mock_request):
        """Test retrieve_document_type_relationships method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "relationship_type": {"type": "picklist", "label": "Relationship Type"}
            },
            "relationshipTypes": [
                {"value": "supporting_document__v", "label": "Supporting Document"}
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRelationshipsService(client)

        # Call method to test
        result = service.retrieve_document_type_relationships("promotional__c")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/types/promotional__c/relationships"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "relationshipTypes" in result
        assert len(result["relationshipTypes"]) == 1
        assert result["relationshipTypes"][0]["value"] == "supporting_document__v"

    @patch("requests.request")
    def test_retrieve_document_relationships(self, mock_request):
        """Test retrieve_document_relationships method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "relationships": [
                {
                    "id": "rel_123",
                    "relationship_type": "supporting_document__v",
                    "target_doc_id": 456,
                    "target_doc_name": "Supporting Document",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRelationshipsService(client)

        # Call method to test
        result = service.retrieve_document_relationships("123", 0, 1)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/versions/0/1/relationships"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "relationships" in result
        assert len(result["relationships"]) == 1
        assert result["relationships"][0]["id"] == "rel_123"
        assert result["relationships"][0]["target_doc_id"] == 456

    @patch("requests.request")
    def test_create_document_relationship(self, mock_request):
        """Test create_document_relationship method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "rel_123"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRelationshipsService(client)

        # Call method to test
        result = service.create_document_relationship(
            doc_id="123",
            major_version=0,
            minor_version=1,
            target_doc_id="456",
            relationship_type="supporting_document__v",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/versions/0/1/relationships"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert json.loads(kwargs["data"]) == {
            "target_doc_id": "456",
            "relationship_type": "supporting_document__v",
        }

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "rel_123"

    @patch("requests.request")
    def test_delete_document_relationship(self, mock_request):
        """Test delete_document_relationship method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "rel_123"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRelationshipsService(client)

        # Call method to test
        result = service.delete_document_relationship("123", 0, 1, "rel_123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/versions/0/1/relationships/rel_123"
        )
        assert kwargs["method"] == "DELETE"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "rel_123"


@mark.integration
@mark.veevavault
class TestDocumentRelationshipsServiceIntegration:
    """
    Integration tests for DocumentRelationshipsService using real API calls
    """

    def test_document_relationships_service(self, authenticated_vault_client):
        """Test basic relationships service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentRelationshipsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(reason="Requires specific document type in the Vault to test")
    def test_retrieve_document_type_relationships_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document type relationships with real API"""
        pass
