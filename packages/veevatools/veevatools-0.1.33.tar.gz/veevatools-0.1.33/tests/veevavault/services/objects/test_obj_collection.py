from pytest import mark, fixture
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.collection_service import ObjectCollectionService


@mark.unit
@mark.veevavault
class TestObjectCollectionServiceUnit:
    """
    Unit tests for ObjectCollectionService
    """

    @patch("requests.request")
    def test_retrieve_object_record_collection(self, mock_request):
        """Test retrieve_object_record_collection method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseDetails": {"limit": 50, "offset": 0, "size": 2, "total": 2},
            "data": [
                {"id": "001", "name__v": "Test Object 1"},
                {"id": "002", "name__v": "Test Object 2"},
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
        collection_service = ObjectCollectionService(client)

        # Call method to test with parameters
        result = collection_service.retrieve_object_record_collection(
            "test_object__v",
            fields=["id", "name__v", "status__v"],
            limit=50,
            offset=0,
            sort="name__v:asc",
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/test_object__v")
        assert kwargs["method"] == "GET"
        assert kwargs["params"]["fields"] == "id,name__v,status__v"
        assert kwargs["params"]["limit"] == 50
        assert kwargs["params"]["offset"] == 0
        assert kwargs["params"]["sort"] == "name__v:asc"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == "001"
        assert result["data"][1]["name__v"] == "Test Object 2"

    @patch("requests.request")
    def test_retrieve_object_record_collection_as_dataframe(self, mock_request):
        """Test retrieve_object_record_collection_as_dataframe method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseDetails": {"limit": 50, "offset": 0, "size": 2, "total": 2},
            "data": [
                {"id": "001", "name__v": "Test Object 1"},
                {"id": "002", "name__v": "Test Object 2"},
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
        collection_service = ObjectCollectionService(client)

        # Call method to test
        result = collection_service.retrieve_object_record_collection_as_dataframe(
            "test_object__v", fields=["id", "name__v"]
        )

        # Verify it returned a DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["id", "name__v"]
        assert result.iloc[0]["id"] == "001"
        assert result.iloc[1]["name__v"] == "Test Object 2"


@mark.integration
@mark.veevavault
class TestObjectCollectionServiceIntegration:
    """
    Integration tests for ObjectCollectionService using real API calls
    """

    def test_retrieve_object_record_collection(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving object records with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        collection_service = ObjectCollectionService(authenticated_vault_client)

        # For safety in this template, we'll skip the actual API call
        pytest.skip("Integration test requires a valid object type in your environment")
