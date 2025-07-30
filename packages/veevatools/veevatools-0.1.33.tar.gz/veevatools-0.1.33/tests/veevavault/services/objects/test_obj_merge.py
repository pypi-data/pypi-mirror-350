from pytest import mark, fixture
import pytest
import requests
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.objects.merge_service import ObjectMergeService


@mark.unit
@mark.veevavault
class TestObjectMergeServiceUnit:
    """
    Unit tests for ObjectMergeService
    """

    @patch("requests.request")
    def test_initiate_record_merge(self, mock_request):
        """Test initiate_record_merge method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "links": [
                {
                    "rel": "self",
                    "href": "/api/v25.1/vobjects/contact__v/actions/mergerecords/job123",
                },
                {
                    "rel": "status",
                    "href": "/api/v25.1/vobjects/contact__v/actions/mergerecords/job123",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        merge_service = ObjectMergeService(client)

        # Test payload
        payload = {
            "records": [{"main_record_id": "12345", "duplicate_record_id": "67890"}]
        }

        # Call method to test
        result = merge_service.initiate_record_merge("contact__v", payload)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/contact__v/actions/mergerecords"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_retrieve_record_merge_status(self, mock_request):
        """Test retrieve_record_merge_status method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job": {
                "id": "job123",
                "status": "IN_PROGRESS",
                "start_date": "2023-01-01T12:00:00.000Z",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        merge_service = ObjectMergeService(client)

        # Call method to test
        result = merge_service.retrieve_record_merge_status("contact__v", "job123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/contact__v/actions/mergerecords/job123"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job"]["status"] == "IN_PROGRESS"
        assert result["job"]["id"] == "job123"

    @patch("requests.request")
    def test_retrieve_record_merge_results(self, mock_request):
        """Test retrieve_record_merge_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job": {
                "id": "job123",
                "status": "SUCCESS",
                "start_date": "2023-01-01T12:00:00.000Z",
                "completion_date": "2023-01-01T12:01:00.000Z",
            },
            "records": [
                {
                    "main_record_id": "12345",
                    "duplicate_record_id": "67890",
                    "status": "SUCCESS",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        merge_service = ObjectMergeService(client)

        # Call method to test
        result = merge_service.retrieve_record_merge_results("contact__v", "job123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/contact__v/actions/mergerecords/job123/results"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job"]["status"] == "SUCCESS"
        assert len(result["records"]) == 1
        assert result["records"][0]["main_record_id"] == "12345"

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_merge_records_job_log(self, mock_file, mock_request):
        """Test download_merge_records_job_log method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"test log data"]
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        merge_service = ObjectMergeService(client)

        # Call method to test
        result = merge_service.download_merge_records_job_log(
            "contact__v", "job123", "test_log.txt"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/contact__v/actions/mergerecords/job123/log"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["stream"] == True
        assert kwargs["raw_response"] == True

        # Verify file was written
        mock_file.assert_called_once_with("test_log.txt", "wb")
        mock_file().write.assert_called_once_with(b"test log data")

        # Verify return message
        assert result == "Merge records job log downloaded successfully"


@mark.integration
@mark.veevavault
class TestObjectMergeServiceIntegration:
    """
    Integration tests for ObjectMergeService using real API calls
    """

    def test_integration_merge_operations(
        self, authenticated_vault_client, vault_config
    ):
        """Integration test for merge operations"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        merge_service = ObjectMergeService(authenticated_vault_client)

        # Skip actual API call in this template
        pytest.skip("Integration test requires two valid record IDs to merge")
