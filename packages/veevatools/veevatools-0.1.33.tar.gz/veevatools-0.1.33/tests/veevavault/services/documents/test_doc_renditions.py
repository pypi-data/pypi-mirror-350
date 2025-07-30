from pytest import mark, fixture
import pytest
import requests
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.documents.renditions_service import DocumentRenditionsService


@mark.unit
@mark.veevavault
class TestDocumentRenditionsServiceUnit:
    """
    Unit tests for DocumentRenditionsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_renditions(self, mock_request):
        """Test retrieve_document_renditions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "renditionTypes": ["viewable", "thumbnail"],
            "renditions": [
                {
                    "type": "viewable",
                    "url": "/api/v25.1/objects/documents/123/renditions/viewable",
                },
                {
                    "type": "thumbnail",
                    "url": "/api/v25.1/objects/documents/123/renditions/thumbnail",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRenditionsService(client)

        # Call method to test
        result = service.retrieve_document_renditions("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/renditions")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "renditionTypes" in result
        assert "renditions" in result
        assert len(result["renditionTypes"]) == 2
        assert len(result["renditions"]) == 2
        assert result["renditions"][0]["type"] == "viewable"

    @patch("requests.request")
    def test_download_document_rendition_file(self, mock_request):
        """Test download_document_rendition_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"rendition content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRenditionsService(client)

        # Call method to test
        result = service.download_document_rendition_file("123", "viewable")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/renditions/viewable"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "*/*"
        assert kwargs["raw_response"] == True

        # Verify response
        assert result == b"rendition content"

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open, read_data=b"rendition content")
    def test_add_single_document_rendition(self, mock_file, mock_request):
        """Test add_single_document_rendition method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRenditionsService(client)

        # Call method to test
        result = service.add_single_document_rendition("123", "viewable", "test.pdf")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/renditions/viewable"
        )
        assert kwargs["method"] == "POST"
        assert "files" in kwargs

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    def test_delete_single_document_rendition(self, mock_request):
        """Test delete_single_document_rendition method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRenditionsService(client)

        # Call method to test
        result = service.delete_single_document_rendition("123", "viewable")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/renditions/viewable"
        )
        assert kwargs["method"] == "DELETE"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_get_document_rendition_types(self, mock_request):
        """Test get_document_rendition_types method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "renditionTypes": [
                {"name": "viewable", "label": "Viewable Rendition"},
                {"name": "thumbnail", "label": "Thumbnail"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRenditionsService(client)

        # Call method to test
        result = service.get_document_rendition_types()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/renditiontypes"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "renditionTypes" in result
        assert len(result["renditionTypes"]) == 2
        assert result["renditionTypes"][0]["name"] == "viewable"
        assert result["renditionTypes"][1]["name"] == "thumbnail"


@mark.integration
@mark.veevavault
class TestDocumentRenditionsServiceIntegration:
    """
    Integration tests for DocumentRenditionsService using real API calls
    """

    def test_document_renditions_service(self, authenticated_vault_client):
        """Test basic renditions service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentRenditionsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_get_document_rendition_types_integration(self, authenticated_vault_client):
        """Test retrieving document rendition types with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentRenditionsService(authenticated_vault_client)

        # Call method to test
        result = service.get_document_rendition_types()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "renditionTypes" in result
        assert isinstance(result["renditionTypes"], list)
        # There should be at least a viewable rendition type
        rendition_names = [r["name"] for r in result["renditionTypes"]]
        assert "viewable" in rendition_names
