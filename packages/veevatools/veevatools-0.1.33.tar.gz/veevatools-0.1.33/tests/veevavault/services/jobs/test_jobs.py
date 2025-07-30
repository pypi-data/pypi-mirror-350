from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.jobs import JobsService


@fixture(scope="function")
def jobs_service(authenticated_vault_client):
    """Returns a JobsService instance using the authenticated Vault client"""
    return JobsService(authenticated_vault_client)


@fixture(scope="function")
def mock_job_data():
    """Provides standard mock data for job tests"""
    return {
        "responseStatus": "SUCCESS",
        "job": {
            "id": "job_001",
            "status": "SUCCESS",
            "method": "GET",
            "created_by": {"id": "user_001", "name": "Test User"},
            "created_date": "2024-03-01T12:00:00Z",
            "run_start_date": "2024-03-01T12:01:00Z",
            "run_end_date": "2024-03-01T12:05:00Z",
            "links": [
                {
                    "rel": "results",
                    "href": "/api/v25.1/services/jobs/job_001/results",
                    "method": "GET",
                }
            ],
        },
    }


@mark.unit
@mark.veevavault
class TestJobsServiceUnit:
    """
    Unit tests for JobsService class using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_job_status(self, mock_request, mock_job_data):
        """Test retrieve_job_status method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_job_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_job_data

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test
        result = jobs_service.retrieve_job_status("job_001")

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with("api/v25.1/services/jobs/job_001")

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job"]["id"] == "job_001"
        assert result["job"]["status"] == "SUCCESS"

    @patch("requests.request")
    def test_retrieve_sdk_job_tasks(self, mock_request):
        """Test retrieve_sdk_job_tasks method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "url": "/api/v25.1/services/jobs/job_001/tasks?limit=50&offset=0",
            "responseDetails": {"total": 2, "limit": 50, "offset": 0},
            "job_id": "job_001",
            "tasks": [
                {"id": "task_001", "state": "SUCCESS"},
                {"id": "task_002", "state": "SUCCESS"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test
        result = jobs_service.retrieve_sdk_job_tasks("job_001")

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/job_001/tasks", params={"limit": 50, "offset": 0}
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job_001"
        assert len(result["tasks"]) == 2
        assert result["tasks"][0]["id"] == "task_001"

    @patch("requests.request")
    def test_retrieve_job_histories(self, mock_request):
        """Test retrieve_job_histories method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "OK",
            "url": "/api/v25.1/services/jobs/histories?limit=50&offset=0",
            "responseDetails": {
                "total": 2,
                "limit": 50,
                "offset": 0,
                "next_page": None,
            },
            "jobs": [
                {
                    "job_id": "job_001",
                    "title": "Test Job 1",
                    "status": "SUCCESS",
                    "created_by": "user_001",
                    "created_date": "2024-03-01T12:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-01T12:05:00Z",
                    "run_start_date": "2024-03-01T12:01:00Z",
                    "run_end_date": "2024-03-01T12:05:00Z",
                },
                {
                    "job_id": "job_002",
                    "title": "Test Job 2",
                    "status": "ERRORS_ENCOUNTERED",
                    "created_by": "user_001",
                    "created_date": "2024-03-02T12:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-02T12:05:00Z",
                    "run_start_date": "2024-03-02T12:01:00Z",
                    "run_end_date": "2024-03-02T12:05:00Z",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test with default parameters
        result = jobs_service.retrieve_job_histories()

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/histories", params={"limit": 50, "offset": 0}
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["jobs"]) == 2
        assert result["jobs"][0]["job_id"] == "job_001"
        assert result["jobs"][1]["job_id"] == "job_002"

    @patch("requests.request")
    def test_retrieve_job_histories_with_params(self, mock_request):
        """Test retrieve_job_histories method with parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "OK",
            "url": "/api/v25.1/services/jobs/histories?start_date=2024-03-01T00:00:00Z&end_date=2024-03-31T23:59:59Z&status=success&limit=10&offset=0",
            "responseDetails": {
                "total": 1,
                "limit": 10,
                "offset": 0,
                "next_page": None,
            },
            "jobs": [
                {
                    "job_id": "job_001",
                    "title": "Test Job 1",
                    "status": "SUCCESS",
                    "created_by": "user_001",
                    "created_date": "2024-03-01T12:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-01T12:05:00Z",
                    "run_start_date": "2024-03-01T12:01:00Z",
                    "run_end_date": "2024-03-01T12:05:00Z",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test with parameters
        result = jobs_service.retrieve_job_histories(
            start_date="2024-03-01T00:00:00Z",
            end_date="2024-03-31T23:59:59Z",
            status="success",
            limit=10,
            offset=0,
        )

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/histories",
            params={
                "start_date": "2024-03-01T00:00:00Z",
                "end_date": "2024-03-31T23:59:59Z",
                "status": "success",
                "limit": 10,
                "offset": 0,
            },
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["jobs"]) == 1
        assert result["jobs"][0]["job_id"] == "job_001"
        assert result["jobs"][0]["status"] == "SUCCESS"

    @patch("requests.request")
    def test_retrieve_job_monitors(self, mock_request):
        """Test retrieve_job_monitors method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "OK",
            "url": "/api/v25.1/services/jobs/monitors?limit=50&offset=0",
            "responseDetails": {"total": 2, "limit": 50, "offset": 0},
            "jobs": [
                {
                    "job_id": "job_003",
                    "title": "Test Job 3",
                    "status": "SCHEDULED",
                    "created_by": "user_001",
                    "created_date": "2024-03-10T12:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-10T12:00:00Z",
                    "run_start_date": "2024-03-10T23:00:00Z",
                },
                {
                    "job_id": "job_004",
                    "title": "Test Job 4",
                    "status": "RUNNING",
                    "created_by": "user_001",
                    "created_date": "2024-03-10T11:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-10T11:01:00Z",
                    "run_start_date": "2024-03-10T11:01:00Z",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test
        result = jobs_service.retrieve_job_monitors()

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/monitors", params={"limit": 50, "offset": 0}
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["jobs"]) == 2
        assert result["jobs"][0]["job_id"] == "job_003"
        assert result["jobs"][0]["status"] == "SCHEDULED"
        assert result["jobs"][1]["job_id"] == "job_004"
        assert result["jobs"][1]["status"] == "RUNNING"

    @patch("requests.request")
    def test_retrieve_job_monitors_with_params(self, mock_request):
        """Test retrieve_job_monitors method with parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "OK",
            "url": "/api/v25.1/services/jobs/monitors?start_date=2024-03-10T00:00:00Z&end_date=2024-03-10T23:59:59Z&status=running&limit=10&offset=0",
            "responseDetails": {"total": 1, "limit": 10, "offset": 0},
            "jobs": [
                {
                    "job_id": "job_004",
                    "title": "Test Job 4",
                    "status": "RUNNING",
                    "created_by": "user_001",
                    "created_date": "2024-03-10T11:00:00Z",
                    "modified_by": "user_001",
                    "modified_date": "2024-03-10T11:01:00Z",
                    "run_start_date": "2024-03-10T11:01:00Z",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test with parameters
        result = jobs_service.retrieve_job_monitors(
            start_date="2024-03-10T00:00:00Z",
            end_date="2024-03-10T23:59:59Z",
            status="running",
            limit=10,
            offset=0,
        )

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/monitors",
            params={
                "start_date": "2024-03-10T00:00:00Z",
                "end_date": "2024-03-10T23:59:59Z",
                "status": "running",
                "limit": 10,
                "offset": 0,
            },
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["jobs"]) == 1
        assert result["jobs"][0]["job_id"] == "job_004"
        assert result["jobs"][0]["status"] == "RUNNING"

    @patch("requests.request")
    def test_start_job(self, mock_request):
        """Test start_job method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "url": "/api/v25.1/services/jobs/job_003",
            "job_id": "job_003",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        client.api_call.return_value = mock_response.json.return_value

        # Create service with mocked client
        jobs_service = JobsService(client)

        # Call method to test
        result = jobs_service.start_job("job_003")

        # Verify client method was called with correct parameters
        client.api_call.assert_called_once_with(
            "api/v25.1/services/jobs/start_now/job_003", method="POST"
        )

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job_003"


@mark.integration
@mark.veevavault
class TestJobsServiceIntegration:
    """
    Integration tests for JobsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_job_histories(self, jobs_service, vault_config):
        """Test retrieve_job_histories with real API"""
        # Skip if not authenticated
        if not jobs_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call method to test with limited results
        result = jobs_service.retrieve_job_histories(limit=5)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "jobs" in result
        assert "responseDetails" in result

    def test_retrieve_job_monitors(self, jobs_service, vault_config):
        """Test retrieve_job_monitors with real API"""
        # Skip if not authenticated
        if not jobs_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call method to test with limited results
        result = jobs_service.retrieve_job_monitors(limit=5)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "jobs" in result
        assert "responseDetails" in result

    @pytest.mark.skip(reason="Test requires a valid job ID from a real environment")
    def test_retrieve_job_status(self, jobs_service, vault_config):
        """Test retrieve_job_status with real API"""
        # This test requires a valid job ID from a real environment
        # which is not available in a generic test setup
        pass

    @pytest.mark.skip(reason="Test requires a valid SDK job ID from a real environment")
    def test_retrieve_sdk_job_tasks(self, jobs_service, vault_config):
        """Test retrieve_sdk_job_tasks with real API"""
        # This test requires a valid SDK job ID from a real environment
        # which is not available in a generic test setup
        pass

    @pytest.mark.skip(
        reason="Test requires a valid scheduled job ID from a real environment"
    )
    def test_start_job(self, jobs_service, vault_config):
        """Test start_job with real API"""
        # This test requires a valid scheduled job ID from a real environment
        # which is not available in a generic test setup
        pass
