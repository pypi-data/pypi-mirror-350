from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderExportService


@mark.unit
@mark.veevavault
class TestBinderExportServiceUnit:
    """
    Unit tests for BinderExportService using mocks
    """

    def test_export_binder(self):
        """Test exporting a complete binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Initiated binder export job",
                "URL": "https://test.veevavault.com/api/v25.1/objects/binders/actions/export/job_123",
                "job_id": "job_123",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test
            result = export_service.export_binder(
                binder_id="123",
                source=True,
                renditiontype="viewable_rendition__v",
                docversion="major",
                fields="name__v,type__v,status__v",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/actions/export"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Accept"] == "application/json"

            # Verify parameters
            assert kwargs["params"]["source"] == "true"
            assert kwargs["params"]["renditiontype"] == "viewable_rendition__v"
            assert kwargs["params"]["docversion"] == "major"
            assert kwargs["params"]["fields"] == "name__v,type__v,status__v"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["job_id"] == "job_123"

    def test_export_binder_specific_version(self):
        """Test exporting a specific version of a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Initiated binder export job",
                "URL": "https://test.veevavault.com/api/v25.1/objects/binders/actions/export/job_124",
                "job_id": "job_124",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test with specific version
            result = export_service.export_binder(
                binder_id="123", major_version=1, minor_version=0, source=True
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/versions/1/0/actions/export"
            )
            assert kwargs["method"] == "POST"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["job_id"] == "job_124"

    def test_export_binder_sections(self):
        """Test exporting specific sections of a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Initiated binder export job",
                "URL": "https://test.veevavault.com/api/v25.1/objects/binders/actions/export/job_125",
                "job_id": "job_125",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test with specific sections in CSV format
            node_ids = ["section_1", "section_2", "document_1"]
            result = export_service.export_binder_sections(
                binder_id="123", node_ids=node_ids, input_file_format="csv"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/actions/export"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Content-Type"] == "text/csv"

            # Verify CSV data format
            assert kwargs["data"] == "section_1\nsection_2\ndocument_1"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["job_id"] == "job_125"

    def test_export_binder_sections_json(self):
        """Test exporting specific sections of a binder with JSON format"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Initiated binder export job",
                "URL": "https://test.veevavault.com/api/v25.1/objects/binders/actions/export/job_126",
                "job_id": "job_126",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test with specific sections in JSON format
            node_ids = ["section_1", "section_2", "document_1"]
            result = export_service.export_binder_sections(
                binder_id="123", node_ids=node_ids, input_file_format="json"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/actions/export"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Content-Type"] == "application/json"

            # Verify JSON data format
            import json

            assert json.loads(kwargs["data"]) == {"id": node_ids}

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["job_id"] == "job_126"

    def test_retrieve_binder_export_results(self):
        """Test retrieving the results of a completed binder export job"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "job_id": "job_123",
                "id": "123",
                "major_version_number__v": 1,
                "minor_version_number__v": 0,
                "file": "/api/v25.1/objects/files/downloadFile/file_123",
                "user_id__v": "user_456",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test
            result = export_service.retrieve_binder_export_results("job_123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/actions/export/job_123/results"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["job_id"] == "job_123"
            assert result["file"] == "/api/v25.1/objects/files/downloadFile/file_123"

    def test_download_exported_binder_files(self):
        """Test downloading the files from a completed binder export"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.content = b"zip file content"
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            export_service = BinderExportService(client)

            # Call method to test
            result = export_service.download_exported_binder_files(
                "/api/v25.1/objects/files/downloadFile/file_123"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert kwargs["url"] == "/api/v25.1/objects/files/downloadFile/file_123"
            assert kwargs["headers"]["Accept"] == "application/zip"

            # Verify returned content
            assert result == b"zip file content"


@mark.integration
@mark.veevavault
class TestBinderExportServiceIntegration:
    """
    Integration tests for BinderExportService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_export_binder(self, authenticated_vault_client, vault_config):
        """Test exporting a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        export_service = BinderExportService(authenticated_vault_client)

        # Skip - requires existing binder and can be resource-intensive
        pytest.skip(
            "Skipping to prevent resource-intensive operation. Requires existing binder ID."
        )

    def test_retrieve_binder_export_results(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving binder export results with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        export_service = BinderExportService(authenticated_vault_client)

        # Skip - requires existing job ID from a previous export
        pytest.skip("Skipping as it requires an existing export job ID.")
