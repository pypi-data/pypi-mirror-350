from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.bulk_translation import BulkTranslationService


@mark.unit
@mark.veevavault
class TestBulkTranslationServiceUnit:
    """
    Unit tests for BulkTranslationService class using mocks (no real API calls)
    """

    def test_init(self):
        """Test service initialization"""
        client = MagicMock()
        service = BulkTranslationService(client)
        assert service.client == client

    @patch("requests.request")
    def test_export_bulk_translation_file(self, mock_request):
        """Test export_bulk_translation_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {
                "jobId": "job123",
                "url": "https://test.veevavault.com/api/v25.1/services/jobs/job123",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        service = BulkTranslationService(client)

        # Call method to test
        result = service.export_bulk_translation_file("field_labels__sys", "en")

        # Verify client.api_call was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/messages/field_labels__sys/language/en/actions/export",
            method="POST",
        )

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"]["jobId"] == "job123"

    @patch("requests.request")
    def test_import_bulk_translation_file(self, mock_request):
        """Test import_bulk_translation_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {
                "jobId": "job456",
                "url": "https://test.veevavault.com/api/v25.1/services/jobs/job456",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        service = BulkTranslationService(client)

        # Call method to test
        result = service.import_bulk_translation_file(
            "field_labels__sys", "/staging/translations.csv"
        )

        # Verify client.api_call was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/messages/field_labels__sys/actions/import",
            method="POST",
            data={"file_path": "/staging/translations.csv"},
        )

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"]["jobId"] == "job456"

    @patch("requests.request")
    def test_retrieve_import_job_summary(self, mock_request):
        """Test retrieve_import_job_summary method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {"ignored": 5, "updated": 10, "failed": 2, "added": 3},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        service = BulkTranslationService(client)

        # Call method to test
        result = service.retrieve_import_job_summary("job456")

        # Verify client.api_call was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/job456/summary"
        )

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"]["ignored"] == 5
        assert result["data"]["updated"] == 10
        assert result["data"]["failed"] == 2
        assert result["data"]["added"] == 3

    @patch("requests.request")
    def test_retrieve_import_job_errors(self, mock_request):
        """Test retrieve_import_job_errors method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.text = "line,error\n1,Invalid value\n2,Required field missing"
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response

        # Create service with mocked client
        service = BulkTranslationService(client)

        # Call method to test
        result = service.retrieve_import_job_errors("job456")

        # Verify client.api_call was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/job456/errors",
            headers={"Accept": "text/csv"},
            return_raw=True,
        )

        # Verify response (raw response is returned in this case)
        assert result == mock_response


@mark.integration
@mark.veevavault
class TestBulkTranslationServiceIntegration:
    """
    Integration tests for BulkTranslationService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_export_bulk_translation_file(
        self, authenticated_vault_client, vault_config
    ):
        """Test export_bulk_translation_file with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = BulkTranslationService(authenticated_vault_client)

        # Export bulk translation for English field labels
        # Note: This is a real API call that creates a job
        pytest.skip("Skipping actual API call to avoid creating real jobs in Vault")
        # If you want to enable this test, remove the skip and uncomment:
        # result = service.export_bulk_translation_file("field_labels__sys", "en")
        # assert result["responseStatus"] == "SUCCESS"
        # assert "jobId" in result["data"]

    def test_import_bulk_translation_file(
        self, authenticated_vault_client, vault_config
    ):
        """Test import_bulk_translation_file with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = BulkTranslationService(authenticated_vault_client)

        # This test requires a file to already be uploaded to staging
        pytest.skip("Skipping actual API call - requires file in Vault staging area")
        # If you want to enable this test, remove the skip and uncomment:
        # result = service.import_bulk_translation_file("field_labels__sys", "/staging/test_translations.csv")
        # assert result["responseStatus"] == "SUCCESS"
        # assert "jobId" in result["data"]

    def test_retrieve_import_job_summary(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieve_import_job_summary with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = BulkTranslationService(authenticated_vault_client)

        # This test requires a real job ID from a previous import
        pytest.skip(
            "Skipping actual API call - requires valid job ID from previous import"
        )
        # If you want to enable this test, remove the skip and uncomment:
        # result = service.retrieve_import_job_summary("job_id_here")
        # assert result["responseStatus"] == "SUCCESS"
        # assert "ignored" in result["data"]
        # assert "updated" in result["data"]
        # assert "failed" in result["data"]
        # assert "added" in result["data"]

    def test_retrieve_import_job_errors(self, authenticated_vault_client, vault_config):
        """Test retrieve_import_job_errors with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = BulkTranslationService(authenticated_vault_client)

        # This test requires a real job ID from a previous import that had errors
        pytest.skip(
            "Skipping actual API call - requires valid job ID from previous import with errors"
        )
        # If you want to enable this test, remove the skip and uncomment:
        # result = service.retrieve_import_job_errors("job_id_here")
        # This returns raw CSV content, so just check it's not empty
        # assert result and len(result) > 0
