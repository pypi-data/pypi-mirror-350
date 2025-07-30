from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.objects import ObjectService
from veevavault.services.objects.crud_service import ObjectCRUDService


@mark.unit
@mark.veevavault
class TestObjectCRUDServiceUnit:
    """
    Unit tests for ObjectCRUDService using mocks
    """

    @patch("requests.request")
    def test_retrieve_object_record(self, mock_request):
        """Test retrieve_object_record method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "object": {
                "name": "test_object__v",
                "id": "123",
                "properties": {
                    "name__v": "Test Object",
                    "status__v": "active__v",
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
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.retrieve_object_record("test_object__v", "123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v/123")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["object"]["name"] == "test_object__v"
        assert result["object"]["id"] == "123"

    @patch("requests.request")
    def test_retrieve_deleted_object_record_id(self, mock_request):
        """Test retrieve_deleted_object_record_id method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "deletions": [
                {
                    "id": "123",
                    "name__v": "Test Object",
                    "deletion_date__v": "2023-01-01T12:00:00.000Z",
                }
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
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.retrieve_deleted_object_record_id(
            "test_object__v", "token123"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v/deleted")
        assert kwargs["method"] == "GET"
        assert kwargs["params"] == {"idtoken": "token123"}

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["deletions"][0]["id"] == "123"

    @patch("requests.request")
    def test_create_object_records(self, mock_request):
        """Test create_object_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "123", "responseStatus": "SUCCESS"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        crud_service = ObjectCRUDService(client)

        # Test data
        test_data = {"name__v": "Test Object", "status__v": "active__v"}

        # Call method to test
        result = crud_service.create_object_records(
            "test_object__v", test_data, content_type="application/json"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "text/csv"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_update_object_records(self, mock_request):
        """Test update_object_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "123", "responseStatus": "SUCCESS"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        crud_service = ObjectCRUDService(client)

        # Test data
        test_data = {"id": "123", "status__v": "approved__v"}

        # Call method to test
        result = crud_service.update_object_records("test_object__v", test_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_delete_object_records(self, mock_request):
        """Test delete_object_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "123", "responseStatus": "SUCCESS"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        crud_service = ObjectCRUDService(client)

        # Test data
        test_data = {"id": "123"}

        # Call method to test
        result = crud_service.delete_object_records("test_object__v", test_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_cascade_delete_object_record(self, mock_request):
        """Test cascade_delete_object_record method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "links": [
                {
                    "rel": "results",
                    "href": "/api/v25.1/vobjects/cascadedelete/results/test_object__v/success/job123",
                }
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
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.cascade_delete_object_record("test_object__v", "123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/test_object__v/123/actions/cascadedelete"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_retrieve_cascade_delete_results(self, mock_request):
        """Test retrieve_cascade_delete_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "status": "success",
            "source_record": {"id": "123", "object": "test_object__v"},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.retrieve_cascade_delete_results(
            "test_object__v", "success", "job123"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/cascadedelete/results/test_object__v/success/job123"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"
        assert result["status"] == "success"

    @patch("requests.request")
    def test_deep_copy_object_record(self, mock_request):
        """Test deep_copy_object_record method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job456",
            "links": [
                {
                    "rel": "results",
                    "href": "/api/v25.1/vobjects/deepcopy/results/test_object__v/success/job456",
                }
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
        crud_service = ObjectCRUDService(client)

        # Test payload
        test_payload = {"name__v": "Copy of Test Object"}

        # Call method to test
        result = crud_service.deep_copy_object_record(
            "test_object__v", "123", test_payload
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/test_object__v/123/actions/deepcopy"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job456"

    @patch("requests.request")
    def test_retrieve_deep_copy_results(self, mock_request):
        """Test retrieve_deep_copy_results method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job456",
            "status": "success",
            "source_record": {"id": "123", "object": "test_object__v"},
            "target_record": {"id": "789", "object": "test_object__v"},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.retrieve_deep_copy_results(
            "test_object__v", "success", "job456"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/deepcopy/results/test_object__v/success/job456"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job456"
        assert result["status"] == "success"

    @patch("requests.request")
    def test_update_corporate_currency_fields(self, mock_request):
        """Test update_corporate_currency_fields method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
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
        crud_service = ObjectCRUDService(client)

        # Call method to test
        result = crud_service.update_corporate_currency_fields("test_object__v", "123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/test_object__v/123/actions/corporatecurrencyupdate"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job789"


@mark.integration
@mark.veevavault
class TestObjectCRUDServiceIntegration:
    """
    Integration tests for ObjectCRUDService using real API calls
    """

    def test_retrieve_object_record(self, authenticated_vault_client, vault_config):
        """Test retrieving an object record with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        crud_service = ObjectCRUDService(authenticated_vault_client)

        # This would normally use a known record ID in your environment
        # For safety, we'll skip the actual API call in this template
        pytest.skip("Integration test requires a valid object record ID")
