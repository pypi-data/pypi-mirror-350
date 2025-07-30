from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.deletion_service import DocumentDeletionService


@mark.unit
@mark.veevavault
class TestDocumentDeletionServiceUnit:
    """
    Unit tests for DocumentDeletionService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_delete_single_document(self, mock_request):
        """Test delete_single_document method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": 534,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentDeletionService(client)

        # Call method to test
        result = service.delete_single_document("534")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/534")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 534

    @patch("requests.request")
    def test_delete_multiple_documents(self, mock_request):
        """Test delete_multiple_documents method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "id": 771,
                    "external_id__v": "ALT-DOC-0771",
                },
                {
                    "responseStatus": "SUCCESS",
                    "id": 772,
                    "external_id__v": "CHO-DOC-0772",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentDeletionService(client)

        # Test CSV data
        csv_data = "id\n771\n772"

        # Call method to test
        result = service.delete_multiple_documents(csv_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/batch")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Content-Type"] == "text/csv"
        assert (
            kwargs["data"] == csv_data.encode()
            if isinstance(csv_data, str)
            else csv_data
        )

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 771
        assert result["data"][1]["id"] == 772

    @patch("requests.request")
    def test_delete_single_document_version(self, mock_request):
        """Test delete_single_document_version method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": 534,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentDeletionService(client)

        # Call method to test
        result = service.delete_single_document_version("534", 0, 1)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/534/versions/0/1")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 534

    @patch("requests.request")
    def test_retrieve_deleted_document_ids(self, mock_request):
        """Test retrieve_deleted_document_ids method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "OK",
            "responseDetails": {"total": 2, "size": 2, "limit": 1000, "offset": 0},
            "data": [
                {
                    "id": 23,
                    "major_version_number__v": 0,
                    "minor_version_number__v": 1,
                    "date_deleted": "2021-02-26T23:46:49Z",
                    "global_id__sys": "10000760_23",
                    "global_version_id__sys": "10000760_23_39",
                    "external_id__v": None,
                    "deletion_type": "version_change__sys",
                },
                {
                    "id": 10,
                    "major_version_number__v": "",
                    "minor_version_number__v": "",
                    "date_deleted": "2021-02-26T23:55:45Z",
                    "global_id__sys": "10000760_10",
                    "global_version_id__sys": None,
                    "external_id__v": None,
                    "deletion_type": "document__sys",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentDeletionService(client)

        # Call method to test
        result = service.retrieve_deleted_document_ids(
            "2021-02-25T00:00:00Z", "2021-02-27T00:00:00Z"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/deletions/documents")
        assert kwargs["method"] == "GET"
        assert kwargs["params"]["start_date"] == "2021-02-25T00:00:00Z"
        assert kwargs["params"]["end_date"] == "2021-02-27T00:00:00Z"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseDetails"]["total"] == 2
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == 23
        assert result["data"][1]["id"] == 10


@mark.integration
@mark.veevavault
class TestDocumentDeletionServiceIntegration:
    """
    Integration tests for DocumentDeletionService using real API calls
    """

    def test_document_deletion_service(self, authenticated_vault_client):
        """Test basic deletion service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentDeletionService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Deleting documents in integration tests can have unintended consequences"
    )
    def test_delete_document_integration(self, authenticated_vault_client):
        """Test deleting a document with real API"""
        # This test would delete real documents which is not desirable in automated tests
        pass
