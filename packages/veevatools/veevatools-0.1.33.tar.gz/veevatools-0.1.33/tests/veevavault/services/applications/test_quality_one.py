from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.quality_one import QualityOneService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.quality_one
class TestQualityOneServiceUnit:
    """
    Unit tests for QualityOneService class using mocks (no real API calls)
    """

    @fixture
    def quality_one_service(self):
        """Fixture for creating a QualityOneService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return QualityOneService(client)

    @patch("requests.request")
    def test_manage_team_assignments(self, mock_request, quality_one_service):
        """Test manage_team_assignments method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "jobId": "job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        quality_one_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        object_name = "risk_event__v"
        data = "record_id,user_id,operation,application_role\nrisk123,user123,add,reviewer__v"

        # Call method
        result = quality_one_service.manage_team_assignments(object_name, data)

        # Verify client.api_call was called with correct parameters
        quality_one_service.client.api_call.assert_called_once()
        args, kwargs = quality_one_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/qualityone/qms/teams/vobjects/risk_event__v/actions/manageassignments"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["jobId"] == "job123"


@mark.integration
@mark.veevavault
@mark.quality_one
class TestQualityOneServiceIntegration:
    """
    Integration tests for QualityOneService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def quality_one_service(self, authenticated_vault_client):
        """Fixture for creating a QualityOneService instance with a real client"""
        return QualityOneService(authenticated_vault_client)

    def test_manage_team_assignments(self, quality_one_service, vault_config):
        """Test manage_team_assignments with real API"""
        # Skip if not authenticated
        if not quality_one_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real team assignment data
        pytest.skip(
            "This test requires real team assignment data and appropriate permissions"
        )
