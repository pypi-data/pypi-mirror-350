from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.signatures_service import DocumentSignaturesService


@mark.unit
@mark.veevavault
class TestDocumentSignaturesServiceUnit:
    """
    Unit tests for DocumentSignaturesService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_signature_metadata(self, mock_request):
        """Test retrieve_document_signature_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "signature_meaning__v": {
                    "type": "picklist",
                    "label": "Signature Meaning",
                },
                "signature_date__v": {"type": "datetime", "label": "Signature Date"},
                "signature_user__v": {
                    "type": "objectReference",
                    "label": "Signature User",
                    "objectType": "user__sys",
                },
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentSignaturesService(client)

        # Call method to test
        result = service.retrieve_document_signature_metadata()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/query/documents/relationships/document_signature__sysr"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "signature_meaning__v" in result["properties"]
        assert "signature_date__v" in result["properties"]
        assert "signature_user__v" in result["properties"]
        assert result["properties"]["signature_user__v"]["objectType"] == "user__sys"

    @patch("requests.request")
    def test_retrieve_archived_document_signature_metadata(self, mock_request):
        """Test retrieve_archived_document_signature_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "signature_meaning__v": {
                    "type": "picklist",
                    "label": "Signature Meaning",
                },
                "signature_date__v": {"type": "datetime", "label": "Signature Date"},
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentSignaturesService(client)

        # Call method to test
        result = service.retrieve_archived_document_signature_metadata()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/query/archived_documents/relationships/document_signature__sysr"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "signature_meaning__v" in result["properties"]
        assert "signature_date__v" in result["properties"]


@mark.integration
@mark.veevavault
class TestDocumentSignaturesServiceIntegration:
    """
    Integration tests for DocumentSignaturesService using real API calls
    """

    def test_document_signatures_service(self, authenticated_vault_client):
        """Test basic signatures service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentSignaturesService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_retrieve_document_signature_metadata_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document signature metadata with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentSignaturesService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_document_signature_metadata()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
