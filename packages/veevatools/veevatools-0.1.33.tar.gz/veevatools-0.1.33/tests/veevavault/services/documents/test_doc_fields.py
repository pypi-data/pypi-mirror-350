from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.fields_service import DocumentFieldsService


@mark.unit
@mark.veevavault
class TestDocumentFieldsServiceUnit:
    """
    Unit tests for DocumentFieldsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_all_document_fields(self, mock_request):
        """Test retrieve_all_document_fields method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "id": {
                    "type": "number",
                    "label": "ID",
                    "queryable": True,
                },
                "name__v": {
                    "type": "string",
                    "label": "Name",
                    "required": True,
                    "editable": True,
                },
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentFieldsService(client)

        # Call method to test
        result = service.retrieve_all_document_fields()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/properties"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "id" in result["properties"]
        assert "name__v" in result["properties"]
        assert result["properties"]["name__v"]["required"] == True

    @patch("requests.request")
    def test_retrieve_common_document_fields(self, mock_request):
        """Test retrieve_common_document_fields method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "id": {
                    "type": "number",
                    "label": "ID",
                    "shared": True,
                },
                "name__v": {
                    "type": "string",
                    "label": "Name",
                    "required": True,
                    "editable": True,
                    "shared": True,
                    "usedIn": [
                        {"key": "document_type_1__c", "type": "document_type"},
                        {"key": "document_type_2__c", "type": "document_type"},
                    ],
                },
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentFieldsService(client)

        # Call method to test
        result = service.retrieve_common_document_fields("123,456")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/properties/find_common"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"]["docIds"] == "123,456"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "id" in result["properties"]
        assert "name__v" in result["properties"]
        assert result["properties"]["id"]["shared"] == True
        assert len(result["properties"]["name__v"]["usedIn"]) == 2


@mark.integration
@mark.veevavault
class TestDocumentFieldsServiceIntegration:
    """
    Integration tests for DocumentFieldsService using real API calls
    """

    def test_document_fields_service(self, authenticated_vault_client):
        """Test basic fields service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentFieldsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_retrieve_all_document_fields_integration(self, authenticated_vault_client):
        """Test retrieving all document fields with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentFieldsService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_all_document_fields()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert isinstance(result["properties"], dict)
        # At minimum, should include standard fields like id, name__v, etc.
        assert "id" in result["properties"]
        assert "name__v" in result["properties"]
