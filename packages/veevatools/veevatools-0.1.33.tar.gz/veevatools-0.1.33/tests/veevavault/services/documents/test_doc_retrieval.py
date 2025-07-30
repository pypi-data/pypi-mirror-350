# tests/veevavault/services/documents/test_doc_retrieval.py
from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents import DocumentService


@mark.unit
@mark.veevavault
class TestDocumentRetrievalServiceUnit:
    """
    Unit tests for DocumentService retrieval functionality using mocks
    """

    @patch("requests.request")
    def test_document_service_retrieve(self, mock_request):
        """Test DocumentService retrieval_service.retrieve_document method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "document": {
                "id": "123",
                "name": "Test Document",
                "type": "test_doc_type__v",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Create service with mocked client
        doc_service = DocumentService(client)

        # Call method to test - note the service structure where retrieve_document is in the retrieval sub-service
        result = doc_service.retrieval.retrieve_document("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["document"]["id"] == "123"
        assert result["document"]["name"] == "Test Document"


@mark.integration
@mark.veevavault
class TestDocumentRetrievalServiceIntegration:
    """
    Integration tests for DocumentService retrieval using real API calls
    """

    def test_document_service(self, authenticated_vault_client, vault_config):
        """Test basic document service methods with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        doc_service = DocumentService(authenticated_vault_client)

        # This is just a placeholder for real document retrieval tests
        # You would implement actual document retrieval tests here
        assert doc_service is not None
        assert doc_service.client is authenticated_vault_client
