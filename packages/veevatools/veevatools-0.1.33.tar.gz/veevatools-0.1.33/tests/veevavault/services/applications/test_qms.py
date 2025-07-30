from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.qms import QMSService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.qms
class TestQMSServiceUnit:
    """
    Unit tests for QMSService class using mocks (no real API calls)
    """

    @fixture
    def qms_service(self):
        """Fixture for creating a QMSService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return QMSService(client)

    @patch("requests.request")
    def test_manage_quality_team_assignments(self, mock_request, qms_service):
        """Test manage_quality_team_assignments method"""
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
        qms_service.client.api_call.return_value = mock_response.json.return_value

        # Test data
        object_name = "quality_event__qdm"
        data = "record_id,user_id,operation,application_role\nqa123,user123,add,reviewer__v"

        # Call method
        result = qms_service.manage_quality_team_assignments(object_name, data)

        # Verify client.api_call was called with correct parameters
        qms_service.client.api_call.assert_called_once()
        args, kwargs = qms_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/quality/qms/teams/vobjects/quality_event__qdm/actions/manageassignments"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"


@mark.integration
@mark.veevavault
@mark.qms
class TestQMSServiceIntegration:
    """
    Integration tests for QMSService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def qms_service(self, authenticated_vault_client):
        """Fixture for creating a QMSService instance with a real client"""
        return QMSService(authenticated_vault_client)

    def test_manage_quality_team_assignments(self, qms_service, vault_config):
        """Test manage_quality_team_assignments with real API"""
        # Skip if not authenticated
        if not qms_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real quality team data
        pytest.skip(
            "This test requires real quality team data and appropriate permissions"
        )
