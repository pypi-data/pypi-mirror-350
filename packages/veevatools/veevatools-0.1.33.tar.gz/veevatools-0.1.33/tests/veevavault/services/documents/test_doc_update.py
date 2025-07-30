from pytest import mark, fixture
import pytest
import requests
import json
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.documents.update_service import DocumentUpdateService


@mark.unit
@mark.veevavault
class TestDocumentUpdateServiceUnit:
    """
    Unit tests for DocumentUpdateService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_update_single_document(self, mock_request):
        """Test update_single_document method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentUpdateService(client)

        # Update data
        data = {
            "name__v": "Updated Document Name",
            "description__v": "Updated description",
        }

        # Call method to test
        result = service.update_single_document(123, data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert json.loads(kwargs["data"]) == data

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    def test_update_multiple_documents(self, mock_request):
        """Test update_multiple_documents method with JSON data"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {"responseStatus": "SUCCESS", "id": 123},
                {"responseStatus": "SUCCESS", "id": 456},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentUpdateService(client)

        # Update data
        data = {"docIds": "123,456", "description__v": "Bulk updated description"}

        # Call method to test
        result = service.update_multiple_documents(data=data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/batch")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"] == json.dumps(data)

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 123
        assert result["data"][1]["id"] == 456

    @patch("requests.request")
    def test_reclassify_single_document(self, mock_request):
        """Test reclassify_single_document method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentUpdateService(client)

        # Call method to test
        result = service.reclassify_single_document(
            doc_id=123,
            type_v="new_type__v",
            lifecycle_v="new_lifecycle__v",
            subtype_v="new_subtype__v",
            classification_v="new_classification__v",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"]["type__v"] == "new_type__v"
        assert kwargs["data"]["lifecycle__v"] == "new_lifecycle__v"
        assert kwargs["data"]["subtype__v"] == "new_subtype__v"
        assert kwargs["data"]["classification__v"] == "new_classification__v"
        assert kwargs["data"]["reclassify"] == "true"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    def test_update_document_version(self, mock_request):
        """Test update_document_version method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentUpdateService(client)

        # Update data
        data = {"description__v": "Updated version description"}

        # Call method to test
        result = service.update_document_version(123, 0, 1, data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/versions/0/1")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"] == data

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open, read_data=b"updated file content")
    def test_update_document_content(self, mock_file, mock_request):
        """Test update_document_content method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": 123,
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentUpdateService(client)

        # Call method to test
        result = service.update_document_content(
            doc_id=123,
            file_path="updated_file.docx",
            comment="Updated document content",
            reuse_file=True,
            make_latest_version=True,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/file")
        assert kwargs["method"] == "POST"
        assert kwargs["params"]["reuse_file"] == "true"
        assert kwargs["params"]["make_latest_version"] == "true"
        assert "files" in kwargs

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123
        assert result["major_version_number__v"] == 0
        assert result["minor_version_number__v"] == 2


@mark.integration
@mark.veevavault
class TestDocumentUpdateServiceIntegration:
    """
    Integration tests for DocumentUpdateService using real API calls
    """

    def test_document_update_service(self, authenticated_vault_client):
        """Test basic update service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentUpdateService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Updating documents in integration tests can have unintended consequences"
    )
    def test_update_document_integration(self, authenticated_vault_client):
        """Test updating a document with real API"""
        # This test would modify real documents which is not desirable in automated tests
        pass
