from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.rim_submissions_archive import (
    RIMSubmissionsArchiveService,
)
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.rim_submissions_archive
class TestRIMSubmissionsArchiveServiceUnit:
    """
    Unit tests for RIMSubmissionsArchiveService class using mocks (no real API calls)
    """

    @fixture
    def rim_submissions_archive_service(self):
        """Fixture for creating a RIMSubmissionsArchiveService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return RIMSubmissionsArchiveService(client)

    @patch("requests.request")
    def test_import_submission(self, mock_request, rim_submissions_archive_service):
        """Test import_submission method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"
        file_path = "/SubmissionsArchive/nda123456/0000"

        # Call method
        result = rim_submissions_archive_service.import_submission(
            submission_id, file_path
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/import"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == {"file": "/SubmissionsArchive/nda123456/0000"}
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_retrieve_submission_import_results(
        self, mock_request, rim_submissions_archive_service
    ):
        """Test retrieve_submission_import_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": "binder123",
            "major_version_number__v": 1,
            "minor_version_number__v": 0,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"
        job_id = "job123"

        # Call method
        result = rim_submissions_archive_service.retrieve_submission_import_results(
            submission_id, job_id
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/import/job123/results"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "binder123"
        assert result["major_version_number__v"] == 1

    @patch("requests.request")
    def test_retrieve_submission_metadata_mapping(
        self, mock_request, rim_submissions_archive_service
    ):
        """Test retrieve_submission_metadata_mapping method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "mappings": [
                {"name__v": "mapping1", "external_id__v": "ext1", "xml_id": "xml1"}
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"

        # Call method
        result = rim_submissions_archive_service.retrieve_submission_metadata_mapping(
            submission_id
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/ectdmapping"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["mappings"]) == 1
        assert result["mappings"][0]["name__v"] == "mapping1"

    @patch("requests.request")
    def test_update_submission_metadata_mapping(
        self, mock_request, rim_submissions_archive_service
    ):
        """Test update_submission_metadata_mapping method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Mapping updated successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"
        mapping_data = [
            {"name__v": "mapping1", "external_id__v": "ext1", "xml_id": "xml1"}
        ]

        # Call method
        result = rim_submissions_archive_service.update_submission_metadata_mapping(
            submission_id, mapping_data
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/ectdmapping"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["json"] == mapping_data
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_remove_submission(self, mock_request, rim_submissions_archive_service):
        """Test remove_submission method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"

        # Call method
        result = rim_submissions_archive_service.remove_submission(submission_id)

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/import"
        )
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_cancel_submission(self, mock_request, rim_submissions_archive_service):
        """Test cancel_submission method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Submission import job cancelled",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        submission_id = "sub123"

        # Call method
        result = rim_submissions_archive_service.cancel_submission(submission_id)

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/submission__v/sub123/actions/import"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["params"] == {"cancel": "true"}
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_export_submission(self, mock_request, rim_submissions_archive_service):
        """Test export_submission method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        binder_id = "binder123"
        submission_id = "sub123"
        major_version = "1"
        minor_version = "0"

        # Call method
        result = rim_submissions_archive_service.export_submission(
            binder_id, submission_id, major_version, minor_version
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/objects/binders/binder123/versions/1/0/actions/export"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["params"] == {"submission": "sub123"}
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_export_partial_submission(
        self, mock_request, rim_submissions_archive_service
    ):
        """Test export_partial_submission method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        binder_id = "binder123"
        submission_id = "sub123"
        major_version = "1"
        minor_version = "0"
        sections_data = "id\nsection1\nsection2"

        # Call method
        result = rim_submissions_archive_service.export_partial_submission(
            binder_id, submission_id, major_version, minor_version, sections_data
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/objects/binders/binder123/1/0/actions/export"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["params"] == {"submission": "sub123"}
        assert kwargs["data"] == sections_data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_retrieve_submission_export_results(
        self, mock_request, rim_submissions_archive_service
    ):
        """Test retrieve_submission_export_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "id": "sub123",
            "major_version_number__v": 1,
            "minor_version_number__v": 0,
            "file": "/exported_submissions/sub123.zip",
            "user_id__v": "user123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        rim_submissions_archive_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        job_id = "job123"

        # Call method
        result = rim_submissions_archive_service.retrieve_submission_export_results(
            job_id
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_archive_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_archive_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/objects/binders/actions/export/job123/results"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"
        assert result["id"] == "sub123"
        assert result["file"] == "/exported_submissions/sub123.zip"


@mark.integration
@mark.veevavault
@mark.rim_submissions_archive
class TestRIMSubmissionsArchiveServiceIntegration:
    """
    Integration tests for RIMSubmissionsArchiveService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def rim_submissions_archive_service(self, authenticated_vault_client):
        """Fixture for creating a RIMSubmissionsArchiveService instance with a real client"""
        return RIMSubmissionsArchiveService(authenticated_vault_client)

    def test_import_submission(self, rim_submissions_archive_service, vault_config):
        """Test import_submission with real API"""
        # Skip if not authenticated
        if not rim_submissions_archive_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real submission data
        pytest.skip(
            "This test requires real submission data and appropriate permissions"
        )

    def test_retrieve_submission_metadata_mapping(
        self, rim_submissions_archive_service, vault_config
    ):
        """Test retrieve_submission_metadata_mapping with real API"""
        # Skip if not authenticated
        if not rim_submissions_archive_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need a real submission ID
        pytest.skip(
            "This test requires a real submission ID and appropriate permissions"
        )
