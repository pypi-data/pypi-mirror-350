from pytest import mark, fixture
import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open, ANY

from veevavault.client import VaultClient
from veevavault.services.objects.attachments_service import ObjectAttachmentsService


@mark.unit
@mark.veevavault
class TestObjectAttachmentsServiceUnit:
    """
    Unit tests for ObjectAttachmentsService
    """

    @patch("requests.request")
    def test_determine_if_attachments_are_enabled_on_object(self, mock_request):
        """Test determine_if_attachments_are_enabled_on_an_object method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "object": {
                "name": "document__v",
                "label": "Document",
                "allow_attachments": True,
                "urls": {
                    "attachments": "/api/v25.1/vobjects/document__v/{id}/attachments"
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.determine_if_attachments_are_enabled_on_an_object(
            "document__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/vobjects/document__v")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["object"]["allow_attachments"] == True
        assert "attachments" in result["object"]["urls"]

    @patch("requests.request")
    def test_retrieve_object_record_attachments(self, mock_request):
        """Test retrieve_object_record_attachments method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "attachments": [
                {
                    "id": "att001",
                    "filename": "test_file.pdf",
                    "format": "application/pdf",
                    "size": 12345,
                    "md5checksum": "abcdef1234567890",
                    "version": 1,
                    "created_by": "user123",
                    "created_date": "2023-01-01T12:00:00.000Z",
                },
                {
                    "id": "att002",
                    "filename": "test_image.jpg",
                    "format": "image/jpeg",
                    "size": 54321,
                    "md5checksum": "0987654321fedcba",
                    "version": 2,
                    "created_by": "user123",
                    "created_date": "2023-01-02T12:00:00.000Z",
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.retrieve_object_record_attachments(
            "document__v", "doc001"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["attachments"]) == 2
        assert result["attachments"][0]["id"] == "att001"
        assert result["attachments"][0]["filename"] == "test_file.pdf"
        assert result["attachments"][1]["id"] == "att002"

    @patch("requests.request")
    def test_retrieve_object_record_attachment_metadata(self, mock_request):
        """Test retrieve_object_record_attachment_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "attachment": {
                "id": "att001",
                "filename": "test_file.pdf",
                "format": "application/pdf",
                "size": 12345,
                "md5checksum": "abcdef1234567890",
                "version": 1,
                "created_by": "user123",
                "created_date": "2023-01-01T12:00:00.000Z",
                "description": "Test PDF document",
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.retrieve_object_record_attachment_metadata(
            "document__v", "doc001", "att001"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["attachment"]["id"] == "att001"
        assert result["attachment"]["filename"] == "test_file.pdf"
        assert result["attachment"]["description"] == "Test PDF document"

    @patch("requests.request")
    def test_retrieve_object_record_attachment_versions(self, mock_request):
        """Test retrieve_object_record_attachment_versions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "versions": [
                {
                    "version": 1,
                    "created_by": "user123",
                    "created_date": "2023-01-01T12:00:00.000Z",
                    "url": "/api/v25.1/vobjects/document__v/doc001/attachments/att001/versions/1",
                },
                {
                    "version": 2,
                    "created_by": "user456",
                    "created_date": "2023-01-02T12:00:00.000Z",
                    "url": "/api/v25.1/vobjects/document__v/doc001/attachments/att001/versions/2",
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.retrieve_object_record_attachment_versions(
            "document__v", "doc001", "att001"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001/versions"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["versions"]) == 2
        assert result["versions"][0]["version"] == 1
        assert result["versions"][1]["version"] == 2

    @patch("requests.request")
    def test_retrieve_object_record_attachment_version_metadata(self, mock_request):
        """Test retrieve_object_record_attachment_version_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "version": {
                "version": 1,
                "created_by": "user123",
                "created_date": "2023-01-01T12:00:00.000Z",
                "filename": "test_file.pdf",
                "format": "application/pdf",
                "size": 12345,
                "md5checksum": "abcdef1234567890",
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.retrieve_object_record_attachment_version_metadata(
            "document__v", "doc001", "att001", "1"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001/versions/1"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["version"]["version"] == 1
        assert result["version"]["filename"] == "test_file.pdf"

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_object_record_attachment_file(self, mock_file, mock_request):
        """Test download_object_record_attachment_file method"""
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
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.download_object_record_attachment_file(
            "document__v", "doc001", "att001", "test_download.pdf"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001/file"
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
    def test_download_all_object_record_attachment_files(
        self, mock_makedirs, mock_exists, mock_path_exists, mock_request
    ):
        """Test download_all_object_record_attachment_files method"""
        # Set up mock response for getting attachments
        first_response = MagicMock()
        first_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "attachments": [
                {
                    "id": "att001",
                    "filename": "test_file.pdf",
                    "format": "application/pdf",
                },
                {"id": "att002", "filename": "test_image.jpg", "format": "image/jpeg"},
            ],
        }

        # Set up mock responses for downloading files
        download_response = MagicMock()
        download_response.iter_content.return_value = [b"file content"]

        # Configure mock to return different responses for different calls
        mock_request.side_effect = [first_response] + [download_response] * 2

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_service = ObjectAttachmentsService(client)

        # Patch the download_object_record_attachment_file method
        with patch.object(
            attachment_service,
            "download_object_record_attachment_file",
            return_value="File downloaded successfully",
        ) as mock_download:
            # Call method to test
            result = attachment_service.download_all_object_record_attachment_files(
                "document__v", "doc001", "/test/download/dir"
            )

            # Verify directory was created
            mock_makedirs.assert_called_once_with("/test/download/dir")

            # Verify download method was called for each attachment
            assert mock_download.call_count == 2
            mock_download.assert_any_call(
                "document__v", "doc001", "att001", "/test/download/dir/test_file.pdf"
            )
            mock_download.assert_any_call(
                "document__v", "doc001", "att002", "/test/download/dir/test_image.jpg"
            )

            # Verify result structure
            assert result["total"] == 2
            assert result["success"] == 2
            assert result["failed"] == 0
            assert len(result["files"]) == 2
            assert result["files"][0]["id"] == "att001"
            assert result["files"][0]["status"] == "success"
            assert result["files"][1]["id"] == "att002"

    @patch("requests.request")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_object_record_attachment(self, mock_file, mock_request):
        """Test create_object_record_attachment method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "attachment": {"id": "att003", "version": 1},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.create_object_record_attachment(
            "document__v", "doc001", "test_file.pdf", "Test attachment description"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments"
        )
        assert kwargs["method"] == "POST"
        assert "files" in kwargs
        assert kwargs["data"] == {"description": "Test attachment description"}

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["attachment"]["id"] == "att003"
        assert result["attachment"]["version"] == 1

    @patch("requests.request")
    def test_update_object_record_attachment_description(self, mock_request):
        """Test update_object_record_attachment_description method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "attachment": {"id": "att001", "description": "Updated description"},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.update_object_record_attachment_description(
            "document__v", "doc001", "att001", "Updated description"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["data"] == {"description__v": "Updated description"}

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["attachment"]["id"] == "att001"
        assert result["attachment"]["description"] == "Updated description"

    @patch("requests.request")
    def test_delete_object_record_attachment(self, mock_request):
        """Test delete_object_record_attachment method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully deleted attachment",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        attachment_service = ObjectAttachmentsService(client)

        # Call method to test
        result = attachment_service.delete_object_record_attachment(
            "document__v", "doc001", "att001"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/document__v/doc001/attachments/att001"
        )
        assert kwargs["method"] == "DELETE"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseMessage"] == "Successfully deleted attachment"


@mark.integration
@mark.veevavault
class TestObjectAttachmentsServiceIntegration:
    """
    Integration tests for ObjectAttachmentsService using real API calls
    """

    def test_retrieve_object_record_attachments(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving attachments for an object record"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        attachment_service = ObjectAttachmentsService(authenticated_vault_client)

        # Skip actual API call in this template
        pytest.skip("Integration test requires a valid object record with attachments")
