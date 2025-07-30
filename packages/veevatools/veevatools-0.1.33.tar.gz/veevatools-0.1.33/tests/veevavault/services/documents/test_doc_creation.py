from pytest import mark, fixture
import pytest
import requests
import json
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.documents.creation_service import DocumentCreationService


@mark.unit
@mark.veevavault
class TestDocumentCreationServiceUnit:
    """
    Unit tests for DocumentCreationService using mocks (no real API calls)
    """

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_create_single_document(self, mock_file, mock_request):
        """Test create_single_document method with file upload"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "successfully created document",
            "id": 773,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentCreationService(client)

        # Call method to test with file
        result = service.create_single_document(
            file_path="test_doc.pdf",
            name_v="Test Document",
            type_v="test_doc_type__v",
            lifecycle_v="test_lifecycle__v",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents")
        assert kwargs["method"] == "POST"
        assert "files" in kwargs

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 773

    @patch("requests.request")
    def test_create_single_document_placeholder(self, mock_request):
        """Test create_single_document method for placeholder document"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "successfully created document",
            "id": 774,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentCreationService(client)

        # Call method to test without file (placeholder)
        result = service.create_single_document(
            name_v="Test Placeholder",
            type_v="test_doc_type__v",
            lifecycle_v="test_lifecycle__v",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents")
        assert kwargs["method"] == "POST"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 774

    @patch("requests.request")
    def test_create_multiple_documents(self, mock_request):
        """Test create_multiple_documents method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {"responseStatus": "SUCCESS", "id": 771, "external_id__v": "DOC-001"},
                {"responseStatus": "SUCCESS", "id": 772, "external_id__v": "DOC-002"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentCreationService(client)

        # Test CSV data
        csv_data = """name__v,type__v,lifecycle__v,external_id__v
        Test Document 1,test_doc_type__v,test_lifecycle__v,DOC-001
        Test Document 2,test_doc_type__v,test_lifecycle__v,DOC-002"""

        # Call method to test
        result = service.create_multiple_documents(csv_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/batch")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 771
        assert result["data"][1]["id"] == 772

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_create_single_document_version(self, mock_file, mock_request):
        """Test create_single_document_version method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentCreationService(client)

        # Call method to test
        result = service.create_single_document_version(
            doc_id="123",
            create_draft=True,
            file_path="test_doc_v2.pdf",
            description="Version 0.2",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/versions")
        assert kwargs["method"] == "POST"
        assert kwargs["params"]["draft"] == "true"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["major_version_number__v"] == 0
        assert result["minor_version_number__v"] == 2


@mark.integration
@mark.veevavault
class TestDocumentCreationServiceIntegration:
    """
    Integration tests for DocumentCreationService using real API calls
    """

    def test_document_creation_service(self, authenticated_vault_client):
        """Test basic creation service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentCreationService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Creating documents in integration tests requires specific permissions and cleanup"
    )
    def test_create_document_integration(self, authenticated_vault_client):
        """Test creating a document with real API"""
        # This test would create real documents which might not be desired in automated tests
        pass
