from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.annotations_service import DocumentAnnotationsService


@mark.unit
@mark.veevavault
class TestDocumentAnnotationsServiceUnit:
    """
    Unit tests for DocumentAnnotationsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_annotation_type_metadata(self, mock_request):
        """Test retrieve_annotation_type_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {"data": "test"},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAnnotationsService(client)

        # Call method to test
        result = service.retrieve_annotation_type_metadata("note__sys")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/annotations/types/note__sys"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["properties"] == {"data": "test"}

    @patch("requests.request")
    def test_create_document_annotations_batch(self, mock_request):
        """Test create_document_annotations_batch method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "anno_001"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAnnotationsService(client)

        # Test data
        annotation_data = [
            {
                "type__sys": "note__sys",
                "document_version_id__sys": "123",
                "placemark": {"type__sys": "sticky__sys", "page__sys": 1},
            }
        ]

        # Call method to test
        result = service.create_document_annotations_batch(annotation_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/annotations/batch")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"][0]["id"] == "anno_001"

    @patch("requests.request")
    def test_retrieve_document_annotations(self, mock_request):
        """Test retrieve_document_annotations method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "annotations": [{"id": "anno_001", "type__sys": "note__sys"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAnnotationsService(client)

        # Call method to test
        result = service.retrieve_document_annotations("doc_123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/doc_123/annotations"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["annotations"][0]["id"] == "anno_001"


@mark.integration
@mark.veevavault
class TestDocumentAnnotationsServiceIntegration:
    """
    Integration tests for DocumentAnnotationsService using real API calls
    """

    def test_document_annotations_service(self, authenticated_vault_client):
        """Test basic annotations service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentAnnotationsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        # Actual API calls would be tested in specific test methods
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(reason="Requires document with annotations to test")
    def test_retrieve_document_annotations_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document annotations with real API"""
        # This test would require a document with annotations to properly test
        pass
