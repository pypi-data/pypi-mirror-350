from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.rollup_service import ObjectRollupService


@mark.unit
@mark.veevavault
class TestObjectRollupServiceUnit:
    """
    Unit tests for ObjectRollupService
    """

    @patch("requests.request")
    def test_recalculate_rollup_fields_all_records(self, mock_request):
        """Test recalculate_rollup_fields method for all records"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Recalculation of rollup fields started",
            "job_id": "job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        rollup_service = ObjectRollupService(client)

        # Call method to test for all records
        result = rollup_service.recalculate_rollup_fields("product__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/actions/recalculaterollups"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["data"] in (None, "{}")  # Empty data or None

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_recalculate_rollup_fields_specific_record(self, mock_request):
        """Test recalculate_rollup_fields method for a specific record"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Recalculation of rollup fields started for record",
            "job_id": "job456",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        rollup_service = ObjectRollupService(client)

        # Call method to test for specific record
        result = rollup_service.recalculate_rollup_fields("product__v", "12345")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/12345/actions/rolluprecalculate"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["data"] in (None, "{}")  # Empty data or None

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job456"

    @patch("requests.request")
    def test_recalculate_specific_rollup_fields(self, mock_request):
        """Test recalculate_rollup_fields method for specific fields"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Recalculation of specified rollup fields started",
            "job_id": "job789",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        rollup_service = ObjectRollupService(client)

        # Call method to test with specific fields
        result = rollup_service.recalculate_rollup_fields(
            "product__v",
            record_id="12345",
            fields=["total_quantity__c", "avg_price__c"],
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/12345/actions/rolluprecalculate"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Check data contains the fields
        data = json.loads(kwargs["data"])
        assert "fields" in data
        assert data["fields"] == ["total_quantity__c", "avg_price__c"]

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job789"

    @patch("requests.request")
    def test_retrieve_rollup_status(self, mock_request):
        """Test retrieve_rollup_field_recalculation_status method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job": {
                "id": "job123",
                "status": "RUNNING",
                "start_date": "2023-01-01T12:00:00.000Z",
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
        rollup_service = ObjectRollupService(client)

        # Call method to test for object-level status
        result = rollup_service.retrieve_rollup_field_recalculation_status("product__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/actions/recalculaterollups"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job"]["status"] == "RUNNING"
        assert result["job"]["id"] == "job123"

    @patch("requests.request")
    def test_retrieve_rollup_status_by_job_id(self, mock_request):
        """Test retrieve_rollup_field_recalculation_status method with job ID"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job": {
                "id": "job123",
                "status": "COMPLETE",
                "start_date": "2023-01-01T12:00:00.000Z",
                "completion_date": "2023-01-01T12:05:00.000Z",
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
        rollup_service = ObjectRollupService(client)

        # Call method to test with specific job ID
        result = rollup_service.retrieve_rollup_field_recalculation_status(
            "product__v", job_id="job123"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/actions/rolluprecalculate/job123"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job"]["status"] == "COMPLETE"
        assert result["job"]["id"] == "job123"


@mark.integration
@mark.veevavault
class TestObjectRollupServiceIntegration:
    """
    Integration tests for ObjectRollupService using real API calls
    """

    def test_retrieve_rollup_status(self, authenticated_vault_client, vault_config):
        """Test retrieving rollup status with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        rollup_service = ObjectRollupService(authenticated_vault_client)

        # Skip actual API call in this template
        pytest.skip("Integration test requires an object with rollup fields")
