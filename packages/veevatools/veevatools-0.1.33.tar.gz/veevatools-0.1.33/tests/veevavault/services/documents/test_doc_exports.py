from pytest import mark, fixture
import pytest
import requests
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.exports_service import DocumentExportsService


@mark.unit
@mark.veevavault
class TestDocumentExportsServiceUnit:
    """
    Unit tests for DocumentExportsService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_export_documents(self, mock_request):
        """Test export_documents method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "url": "/api/v25.1/services/jobs/36203",
            "job_id": "36203",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentExportsService(client)

        # Document IDs to export
        doc_ids = [{"id": "58"}, {"id": "134"}]

        # Call method to test
        result = service.export_documents(
            doc_ids, source=True, renditions=True, all_versions=False
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/batch/actions/fileextract"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["params"]["source"] == "true"
        assert kwargs["params"]["renditions"] == "true"
        assert kwargs["params"]["allversions"] == "false"
        assert json.loads(kwargs["data"]) == doc_ids

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "36203"

    @patch("requests.request")
    def test_export_document_versions(self, mock_request):
        """Test export_document_versions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "url": "/api/v25.1/services/jobs/40604",
            "job_id": "40604",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentExportsService(client)

        # Version data to export
        version_data = [
            {"id": "58", "major_version_number__v": 0, "minor_version_number__v": 1},
            {"id": "134", "major_version_number__v": 1, "minor_version_number__v": 0},
        ]

        # Call method to test
        result = service.export_document_versions(
            version_data, source=True, renditions=False
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/versions/batch/actions/fileextract"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["params"]["source"] == "true"
        assert kwargs["params"]["renditions"] == "false"
        assert json.loads(kwargs["data"]) == version_data

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "40604"

    @patch("requests.request")
    def test_get_document_export_results(self, mock_request):
        """Test get_document_export_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "id": 23,
                    "major_version_number__v": 0,
                    "minor_version_number__v": 1,
                    "file": "/82701/23/0_1/New Document.png",
                    "user_id__v": 88973,
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentExportsService(client)

        # Call method to test
        result = service.get_document_export_results("36203")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/batch/actions/fileextract/36203/results"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == 23
        assert result["data"][0]["file"] == "/82701/23/0_1/New Document.png"

    @patch("requests.request")
    def test_export_document_data_as_csv(self, mock_request):
        """Test export_document_data_as_csv method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.text = "id,name__v,type__v\n123,Test Document,test_doc_type__v"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentExportsService(client)

        # Call method to test
        result = service.export_document_data_as_csv("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/export")
        assert kwargs["headers"]["Accept"] == "text/csv"
        assert kwargs["raw_response"] == True

        # Verify response
        assert result == "id,name__v,type__v\n123,Test Document,test_doc_type__v"


@mark.integration
@mark.veevavault
class TestDocumentExportsServiceIntegration:
    """
    Integration tests for DocumentExportsService using real API calls
    """

    def test_document_exports_service(self, authenticated_vault_client):
        """Test basic exports service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentExportsService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Exporting documents requires specific permissions and document IDs"
    )
    def test_export_documents_integration(self, authenticated_vault_client):
        """Test exporting documents with real API"""
        pass
