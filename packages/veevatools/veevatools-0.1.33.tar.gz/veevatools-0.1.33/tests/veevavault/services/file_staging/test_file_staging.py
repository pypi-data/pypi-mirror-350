from pytest import mark, fixture
import pytest
import requests
import os
import io
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.file_staging import FileStagingService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
class TestFileStagingServiceUnit:
    """
    Unit tests for FileStagingService class using mocks (no real API calls)
    """

    def setup_method(self):
        """Set up test environment before each test method"""
        # Create mocked client
        self.client = VaultClient()
        self.client.vaultURL = "https://test.veevavault.com"
        self.client.sessionId = "test-session-id"
        self.client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        self.service = FileStagingService(self.client)

    @patch("requests.request")
    def test_list_items_at_path(self, mock_request):
        """Test list_items_at_path method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "items": [
                {
                    "kind": "folder",
                    "path": "/users/test_user/folder1",
                    "name": "folder1",
                },
                {
                    "kind": "file",
                    "path": "/users/test_user/file1.txt",
                    "name": "file1.txt",
                    "size": 1024,
                    "modified_date": "2023-01-01T00:00:00Z",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.list_items_at_path("users/test_user")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/items/users/test_user"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["params"]["recursive"] == "false"
        assert kwargs["params"]["limit"] == 1000

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["items"]) == 2
        assert result["items"][0]["kind"] == "folder"
        assert result["items"][1]["kind"] == "file"

    @patch("requests.request")
    def test_download_item_content(self, mock_request):
        """Test download_item_content method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"file content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.download_item_content("users/test_user/file1.txt")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/items/content/users/test_user/file1.txt"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert result == mock_response

    @patch("requests.request")
    def test_download_item_content_with_range(self, mock_request):
        """Test download_item_content method with byte range"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"file content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test with byte range
        result = self.service.download_item_content(
            "users/test_user/file1.txt", byte_range=(0, 100)
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["headers"]["Range"] == "bytes=0-100"

        # Verify response
        assert result == mock_response

    @patch("requests.request")
    def test_create_folder(self, mock_request):
        """Test create_folder_or_file method for creating a folder"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "kind": "folder",
            "path": "/users/test_user/new_folder",
            "name": "new_folder",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.create_folder_or_file(
            path="users/test_user/new_folder", kind="folder"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/services/file_staging/items")
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["path"] == "users/test_user/new_folder"
        assert kwargs["data"]["kind"] == "folder"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["kind"] == "folder"
        assert result["path"] == "/users/test_user/new_folder"

    @patch("requests.request")
    def test_create_file(self, mock_request):
        """Test create_folder_or_file method for creating a file"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "kind": "file",
            "path": "/users/test_user/new_file.txt",
            "name": "new_file.txt",
            "size": 10,
            "file_content_md5": "abcd1234",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test with mocked file
        with patch(
            "builtins.open", mock_open(read_data=b"test data")
        ) as mock_file_open:
            result = self.service.create_folder_or_file(
                path="users/test_user/new_file.txt",
                kind="file",
                file="local_file.txt",
                overwrite=True,
            )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["path"] == "users/test_user/new_file.txt"
        assert kwargs["data"]["kind"] == "file"
        assert kwargs["data"]["overwrite"] == "true"
        assert "files" in kwargs

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["kind"] == "file"
        assert result["path"] == "/users/test_user/new_file.txt"
        assert result["size"] == 10

    @patch("requests.request")
    def test_update_folder_or_file(self, mock_request):
        """Test update_folder_or_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job-123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job-123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.update_folder_or_file(
            item_path="users/test_user/old_folder",
            parent="users/test_user/parent_folder",
            name="new_folder",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/items/users/test_user/old_folder"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"]["parent"] == "users/test_user/parent_folder"
        assert kwargs["data"]["name"] == "new_folder"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job-123"

    def test_update_folder_or_file_error(self):
        """Test update_folder_or_file method with missing parameters"""
        # Should raise ValueError if both parent and name are None
        with pytest.raises(ValueError):
            self.service.update_folder_or_file(item_path="users/test_user/old_folder")

    @patch("requests.request")
    def test_delete_file_or_folder(self, mock_request):
        """Test delete_file_or_folder method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job-123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job-123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.delete_file_or_folder("users/test_user/file1.txt")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/items/users/test_user/file1.txt"
        )
        assert kwargs["method"] == "DELETE"
        assert kwargs["params"] == {}

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job-123"

    @patch("requests.request")
    def test_delete_folder_recursive(self, mock_request):
        """Test delete_file_or_folder method with recursive option"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job-123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job-123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.delete_file_or_folder(
            "users/test_user/folder1", recursive=True
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/items/users/test_user/folder1"
        )
        assert kwargs["method"] == "DELETE"
        assert kwargs["params"]["recursive"] == "true"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job-123"

    @patch("requests.request")
    def test_create_resumable_upload_session(self, mock_request):
        """Test create_resumable_upload_session method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "path": "/users/test_user/large_file.zip",
            "id": "upload-session-123",
            "expiration_date": "2023-01-02T00:00:00Z",
            "created_date": "2023-01-01T00:00:00Z",
            "last_uploaded_date": None,
            "owner": "user-123",
            "uploaded_parts": 0,
            "size": 100000000,
            "uploaded": 0,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.create_resumable_upload_session(
            path="users/test_user/large_file.zip", size=100000000, overwrite=True
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/services/file_staging/upload")
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["path"] == "users/test_user/large_file.zip"
        assert kwargs["data"]["size"] == 100000000
        assert kwargs["data"]["overwrite"] == "true"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "upload-session-123"
        assert result["size"] == 100000000

    @patch("requests.request")
    def test_upload_to_session(self, mock_request):
        """Test upload_to_session method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "size": 10485760,
            "part_number": 1,
            "part_content_md5": "abcd1234",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create test file part data
        file_part = b"x" * 10485760

        # Call method to test
        result = self.service.upload_to_session(
            upload_session_id="upload-session-123",
            file_part=file_part,
            part_number=1,
            content_md5="abcd1234",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/upload/upload-session-123"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/octet-stream"
        assert kwargs["headers"]["X-VaultAPI-FilePartNumber"] == "1"
        assert kwargs["headers"]["Content-MD5"] == "abcd1234"
        assert kwargs["headers"]["Content-Length"] == str(len(file_part))
        assert kwargs["data"] == file_part

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["size"] == 10485760
        assert result["part_number"] == 1

    @patch("requests.request")
    def test_commit_upload_session(self, mock_request):
        """Test commit_upload_session method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job-123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job-123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.commit_upload_session("upload-session-123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/upload/upload-session-123"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job-123"

    @patch("requests.request")
    def test_list_upload_sessions(self, mock_request):
        """Test list_upload_sessions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "sessions": [
                {
                    "path": "/users/test_user/file1.zip",
                    "id": "upload-session-123",
                    "expiration_date": "2023-01-02T00:00:00Z",
                    "created_date": "2023-01-01T00:00:00Z",
                    "last_uploaded_date": "2023-01-01T00:30:00Z",
                    "owner": "user-123",
                    "uploaded_parts": 5,
                    "size": 100000000,
                    "uploaded": 50000000,
                },
                {
                    "path": "/users/test_user/file2.zip",
                    "id": "upload-session-456",
                    "expiration_date": "2023-01-03T00:00:00Z",
                    "created_date": "2023-01-01T12:00:00Z",
                    "last_uploaded_date": "2023-01-01T12:30:00Z",
                    "owner": "user-123",
                    "uploaded_parts": 2,
                    "size": 50000000,
                    "uploaded": 20000000,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.list_upload_sessions()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/services/file_staging/upload")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["sessions"]) == 2
        assert result["sessions"][0]["id"] == "upload-session-123"
        assert result["sessions"][1]["id"] == "upload-session-456"

    @patch("requests.request")
    def test_get_upload_session_details(self, mock_request):
        """Test get_upload_session_details method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "path": "/users/test_user/file1.zip",
            "id": "upload-session-123",
            "expiration_date": "2023-01-02T00:00:00Z",
            "created_date": "2023-01-01T00:00:00Z",
            "last_uploaded_date": "2023-01-01T00:30:00Z",
            "owner": "user-123",
            "uploaded_parts": 5,
            "size": 100000000,
            "uploaded": 50000000,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.get_upload_session_details("upload-session-123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/upload/upload-session-123"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "upload-session-123"
        assert result["uploaded_parts"] == 5
        assert result["size"] == 100000000

    @patch("requests.request")
    def test_list_file_parts_uploaded_to_session(self, mock_request):
        """Test list_file_parts_uploaded_to_session method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "parts": [
                {
                    "part_number": 1,
                    "size": 10485760,
                },
                {
                    "part_number": 2,
                    "size": 10485760,
                },
                {
                    "part_number": 3,
                    "size": 10485760,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.list_file_parts_uploaded_to_session("upload-session-123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/upload/upload-session-123/parts"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["params"]["limit"] == 1000

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["parts"]) == 3
        assert result["parts"][0]["part_number"] == 1
        assert result["parts"][1]["part_number"] == 2

    @patch("requests.request")
    def test_abort_upload_session(self, mock_request):
        """Test abort_upload_session method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call method to test
        result = self.service.abort_upload_session("upload-session-123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/services/file_staging/upload/upload-session-123"
        )
        assert kwargs["method"] == "DELETE"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestFileStagingServiceIntegration:
    """
    Integration tests for FileStagingService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_vault_client, vault_config):
        """Set up test environment before each test"""
        # Skip all integration tests if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available for integration tests")

        # Create service with authenticated client
        self.service = FileStagingService(authenticated_vault_client)
        self.test_folder_path = f"users/{vault_config.username}/test_folder"
        self.test_file_path = f"users/{vault_config.username}/test_file.txt"

        # Clean up any leftovers from previous test runs
        self._cleanup_test_data()

        yield

        # Clean up after tests
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up test data before/after tests"""
        try:
            # Try to delete test file
            self.service.delete_file_or_folder(self.test_file_path)
        except:
            pass

        try:
            # Try to delete test folder (recursive)
            self.service.delete_file_or_folder(self.test_folder_path, recursive=True)
        except:
            pass

    def test_create_and_list_folder(self):
        """Test creating a folder and listing its contents"""
        # Create a test folder
        create_result = self.service.create_folder_or_file(
            path=self.test_folder_path, kind="folder"
        )

        # Verify the folder was created successfully
        assert create_result["responseStatus"] == "SUCCESS"
        assert create_result["kind"] == "folder"
        assert self.test_folder_path in create_result["path"]

        # List the items in the parent directory
        parent_path = os.path.dirname(self.test_folder_path)
        list_result = self.service.list_items_at_path(parent_path)

        # Verify the folder appears in the listing
        assert list_result["responseStatus"] == "SUCCESS"
        folder_found = False
        for item in list_result["items"]:
            if (
                item["kind"] == "folder"
                and os.path.basename(self.test_folder_path) in item["name"]
            ):
                folder_found = True
                break

        assert folder_found, "Created folder not found in directory listing"

    def test_create_update_file(self):
        """Test creating and updating a file"""
        # Skip test if not possible to create a local file
        try:
            # Create a local temp file
            with open("temp_test_file.txt", "w") as f:
                f.write("Test content for file staging")

            # Create test file in vault
            create_result = self.service.create_folder_or_file(
                path=self.test_file_path, kind="file", file="temp_test_file.txt"
            )

            # Verify the file was created successfully
            assert create_result["responseStatus"] == "SUCCESS"
            assert create_result["kind"] == "file"
            assert self.test_file_path in create_result["path"]

            # Update the file (rename it)
            new_file_name = "updated_test_file.txt"
            update_result = self.service.update_folder_or_file(
                item_path=self.test_file_path, name=new_file_name
            )

            # Verify the update job was initiated
            assert update_result["responseStatus"] == "SUCCESS"
            assert "job_id" in update_result

        finally:
            # Clean up local temp file
            if os.path.exists("temp_test_file.txt"):
                os.remove("temp_test_file.txt")

    def test_resumable_upload_session(self):
        """Test resumable upload session functionality"""
        # Skip test because it requires handling large files
        pytest.skip(
            "Skipping resumable upload test as it requires handling of large files (5MB+)"
        )

    def test_download_file_content(self):
        """Test downloading file content"""
        # Skip test if authentication is missing
        if not hasattr(self, "service"):
            pytest.skip("Service not initialized - authentication may be missing")

        # Skip test as it requires an existing file to download
        pytest.skip(
            "Skipping download test as it requires an existing file in the vault"
        )

    def test_list_upload_sessions(self):
        """Test listing upload sessions"""
        # This test just verifies the API call works
        result = self.service.list_upload_sessions()
        assert result["responseStatus"] == "SUCCESS"
        # Note: Result may have empty sessions list if no active uploads
