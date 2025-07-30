from pytest import mark, fixture
import pytest
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.objects.attachment_fields_service import (
    ObjectAttachmentFieldsService,
)


@mark.unit
@mark.veevavault
class TestObjectAttachmentFieldsServiceUnit:
    """
    Unit tests for ObjectAttachmentFieldsService
    """

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_attachment_field_file(self, mock_file, mock_request):
        """Test download_attachment_field_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"file content"]
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_fields_service = ObjectAttachmentFieldsService(client)

        # Call method to test
        result = attachment_fields_service.download_attachment_field_file(
            "document__v", "doc001", "attachment_field__vs", "test_download.pdf"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachmentfields/attachment_field__vs/file"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["stream"] == True
        assert kwargs["raw_response"] == True

        # Verify file was written
        mock_file.assert_called_once_with("test_download.pdf", "wb")
        mock_file().write.assert_called_once_with(b"file content")

        # Verify return message
        assert result == "File downloaded successfully"

    @patch("requests.request")
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    def test_download_all_attachment_field_files(
        self, mock_makedirs, mock_exists, mock_request
    ):
        """Test download_all_attachment_field_files method"""
        # Set up mock response for getting the record
        record_response = MagicMock()
        record_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "doc001",
                "name__v": "Test Document",
                "attachment_field1__vs": {
                    "filename": "test_file1.pdf",
                    "format": "application/pdf",
                    "size": 12345,
                },
                "attachment_field2__vs": {
                    "filename": "test_file2.jpg",
                    "format": "image/jpeg",
                    "size": 54321,
                },
                "regular_field__c": "Some value",
            },
        }
        mock_request.return_value = record_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_fields_service = ObjectAttachmentFieldsService(client)

        # Patch the download_attachment_field_file method
        with patch.object(
            attachment_fields_service,
            "download_attachment_field_file",
            return_value="File downloaded successfully",
        ) as mock_download:
            # Call method to test
            result = attachment_fields_service.download_all_attachment_field_files(
                "document__v", "doc001", "/test/download/dir"
            )

            # Verify directory was created
            mock_makedirs.assert_called_once_with("/test/download/dir")

            # Verify download method was called for each attachment field
            assert mock_download.call_count == 2
            mock_download.assert_any_call(
                "document__v",
                "doc001",
                "attachment_field1__vs",
                "/test/download/dir/test_file1.pdf",
            )
            mock_download.assert_any_call(
                "document__v",
                "doc001",
                "attachment_field2__vs",
                "/test/download/dir/test_file2.jpg",
            )

            # Verify result structure
            assert result["total"] == 2
            assert result["success"] == 2
            assert result["failed"] == 0
            assert len(result["files"]) == 2
            assert result["files"][0]["field"] == "attachment_field1__vs"
            assert result["files"][0]["status"] == "success"
            assert result["files"][1]["field"] == "attachment_field2__vs"

    @patch("requests.request")
    def test_update_attachment_field_file(self, mock_request):
        """Test update_attachment_field_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "doc001",
                "attachment_field__vs": {
                    "filename": "new_file.pdf",
                    "format": "application/pdf",
                    "size": 54321,
                },
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
        attachment_fields_service = ObjectAttachmentFieldsService(client)

        # Mock open for file
        with patch("builtins.open", mock_open(read_data=b"file content")):
            with patch("os.path.basename", return_value="new_file.pdf"):
                # Call method to test
                result = attachment_fields_service.update_attachment_field_file(
                    "document__v",
                    "doc001",
                    "attachment_field__vs",
                    "/path/to/new_file.pdf",
                )

                # Verify request was made with correct parameters
                mock_request.assert_called_once()
                args, kwargs = mock_request.call_args
                assert kwargs["url"].endswith(
                    "/api/v25.1/vobjects/document__v/doc001/attachmentfields/attachment_field__vs"
                )
                assert kwargs["method"] == "PUT"
                assert "files" in kwargs

                # Verify response parsing
                assert result["responseStatus"] == "SUCCESS"
                assert result["data"]["id"] == "doc001"
                assert (
                    result["data"]["attachment_field__vs"]["filename"] == "new_file.pdf"
                )


@mark.integration
@mark.veevavault
class TestObjectAttachmentFieldsServiceIntegration:
    """
    Integration tests for ObjectAttachmentFieldsService using real API calls
    """

    def test_download_attachment_field_files(
        self, authenticated_vault_client, vault_config
    ):
        """Test downloading attachment field files"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        attachment_fields_service = ObjectAttachmentFieldsService(
            authenticated_vault_client
        )

        # Skip actual API call in this template
        pytest.skip(
            "Integration test requires a valid object record with attachment fields"
        )
