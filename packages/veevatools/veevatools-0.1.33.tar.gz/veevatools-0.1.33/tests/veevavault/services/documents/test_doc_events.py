from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.events_service import DocumentEventsService


@mark.unit
@mark.veevavault
class TestDocumentEventsServiceUnit:
    """
    Unit tests for DocumentEventsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_event_types(self, mock_request):
        """Test retrieve_document_event_types method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "eventTypes": [
                {
                    "name": "distribution__v",
                    "label": "Distribution",
                    "subtypes": [
                        {"name": "approved_email__v", "label": "Approved Email"}
                    ],
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentEventsService(client)

        # Call method to test
        result = service.retrieve_document_event_types()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/objects/documents/events")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["eventTypes"]) == 1
        assert result["eventTypes"][0]["name"] == "distribution__v"
        assert result["eventTypes"][0]["subtypes"][0]["name"] == "approved_email__v"

    @patch("requests.request")
    def test_retrieve_document_event_subtype_metadata(self, mock_request):
        """Test retrieve_document_event_subtype_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "name__v": {"type": "string", "label": "Name"},
                "classification__v": {"type": "picklist", "label": "Classification"},
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentEventsService(client)

        # Call method to test
        result = service.retrieve_document_event_subtype_metadata(
            "distribution__v", "approved_email__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/objects/documents/events/distribution__v/types/approved_email__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "name__v" in result["properties"]
        assert "classification__v" in result["properties"]

    @patch("requests.request")
    def test_create_document_event(self, mock_request):
        """Test create_document_event method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentEventsService(client)

        # Call method to test
        result = service.create_document_event(
            doc_id="456",
            major_version=0,
            minor_version=1,
            event_type="distribution__v",
            event_subtype="approved_email__v",
            classification="download__v",
            external_id="EXT-EVENT-001",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/456/versions/0/1/events"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert "event_type__v" in kwargs["data"]
        assert "event_subtype__v" in kwargs["data"]
        assert "classification__v" in kwargs["data"]
        assert "external_id__v" in kwargs["data"]

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    def test_retrieve_document_events(self, mock_request):
        """Test retrieve_document_events method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "events": [
                {
                    "id": 123,
                    "event_type__v": "distribution__v",
                    "event_subtype__v": "approved_email__v",
                    "classification__v": "download__v",
                    "created_by__v": 1001,
                    "created_date__v": "2021-01-15T10:30:00Z",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentEventsService(client)

        # Call method to test
        result = service.retrieve_document_events("456")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/456/events")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["events"]) == 1
        assert result["events"][0]["id"] == 123
        assert result["events"][0]["event_type__v"] == "distribution__v"


@mark.integration
@mark.veevavault
class TestDocumentEventsServiceIntegration:
    """
    Integration tests for DocumentEventsService using real API calls
    """

    def test_document_events_service(self, authenticated_vault_client):
        """Test basic events service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentEventsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(reason="This test requires configured event types in the Vault")
    def test_retrieve_document_event_types_integration(
        self, authenticated_vault_client
    ):
        """Test retrieving document event types with real API"""
        pass
