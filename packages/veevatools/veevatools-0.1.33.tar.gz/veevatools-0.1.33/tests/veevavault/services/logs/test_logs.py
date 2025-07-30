from pytest import mark, fixture
import pytest
import json
import datetime
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.logs import LogsService


@mark.unit
@mark.veevavault
class TestLogsServiceUnit:
    """
    Unit tests for LogsService class using mocks (no real API calls)
    """

    def test_retrieve_audit_types(self, authenticated_vault_client):
        """Test retrieving all audit types"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "audittrail": [
                {
                    "name": "document_audit_trail",
                    "label": "Document Audit Trail",
                    "url": "/api/v25.1/metadata/audittrail/document_audit_trail",
                },
                {
                    "name": "object_audit_trail",
                    "label": "Object Audit Trail",
                    "url": "/api/v25.1/metadata/audittrail/object_audit_trail",
                },
            ],
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_audit_types()

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once_with(
            f"api/{authenticated_vault_client.LatestAPIversion}/metadata/audittrail"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["audittrail"]) == 2
        assert result["audittrail"][0]["name"] == "document_audit_trail"
        assert result["audittrail"][1]["name"] == "object_audit_trail"

    def test_retrieve_audit_metadata(self, authenticated_vault_client):
        """Test retrieving metadata for a specific audit type"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "name": "document_audit_trail",
            "label": "Document Audit Trail",
            "fields": [
                {"name": "date", "label": "Date", "type": "datetime"},
                {
                    "name": "event_description",
                    "label": "Event Description",
                    "type": "string",
                },
            ],
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_audit_metadata("document_audit_trail")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once_with(
            f"api/{authenticated_vault_client.LatestAPIversion}/metadata/audittrail/document_audit_trail"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "document_audit_trail"
        assert len(result["fields"]) == 2
        assert result["fields"][0]["name"] == "date"
        assert result["fields"][1]["name"] == "event_description"

    def test_retrieve_audit_details(self, authenticated_vault_client):
        """Test retrieving audit details for a specific audit type"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "audittrail_details": [
                {
                    "date": "2023-01-15T07:00:00Z",
                    "user": "test_user",
                    "event": "Create",
                    "event_description": "Document created",
                },
                {
                    "date": "2023-01-16T08:30:00Z",
                    "user": "test_user",
                    "event": "Edit",
                    "event_description": "Document updated",
                },
            ],
            "responseDetails": {"limit": 200, "offset": 0, "size": 2, "total": 2},
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with parameters
        result = logs_service.retrieve_audit_details(
            "document_audit_trail",
            start_date="2023-01-15T00:00:00Z",
            end_date="2023-01-16T23:59:59Z",
            limit=100,
            offset=0,
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/audittrail/document_audit_trail"
        )
        assert kwargs["params"]["start_date"] == "2023-01-15T00:00:00Z"
        assert kwargs["params"]["end_date"] == "2023-01-16T23:59:59Z"
        assert kwargs["params"]["limit"] == "100"
        assert kwargs["params"]["offset"] == "0"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["audittrail_details"]) == 2
        assert result["audittrail_details"][0]["event"] == "Create"
        assert result["audittrail_details"][1]["event"] == "Edit"

    def test_retrieve_document_audit_history(self, authenticated_vault_client):
        """Test retrieving audit history for a specific document"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "audittrail": [
                {
                    "date": "2023-01-15T07:00:00Z",
                    "user": "test_user",
                    "event": "Create",
                    "event_description": "Document created",
                },
                {
                    "date": "2023-01-16T08:30:00Z",
                    "user": "test_user",
                    "event": "Edit",
                    "event_description": "Document updated",
                },
            ],
            "responseDetails": {"limit": 200, "offset": 0, "size": 2, "total": 2},
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with document ID
        result = logs_service.retrieve_document_audit_history("doc_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/objects/documents/doc_123/audittrail"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["audittrail"]) == 2
        assert result["audittrail"][0]["event"] == "Create"
        assert result["audittrail"][1]["event"] == "Edit"

    def test_retrieve_object_audit_history(self, authenticated_vault_client):
        """Test retrieving audit history for a specific object record"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "audittrail": [
                {
                    "date": "2023-01-15T07:00:00Z",
                    "user": "test_user",
                    "event": "Create",
                    "event_description": "Object created",
                },
                {
                    "date": "2023-01-16T08:30:00Z",
                    "user": "test_user",
                    "event": "Edit",
                    "event_description": "Object updated",
                },
            ],
            "responseDetails": {"limit": 200, "offset": 0, "size": 2, "total": 2},
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with object name and ID
        result = logs_service.retrieve_object_audit_history("test_object__v", "obj_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/vobjects/test_object__v/obj_123/audittrail"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["audittrail"]) == 2
        assert result["audittrail"][0]["event"] == "Create"
        assert result["audittrail"][1]["event"] == "Edit"

    def test_retrieve_all_debug_logs(self, authenticated_vault_client):
        """Test retrieving all debug logs"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "logs": [
                {
                    "id": "log_123",
                    "name": "Test Debug Log 1",
                    "user": {"id": "user_123", "name": "Test User"},
                    "created_date": "2023-01-15T07:00:00Z",
                    "status": "active__sys",
                },
                {
                    "id": "log_456",
                    "name": "Test Debug Log 2",
                    "user": {"id": "user_456", "name": "Another User"},
                    "created_date": "2023-01-16T08:30:00Z",
                    "status": "active__sys",
                },
            ],
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_all_debug_logs()

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["logs"]) == 2
        assert result["logs"][0]["id"] == "log_123"
        assert result["logs"][1]["id"] == "log_456"

    def test_retrieve_single_debug_log(self, authenticated_vault_client):
        """Test retrieving a single debug log"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "id": "log_123",
            "name": "Test Debug Log",
            "user": {"id": "user_123", "name": "Test User"},
            "created_date": "2023-01-15T07:00:00Z",
            "status": "active__sys",
            "log_level": "all__sys",
            "files": [
                {
                    "id": "file_123",
                    "name": "debug_log_file.txt",
                    "created_date": "2023-01-15T07:10:00Z",
                }
            ],
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_single_debug_log("log_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug/log_123"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "log_123"
        assert len(result["files"]) == 1
        assert result["files"][0]["id"] == "file_123"

    def test_download_debug_log_files(self, authenticated_vault_client):
        """Test downloading debug log files"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.download_debug_log_files("log_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug/log_123/files"
        )
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data

    def test_create_debug_log(self, authenticated_vault_client):
        """Test creating a debug log"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "id": "log_123",
            "name": "Test Debug Log",
            "user": {"id": "user_123", "name": "Test User"},
            "created_date": "2023-01-15T07:00:00Z",
            "status": "active__sys",
            "log_level": "all__sys",
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.create_debug_log(
            name="Test Debug Log",
            user_id="user_123",
            log_level="all__sys",
            class_filters=["com.veeva.vault.custom.triggers.HelloWorld"],
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == {
            "name": "Test Debug Log",
            "user_id": "user_123",
            "log_level": "all__sys",
            "class_filters": "com.veeva.vault.custom.triggers.HelloWorld",
        }

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == "log_123"
        assert result["log_level"] == "all__sys"

    def test_reset_debug_log(self, authenticated_vault_client):
        """Test resetting a debug log"""
        # Set up mock client response
        mock_response = {"responseStatus": "SUCCESS"}

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.reset_debug_log("log_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug/log_123/actions/reset"
        )
        assert kwargs["method"] == "POST"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"

    def test_delete_debug_log(self, authenticated_vault_client):
        """Test deleting a debug log"""
        # Set up mock client response
        mock_response = {"responseStatus": "SUCCESS"}

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.delete_debug_log("log_123")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/debug/log_123"
        )
        assert kwargs["method"] == "DELETE"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"

    def test_retrieve_all_profiling_sessions(self, authenticated_vault_client):
        """Test retrieving all SDK request profiling sessions"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "sessions": [
                {
                    "id": "session_123",
                    "name": "session1__c",
                    "label": "Test Session 1",
                    "status": "complete__sys",
                    "created_date": "2023-01-15T07:00:00Z",
                },
                {
                    "id": "session_456",
                    "name": "session2__c",
                    "label": "Test Session 2",
                    "status": "complete__sys",
                    "created_date": "2023-01-16T08:30:00Z",
                },
            ],
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_all_profiling_sessions()

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["sessions"]) == 2
        assert result["sessions"][0]["name"] == "session1__c"
        assert result["sessions"][1]["name"] == "session2__c"

    def test_retrieve_profiling_session(self, authenticated_vault_client):
        """Test retrieving a specific SDK request profiling session"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "id": "session_123",
            "name": "session1__c",
            "label": "Test Session 1",
            "status": "complete__sys",
            "created_date": "2023-01-15T07:00:00Z",
            "user": {"id": "user_123", "name": "Test User"},
            "description": "Test description",
            "request_count": 100,
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.retrieve_profiling_session("session1__c")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler/session1__c"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "session1__c"
        assert result["label"] == "Test Session 1"
        assert result["request_count"] == 100

    def test_create_profiling_session(self, authenticated_vault_client):
        """Test creating a new SDK request profiling session"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "id": "session_123",
            "name": "session1__c",
            "label": "Test Session",
            "status": "active__sys",
            "created_date": "2023-01-15T07:00:00Z",
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.create_profiling_session(
            label="Test Session", user_id="user_123", description="Test description"
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == {
            "label": "Test Session",
            "user_id": "user_123",
            "description": "Test description",
        }

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "session1__c"
        assert result["label"] == "Test Session"
        assert result["status"] == "active__sys"

    def test_end_profiling_session(self, authenticated_vault_client):
        """Test ending a profiling session early"""
        # Set up mock client response
        mock_response = {"responseStatus": "SUCCESS"}

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.end_profiling_session("session1__c")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler/session1__c/actions/end"
        )
        assert kwargs["method"] == "POST"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"

    def test_delete_profiling_session(self, authenticated_vault_client):
        """Test deleting an inactive profiling session"""
        # Set up mock client response
        mock_response = {"responseStatus": "SUCCESS"}

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.delete_profiling_session("session1__c")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler/session1__c"
        )
        assert kwargs["method"] == "DELETE"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"

    def test_download_profiling_session_results(self, authenticated_vault_client):
        """Test downloading profiling session results"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.download_profiling_session_results("session1__c")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/code/profiler/session1__c/results"
        )
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data

    def test_retrieve_email_notification_histories(self, authenticated_vault_client):
        """Test retrieving email notification histories"""
        # Set up mock client response
        mock_response = {
            "responseStatus": "SUCCESS",
            "notifications": [
                {
                    "id": "notification_123",
                    "date": "2023-01-15T07:00:00Z",
                    "recipient": "user@example.com",
                    "subject": "Test Notification 1",
                    "status": "delivered",
                },
                {
                    "id": "notification_456",
                    "date": "2023-01-16T08:30:00Z",
                    "recipient": "user@example.com",
                    "subject": "Test Notification 2",
                    "status": "delivered",
                },
            ],
            "responseDetails": {"limit": 200, "offset": 0, "size": 2, "total": 2},
        }

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_response)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with parameters
        result = logs_service.retrieve_email_notification_histories(
            start_date="2023-01-15T00:00:00Z",
            end_date="2023-01-16T23:59:59Z",
            limit=100,
            offset=0,
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/notifications/histories"
        )
        assert kwargs["params"]["start_date"] == "2023-01-15T00:00:00Z"
        assert kwargs["params"]["end_date"] == "2023-01-16T23:59:59Z"
        assert kwargs["params"]["limit"] == "100"
        assert kwargs["params"]["offset"] == "0"

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["notifications"]) == 2
        assert result["notifications"][0]["id"] == "notification_123"
        assert result["notifications"][1]["id"] == "notification_456"

    def test_download_daily_api_usage(self, authenticated_vault_client):
        """Test downloading daily API usage logs"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.download_daily_api_usage("2023-01-15", log_format="csv")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/api_usage"
        )
        assert kwargs["params"]["date"] == "2023-01-15"
        assert "log_format" not in kwargs["params"]  # Since default is csv
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data

    def test_download_daily_api_usage_with_logfile_format(
        self, authenticated_vault_client
    ):
        """Test downloading daily API usage logs with logfile format"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with non-default format
        result = logs_service.download_daily_api_usage(
            "2023-01-15", log_format="logfile"
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/api_usage"
        )
        assert kwargs["params"]["date"] == "2023-01-15"
        assert kwargs["params"]["log_format"] == "logfile"
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data

    def test_download_sdk_runtime_log(self, authenticated_vault_client):
        """Test downloading SDK runtime logs"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test
        result = logs_service.download_sdk_runtime_log("2023-01-15", log_format="csv")

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/runtime"
        )
        assert kwargs["params"]["date"] == "2023-01-15"
        assert "log_format" not in kwargs["params"]  # Since default is csv
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data

    def test_download_sdk_runtime_log_with_logfile_format(
        self, authenticated_vault_client
    ):
        """Test downloading SDK runtime logs with logfile format"""
        # Mock binary response data
        mock_binary_data = b"mock binary data"

        # Mock the client's api_call method
        authenticated_vault_client.api_call = MagicMock(return_value=mock_binary_data)

        # Create service instance
        logs_service = LogsService(authenticated_vault_client)

        # Call method to test with non-default format
        result = logs_service.download_sdk_runtime_log(
            "2023-01-15", log_format="logfile"
        )

        # Verify api_call was called with correct parameters
        authenticated_vault_client.api_call.assert_called_once()
        args, kwargs = authenticated_vault_client.api_call.call_args
        assert (
            args[0]
            == f"api/{authenticated_vault_client.LatestAPIversion}/logs/code/runtime"
        )
        assert kwargs["params"]["date"] == "2023-01-15"
        assert kwargs["params"]["log_format"] == "logfile"
        assert kwargs["binary_response"] is True

        # Verify the result
        assert result == mock_binary_data


@mark.integration
@mark.veevavault
class TestLogsServiceIntegration:
    """
    Integration tests for LogsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_audit_types(self, logs_service, authenticated_vault_client):
        """Test retrieving all audit types with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # Call method to test
            result = logs_service.retrieve_audit_types()

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"
            assert "audittrail" in result
            assert isinstance(result["audittrail"], list)
            # Verify each entry has required fields
            for audit_type in result["audittrail"]:
                assert "name" in audit_type
                assert "label" in audit_type
                assert "url" in audit_type

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise

    def test_retrieve_audit_metadata(self, logs_service, authenticated_vault_client):
        """Test retrieving metadata for an audit trail with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # First get available audit types to ensure we use a valid one
            audit_types = logs_service.retrieve_audit_types()
            if not audit_types.get("audittrail"):
                pytest.skip("No audit types available for testing")

            # Use the first available audit type
            audit_type_name = audit_types["audittrail"][0]["name"]

            # Call method to test with real audit type
            result = logs_service.retrieve_audit_metadata(audit_type_name)

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"
            assert "name" in result
            assert result["name"] == audit_type_name
            assert "fields" in result
            assert isinstance(result["fields"], list)

            # Verify each field has required properties
            for field in result["fields"]:
                assert "name" in field
                assert "label" in field
                assert "type" in field

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise

    def test_retrieve_audit_details_limited_range(
        self, logs_service, authenticated_vault_client
    ):
        """Test retrieving audit details for a limited date range with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # First get available audit types to ensure we use a valid one
            audit_types = logs_service.retrieve_audit_types()
            if not audit_types.get("audittrail"):
                pytest.skip("No audit types available for testing")

            # Use the first available audit type
            audit_type_name = audit_types["audittrail"][0]["name"]

            # Use a small date range (1 day) to limit data and avoid timeouts
            end_date = datetime.datetime.utcnow()
            start_date = end_date - datetime.timedelta(days=1)

            # Format dates as expected by the API
            start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Call method to test with real audit type and limited date range
            result = logs_service.retrieve_audit_details(
                audit_type_name,
                start_date=start_date_str,
                end_date=end_date_str,
                limit=10,  # Limit to 10 results for faster response
            )

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"
            assert "responseDetails" in result

            # Details can be in different keys depending on the audit type
            has_details = False
            for possible_key in ["audittrail_details", "audit_details", "details"]:
                if possible_key in result:
                    assert isinstance(result[possible_key], list)
                    has_details = True
                    break

            # If no audit details were found, that's okay for this test
            # We're just validating the API call works
            if not has_details:
                assert "responseDetails" in result
                assert "total" in result["responseDetails"]

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise

    def test_retrieve_debug_logs(self, logs_service, authenticated_vault_client):
        """Test retrieving debug logs with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # Call method to test - just retrieve all debug logs
            result = logs_service.retrieve_all_debug_logs()

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"

            # If logs exist, verify their structure
            if "logs" in result and result["logs"]:
                for log in result["logs"]:
                    assert "id" in log
                    assert "name" in log
                    assert "status" in log

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise

    def test_retrieve_profiling_sessions(
        self, logs_service, authenticated_vault_client
    ):
        """Test retrieving profiling sessions with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # Call method to test - just retrieve all profiling sessions
            result = logs_service.retrieve_all_profiling_sessions()

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"

            # If sessions exist, verify their structure
            if "sessions" in result and result["sessions"]:
                for session in result["sessions"]:
                    assert "id" in session
                    assert "name" in session
                    assert "status" in session

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise

    def test_document_audit_history(self, logs_service, authenticated_vault_client):
        """Test retrieving document audit history with real API"""
        # Skip this test as it requires a specific document ID
        pytest.skip("Skipping test that requires a specific document ID")

    def test_object_audit_history(self, logs_service, authenticated_vault_client):
        """Test retrieving object audit history with real API"""
        # Skip this test as it requires a specific object record ID
        pytest.skip("Skipping test that requires a specific object record ID")

    def test_create_debug_log(self, logs_service, authenticated_vault_client):
        """Test creating a debug log with real API"""
        # Skip this test as it creates resources in the system
        pytest.skip("Skipping test that creates resources in the system")

    def test_email_notification_histories(
        self, logs_service, authenticated_vault_client
    ):
        """Test retrieving email notification histories with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        try:
            # Use a small date range (1 day) to limit data and avoid timeouts
            end_date = datetime.datetime.utcnow()
            start_date = end_date - datetime.timedelta(days=1)

            # Format dates as expected by the API
            start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Call method to test with a limited date range
            result = logs_service.retrieve_email_notification_histories(
                start_date=start_date_str,
                end_date=end_date_str,
                limit=10,  # Limit to 10 results for faster response
            )

            # Verify basic structure without relying on specific data
            assert result["responseStatus"] == "SUCCESS"
            assert "responseDetails" in result

            # If notifications exist, verify their structure
            if "notifications" in result and result["notifications"]:
                for notification in result["notifications"]:
                    assert "date" in notification
                    assert "recipient" in notification

        except Exception as e:
            # If the request fails due to permission issues, skip the test
            if "PERMISSION_DENIED" in str(e) or "NOT_FOUND" in str(e):
                pytest.skip(f"Permission denied or not found: {str(e)}")
            else:
                raise
