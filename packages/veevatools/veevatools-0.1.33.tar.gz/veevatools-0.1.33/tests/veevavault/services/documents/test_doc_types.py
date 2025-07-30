from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.types_service import DocumentTypesService


@mark.unit
@mark.veevavault
class TestDocumentTypesServiceUnit:
    """
    Unit tests for DocumentTypesService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_all_document_types(self, mock_request):
        """Test retrieve_all_document_types method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "types": [
                {
                    "label": "Promotional",
                    "value": "promotional__v",
                    "url": "/api/v25.1/metadata/objects/documents/types/promotional__v",
                },
                {
                    "label": "Reference",
                    "value": "reference__v",
                    "url": "/api/v25.1/metadata/objects/documents/types/reference__v",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTypesService(client)

        # Call method to test
        result = service.retrieve_all_document_types()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/objects/documents/types")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "types" in result
        assert len(result["types"]) == 2
        assert result["types"][0]["label"] == "Promotional"
        assert result["types"][0]["value"] == "promotional__v"
        assert result["types"][1]["label"] == "Reference"
        assert result["types"][1]["value"] == "reference__v"

    @patch("requests.request")
    def test_retrieve_document_type(self, mock_request):
        """Test retrieve_document_type method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "name": "promotional__v",
            "label": "Promotional",
            "properties": {"name__v": {"type": "string", "label": "Name"}},
            "relationshipTypes": [
                {"value": "supporting_document__v", "label": "Supporting Document"}
            ],
            "renditions": [{"value": "viewable", "label": "Viewable Rendition"}],
            "subtypes": [
                {
                    "label": "Print Ad",
                    "value": "print_ad__v",
                    "url": "/api/v25.1/metadata/objects/documents/types/promotional__v/subtypes/print_ad__v",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTypesService(client)

        # Call method to test
        result = service.retrieve_document_type("promotional__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/types/promotional__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "promotional__v"
        assert result["label"] == "Promotional"
        assert "properties" in result
        assert "name__v" in result["properties"]
        assert "relationshipTypes" in result
        assert "renditions" in result
        assert "subtypes" in result
        assert len(result["subtypes"]) == 1
        assert result["subtypes"][0]["label"] == "Print Ad"
        assert result["subtypes"][0]["value"] == "print_ad__v"

    @patch("requests.request")
    def test_retrieve_document_subtype(self, mock_request):
        """Test retrieve_document_subtype method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "name": "print_ad__v",
            "label": "Print Ad",
            "properties": {
                "name__v": {"type": "string", "label": "Name"},
                "audience__v": {"type": "picklist", "label": "Audience"},
            },
            "classifications": [
                {
                    "label": "Medical Journal Ad",
                    "value": "medical_journal_ad__v",
                    "url": "/api/v25.1/metadata/objects/documents/types/promotional__v/subtypes/print_ad__v/classifications/medical_journal_ad__v",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTypesService(client)

        # Call method to test
        result = service.retrieve_document_subtype("promotional__v", "print_ad__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/types/promotional__v/subtypes/print_ad__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "print_ad__v"
        assert result["label"] == "Print Ad"
        assert "properties" in result
        assert "audience__v" in result["properties"]
        assert "classifications" in result
        assert len(result["classifications"]) == 1
        assert result["classifications"][0]["label"] == "Medical Journal Ad"
        assert result["classifications"][0]["value"] == "medical_journal_ad__v"

    @patch("requests.request")
    def test_retrieve_document_classification(self, mock_request):
        """Test retrieve_document_classification method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "name": "medical_journal_ad__v",
            "label": "Medical Journal Ad",
            "properties": {
                "name__v": {"type": "string", "label": "Name"},
                "journal_name__v": {"type": "string", "label": "Journal Name"},
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTypesService(client)

        # Call method to test
        result = service.retrieve_document_classification(
            "promotional__v", "print_ad__v", "medical_journal_ad__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/types/promotional__v/subtypes/print_ad__v/classifications/medical_journal_ad__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "medical_journal_ad__v"
        assert result["label"] == "Medical Journal Ad"
        assert "properties" in result
        assert "journal_name__v" in result["properties"]


@mark.integration
@mark.veevavault
class TestDocumentTypesServiceIntegration:
    """
    Integration tests for DocumentTypesService using real API calls
    """

    def test_document_types_service(self, authenticated_vault_client):
        """Test basic types service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentTypesService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_retrieve_all_document_types_integration(self, authenticated_vault_client):
        """Test retrieving all document types with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentTypesService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_all_document_types()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "types" in result
        assert isinstance(result["types"], list)
        # There should be at least one document type in the vault
        assert len(result["types"]) > 0
        # Check structure of first document type
        assert "label" in result["types"][0]
        assert "value" in result["types"][0]
        assert "url" in result["types"][0]
