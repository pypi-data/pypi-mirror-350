from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.quality_docs import QualityDocsService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.quality_docs
class TestQualityDocsServiceUnit:
    """
    Unit tests for QualityDocsService class using mocks (no real API calls)
    """

    @fixture
    def quality_docs_service(self):
        """Fixture for creating a QualityDocsService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return QualityDocsService(client)

    @patch("requests.request")
    def test_document_role_check_for_document_change_control(
        self, mock_request, quality_docs_service
    ):
        """Test document_role_check_for_document_change_control method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "check_result": True,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        quality_docs_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        object_record_id = "dcc123"
        application_role = "reviewer__v"

        # Call method
        result = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id, application_role
        )

        # Verify client.api_call was called with correct parameters
        quality_docs_service.client.api_call.assert_called_once()
        args, kwargs = quality_docs_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/document_change_control__v/dcc123/actions/documentrolecheck"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == {"application_role": "reviewer__v"}
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["check_result"] is True


@mark.integration
@mark.veevavault
@mark.quality_docs
class TestQualityDocsServiceIntegration:
    """
    Integration tests for QualityDocsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def quality_docs_service(self, authenticated_vault_client):
        """Fixture for creating a QualityDocsService instance with a real client"""
        return QualityDocsService(authenticated_vault_client)

    def test_document_role_check_for_document_change_control(
        self, quality_docs_service, vault_config
    ):
        """Test document_role_check_for_document_change_control with real API"""
        # Skip if not authenticated
        if not quality_docs_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real document change control data
        pytest.skip(
            "This test requires a real document change control ID and appropriate permissions"
        )
