from pytest import mark, fixture
import pytest
import requests
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.documents.attachments_service import DocumentAttachmentsService


@mark.unit
@mark.veevavault
class TestDocumentAttachmentsServiceUnit:
    """
    Unit tests for DocumentAttachmentsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_determine_if_document_has_attachments(self, mock_request):
        """Test determine_if_document_has_attachments method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "document": {"id": "123", "name": "Test Document"},
            "attachments": [
                {
                    "id": 566,
                    "url": "https://test.veevavault.com/api/v25.1/objects/documents/123/attachments/566",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAttachmentsService(client)

        # Call method to test
        result = service.determine_if_document_has_attachments("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["attachments"]) == 1
        assert result["attachments"][0]["id"] == 566

    @patch("requests.request")
    def test_retrieve_document_attachments(self, mock_request):
        """Test retrieve_document_attachments method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": 566,
                    "filename__v": "Test Attachment.pdf",
                    "format__v": "application/pdf",
                    "size__v": 12345,
                    "md5checksum__v": "abcdef1234567890",
                    "version__v": 1,
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAttachmentsService(client)

        # Call method to test
        result = service.retrieve_document_attachments("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/attachments")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"][0]["id"] == 566
        assert result["data"][0]["filename__v"] == "Test Attachment.pdf"

    @patch("requests.request")
    def test_download_document_attachment(self, mock_request):
        """Test download_document_attachment method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"test file content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAttachmentsService(client)

        # Call method to test
        result = service.download_document_attachment("123", "456")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/attachments/456/file"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "*/*"

        # Verify response
        assert result == b"test file content"

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_create_document_attachment(self, mock_file, mock_request):
        """Test create_document_attachment method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {"id": "567", "version__v": 1},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentAttachmentsService(client)

        # Call method to test
        result = service.create_document_attachment("123", "test_file.pdf")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/attachments")
        assert kwargs["method"] == "POST"
        assert "files" in kwargs

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"]["id"] == "567"
        assert result["data"]["version__v"] == 1


@mark.integration
@mark.veevavault
class TestDocumentAttachmentsServiceIntegration:
    """
    Integration tests for DocumentAttachmentsService using real API calls
    """

    def test_document_attachments_service(self, authenticated_vault_client):
        """Test basic attachments service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentAttachmentsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(reason="Requires document with attachments to test")
    def test_retrieve_document_attachments_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document attachments with real API"""
        # This test would require a document with attachments to properly test
        pass
