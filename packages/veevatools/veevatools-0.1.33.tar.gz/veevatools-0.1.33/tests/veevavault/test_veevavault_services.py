from pytest import mark, fixture
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
class TestVaultServicesUnit:
    """
    Unit tests for various VeevaVault service classes using mocks
    """

    @patch("requests.request")
    def test_document_service_retrieve(self, mock_request):
        """Test DocumentService retrieval_service.retrieve_document method"""
        from veevavault.services.documents import DocumentService

        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "document": {
                "id": "123",
                "name": "Test Document",
                "type": "test_doc_type__v",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Create service with mocked client
        doc_service = DocumentService(client)

        # Call method to test - note the service structure where retrieve_document is in the retrieval sub-service
        result = doc_service.retrieval.retrieve_document("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["document"]["id"] == "123"
        assert result["document"]["name"] == "Test Document"

    @patch("requests.post")
    def test_query_service_query(self, mock_post):
        """Test QueryService query method"""
        from veevavault.services.queries import QueryService

        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            # Put data at the top level as expected by the query method
            "data": [
                {"id": "001", "name": "Object 1"},
                {"id": "002", "name": "Object 2"},
            ],
            "responseDetails": {"total": 2, "offset": 0, "pageSize": 2},
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test - use query method instead of execute_query
        result = query_service.query("SELECT id, name FROM object__v")

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://test.veevavault.com/api/v25.1/query"
        assert "q" in kwargs["data"]
        assert kwargs["data"]["q"] == "SELECT id, name FROM object__v"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == "001"

    @patch("requests.request")
    def test_object_service_retrieve(self, mock_request):
        """Test ObjectService retrieve_object_record method"""
        from veevavault.services.objects import ObjectService

        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "object": {
                "name": "test_object__v",
                "label": "Test Object",
                "properties": {
                    "name__v": {"type": "string", "required": True},
                    "status__v": {"type": "picklist", "required": True},
                },
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"

        # Create service with mocked client
        object_service = ObjectService(client)

        # Call method to test - use retrieve_object_record instead of retrieve_object
        result = object_service.retrieve_object_record("test_object__v", "123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v/123")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["object"]["name"] == "test_object__v"
        assert result["object"]["label"] == "Test Object"
        assert "name__v" in result["object"]["properties"]


@mark.integration
@mark.veevavault
class TestVaultServicesIntegration:
    """
    Integration tests for VeevaVault service classes using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_document_service(self, authenticated_vault_client, vault_config):
        """Test basic document service methods with real API"""
        from veevavault.services.documents import DocumentService
        from veevavault.services.documents.types_service import DocumentTypesService

        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        doc_service = DocumentService(authenticated_vault_client)

    def test_query_service(self, authenticated_vault_client, vault_config):
        """Test query service with real API"""
        from veevavault.services.queries import QueryService

        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        query_service = QueryService(authenticated_vault_client)

        # Execute a safe query - using query method instead of execute_query
        result = query_service.query(
            "SELECT id, name__v FROM vault_package__v LIMIT 10"
        )

        # Verify response structure - only check what's actually in the response
        assert result["responseStatus"] == "SUCCESS"
        # The response now has data at the top level instead of under queryResponse
        assert "data" in result
        assert isinstance(result["data"], list)
