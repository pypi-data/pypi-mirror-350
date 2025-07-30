import pytest
from pytest import mark, fixture
import requests
import json
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.directdata import DirectDataService


@mark.unit
@mark.veevavault
class TestDirectDataServiceUnit:
    """
    Unit tests for DirectDataService class using mocks (no real API calls)
    """

    def test_init(self):
        """Test service initialization"""
        # Create mock client
        mock_client = MagicMock()
        mock_client.LatestAPIversion = "v25.1"

        # Initialize service
        service = DirectDataService(mock_client)

        # Verify client is set correctly
        assert service.client == mock_client

    @patch("requests.request")
    def test_retrieve_available_direct_data_files_default(self, mock_request):
        """Test retrieve_available_direct_data_files with default parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "files": [
                {
                    "name": "146478-20240213-0000-F",
                    "filename": "146478-20240213-0000-F.tar.gz",
                    "extract_type": "full_directdata",
                    "start_time": "2000-01-01T00:00:00Z",
                    "stop_time": "2024-02-13T00:00:00Z",
                    "record_count": 150000,
                    "size": 45000000,
                    "fileparts": 3,
                    "filepart_details": [
                        {"name": "146478-20240213-0000-F.001", "size": 15000000},
                        {"name": "146478-20240213-0000-F.002", "size": 15000000},
                        {"name": "146478-20240213-0000-F.003", "size": 15000000},
                    ],
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mock client
        mock_client = MagicMock()
        mock_client.vaultURL = "https://test.veevavault.com"
        mock_client.sessionId = "test-session-id"
        mock_client.LatestAPIversion = "v25.1"
        mock_client.api_call.return_value = mock_response.json.return_value

        # Initialize service and call method
        service = DirectDataService(mock_client)
        result = service.retrieve_available_direct_data_files()

        # Verify client.api_call was called with correct parameters
        mock_client.api_call.assert_called_once()
        args, kwargs = mock_client.api_call.call_args
        assert args[0] == "api/v25.1/services/directdata/files"
        assert kwargs["method"] == "GET"
        assert kwargs["headers"] == {"Accept": "application/json"}
        assert "params" in kwargs
        assert len(kwargs["params"]) == 0  # No parameters for default call

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["files"]) == 1
        assert result["files"][0]["name"] == "146478-20240213-0000-F"
        assert result["files"][0]["extract_type"] == "full_directdata"
        assert result["files"][0]["fileparts"] == 3

    @patch("requests.request")
    def test_retrieve_available_direct_data_files_with_params(self, mock_request):
        """Test retrieve_available_direct_data_files with optional parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "files": [
                {
                    "name": "146478-20240213-0000-I",
                    "filename": "146478-20240213-0000-I.tar.gz",
                    "extract_type": "incremental_directdata",
                    "start_time": "2024-02-12T00:00:00Z",
                    "stop_time": "2024-02-13T00:00:00Z",
                    "record_count": 5000,
                    "size": 1500000,
                    "fileparts": 1,
                    "filepart_details": [
                        {"name": "146478-20240213-0000-I.001", "size": 1500000}
                    ],
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mock client
        mock_client = MagicMock()
        mock_client.vaultURL = "https://test.veevavault.com"
        mock_client.sessionId = "test-session-id"
        mock_client.LatestAPIversion = "v25.1"
        mock_client.api_call.return_value = mock_response.json.return_value

        # Initialize service and call method with parameters
        service = DirectDataService(mock_client)
        result = service.retrieve_available_direct_data_files(
            extract_type="incremental_directdata",
            start_time="2024-02-12T00:00:00Z",
            stop_time="2024-02-13T00:00:00Z",
        )

        # Verify client.api_call was called with correct parameters
        mock_client.api_call.assert_called_once()
        args, kwargs = mock_client.api_call.call_args
        assert args[0] == "api/v25.1/services/directdata/files"
        assert kwargs["method"] == "GET"
        assert kwargs["params"] == {
            "extract_type": "incremental_directdata",
            "start_time": "2024-02-12T00:00:00Z",
            "stop_time": "2024-02-13T00:00:00Z",
        }

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["files"]) == 1
        assert result["files"][0]["name"] == "146478-20240213-0000-I"
        assert result["files"][0]["extract_type"] == "incremental_directdata"

    @patch("requests.get")
    def test_download_direct_data_file(self, mock_get):
        """Test download_direct_data_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"mock file content"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Create mock client
        mock_client = MagicMock()
        mock_client.vaultURL = "https://test.veevavault.com"
        mock_client.sessionId = "test-session-id"
        mock_client.LatestAPIversion = "v25.1"

        # Initialize service and call method
        service = DirectDataService(mock_client)
        result = service.download_direct_data_file("146478-20240213-0000-F.001")

        # Verify requests.get was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            args[0]
            == "https://test.veevavault.com/api/v25.1/services/directdata/files/146478-20240213-0000-F.001"
        )
        assert kwargs["headers"] == {
            "Authorization": "test-session-id",
            "Accept": "application/octet-stream",
        }

        # Verify result is binary data
        assert result == b"mock file content"

    @patch("requests.get")
    def test_download_direct_data_file_http_error(self, mock_get):
        """Test download_direct_data_file method with HTTP error"""
        # Set up mock to raise HTTPError
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found"
        )
        mock_get.return_value = mock_response

        # Create mock client
        mock_client = MagicMock()
        mock_client.vaultURL = "https://test.veevavault.com"
        mock_client.sessionId = "test-session-id"
        mock_client.LatestAPIversion = "v25.1"

        # Initialize service
        service = DirectDataService(mock_client)

        # Call method that should raise exception
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            service.download_direct_data_file("nonexistent-file.001")

        # Verify correct exception message
        assert "404 Client Error" in str(exc_info.value)


@mark.integration
@mark.veevavault
class TestDirectDataServiceIntegration:
    """
    Integration tests for DirectDataService class using real API calls
    These tests will be skipped if no credentials are available or if Direct Data is not enabled
    """

    def test_retrieve_available_direct_data_files(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieve_available_direct_data_files with real credentials"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DirectDataService(authenticated_vault_client)

        # Try to get available files
        try:
            result = service.retrieve_available_direct_data_files()

            # Check basic response structure
            assert "responseStatus" in result

            # If successful, check for files array (even if empty)
            if result["responseStatus"] == "SUCCESS":
                assert "files" in result
        except requests.exceptions.HTTPError as e:
            # Skip if Direct Data API is not enabled (403 error expected)
            if "403" in str(e):
                pytest.skip("Direct Data API is not enabled for this Vault")
            else:
                # For other HTTP errors, fail the test
                raise

    @pytest.mark.skip(
        reason="Cannot reliably test file download in integration tests without knowing valid file names"
    )
    def test_download_direct_data_file(self, authenticated_vault_client, vault_config):
        """Test download_direct_data_file with real credentials"""
        # This test is skipped because:
        # 1. We don't know valid file names in advance
        # 2. Downloads could be large and take time
        # 3. Need to use a file name from retrieve_available_direct_data_files response

        # In a real implementation, one would:
        # 1. Call retrieve_available_direct_data_files
        # 2. Get a file name from the response
        # 3. Use that file name to test download_direct_data_file
        pass
