from pytest import mark, fixture
import pytest
import requests
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.locks_service import DocumentLocksService


@mark.unit
@mark.veevavault
class TestDocumentLocksServiceUnit:
    """
    Unit tests for DocumentLocksService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_lock_metadata(self, mock_request):
        """Test retrieve_document_lock_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "locked_by__v": {
                    "type": "objectReference",
                    "label": "Locked By",
                    "objectType": "user__sys",
                },
                "locked_date__v": {"type": "datetime", "label": "Locked Date"},
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentLocksService(client)

        # Call method to test
        result = service.retrieve_document_lock_metadata()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/objects/documents/lock")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "locked_by__v" in result["properties"]
        assert "locked_date__v" in result["properties"]
        assert result["properties"]["locked_by__v"]["objectType"] == "user__sys"

    @patch("requests.request")
    def test_create_document_lock(self, mock_request):
        """Test create_document_lock method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Document successfully checked out.",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentLocksService(client)

        # Call method to test
        result = service.create_document_lock("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/lock")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseMessage"] == "Document successfully checked out."

    @patch("requests.request")
    def test_retrieve_document_lock(self, mock_request):
        """Test retrieve_document_lock method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "document": {
                "id": 123,
                "locked_by__v": 456,
                "locked_date__v": "2021-06-15T14:30:00Z",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentLocksService(client)

        # Call method to test
        result = service.retrieve_document_lock("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/lock")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "document" in result
        assert result["document"]["locked_by__v"] == 456
        assert "locked_date__v" in result["document"]

    @patch("requests.request")
    def test_delete_document_lock(self, mock_request):
        """Test delete_document_lock method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Undo check out successful.",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentLocksService(client)

        # Call method to test
        result = service.delete_document_lock("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/lock")
        assert kwargs["method"] == "DELETE"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseMessage"] == "Undo check out successful."

    @patch("requests.request")
    def test_undo_collaborative_authoring_checkout(self, mock_request):
        """Test undo_collaborative_authoring_checkout method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "Undo check out successful.",
                    "id": 123,
                },
                {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "Undo check out successful.",
                    "id": 456,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentLocksService(client)

        # Call method to test
        result = service.undo_collaborative_authoring_checkout(["123", "456"])

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/batch/lock")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Content-Type"] == "text/csv"
        assert "id\n123\n456" in kwargs["data"].decode()

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 123
        assert result["data"][1]["id"] == 456


@mark.integration
@mark.veevavault
class TestDocumentLocksServiceIntegration:
    """
    Integration tests for DocumentLocksService using real API calls
    """

    def test_document_locks_service(self, authenticated_vault_client):
        """Test basic locks service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentLocksService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_retrieve_document_lock_metadata_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document lock metadata with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentLocksService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_document_lock_metadata()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "locked_by__v" in result["properties"]
        assert "locked_date__v" in result["properties"]
