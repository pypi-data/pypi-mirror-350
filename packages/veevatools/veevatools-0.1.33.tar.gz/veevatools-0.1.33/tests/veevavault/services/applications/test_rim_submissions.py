from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.rim_submissions import RIMSubmissionsService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.rim_submissions
class TestRIMSubmissionsServiceUnit:
    """
    Unit tests for RIMSubmissionsService class using mocks (no real API calls)
    """

    @fixture
    def rim_submissions_service(self):
        """Fixture for creating a RIMSubmissionsService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return RIMSubmissionsService(client)

    @patch("requests.request")
    def test_copy_into_content_plan(self, mock_request, rim_submissions_service):
        """Test copy_into_content_plan method"""
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
        rim_submissions_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        source_id = "source123"
        target_id = "target123"
        order = 1
        copy_documents = True

        # Call method
        result = rim_submissions_service.copy_into_content_plan(
            source_id, target_id, order, copy_documents
        )

        # Verify client.api_call was called with correct parameters
        rim_submissions_service.client.api_call.assert_called_once()
        args, kwargs = rim_submissions_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/rim/content_plans/actions/copyinto"
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == {
            "source_id": "source123",
            "target_id": "target123",
            "order": 1,
            "copy_documents": True,
        }
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"


@mark.integration
@mark.veevavault
@mark.rim_submissions
class TestRIMSubmissionsServiceIntegration:
    """
    Integration tests for RIMSubmissionsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def rim_submissions_service(self, authenticated_vault_client):
        """Fixture for creating a RIMSubmissionsService instance with a real client"""
        return RIMSubmissionsService(authenticated_vault_client)

    def test_copy_into_content_plan(self, rim_submissions_service, vault_config):
        """Test copy_into_content_plan with real API"""
        # Skip if not authenticated
        if not rim_submissions_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real content plan data
        pytest.skip(
            "This test requires real content plan IDs and appropriate permissions"
        )
