from pytest import mark, fixture
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.metadata_service import ObjectMetadataService


@mark.unit
@mark.veevavault
class TestObjectMetadataServiceUnit:
    """
    Unit tests for ObjectMetadataService
    """

    @patch("requests.request")
    def test_retrieve_object_metadata(self, mock_request):
        """Test retrieve_object_metadata method"""
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
                "urls": {
                    "fields": "/api/v25.1/metadata/vobjects/test_object__v/fields"
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test
        result = metadata_service.retrieve_object_metadata("test_object__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/vobjects/test_object__v")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert kwargs["params"] == {}  # No loc parameter

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["object"]["name"] == "test_object__v"
        assert result["object"]["label"] == "Test Object"
        assert "name__v" in result["object"]["properties"]

    @patch("requests.request")
    def test_retrieve_object_metadata_with_loc(self, mock_request):
        """Test retrieve_object_metadata method with localization"""
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
                "urls": {
                    "fields": "/api/v25.1/metadata/vobjects/test_object__v/fields"
                },
                "localization": {"label": {"en": "Test Object", "fr": "Objet de Test"}},
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test with loc=True
        result = metadata_service.retrieve_object_metadata("test_object__v", loc=True)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/vobjects/test_object__v")
        assert kwargs["method"] == "GET"
        assert kwargs["params"] == {"loc": "true"}

        # Verify response parsing with localization
        assert result["responseStatus"] == "SUCCESS"
        assert "localization" in result["object"]
        assert result["object"]["localization"]["label"]["fr"] == "Objet de Test"

    @patch("requests.request")
    def test_retrieve_object_field_metadata(self, mock_request):
        """Test retrieve_object_field_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "field": {
                "name": "status__v",
                "label": "Status",
                "type": "picklist",
                "required": True,
                "editable": True,
                "picklist_values": [
                    {"name": "active__v", "label": "Active"},
                    {"name": "inactive__v", "label": "Inactive"},
                ],
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test
        result = metadata_service.retrieve_object_field_metadata(
            "test_object__v", "status__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/metadata/vobjects/test_object__v/fields/status__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["field"]["name"] == "status__v"
        assert result["field"]["type"] == "picklist"
        assert len(result["field"]["picklist_values"]) == 2

    @patch("requests.request")
    def test_retrieve_object_collection(self, mock_request):
        """Test retrieve_object_collection method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "objects": [
                {
                    "name": "test_object__v",
                    "label": "Test Object",
                    "url": "/api/v25.1/metadata/vobjects/test_object__v",
                },
                {
                    "name": "product__v",
                    "label": "Product",
                    "url": "/api/v25.1/metadata/vobjects/product__v",
                },
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test
        result = metadata_service.retrieve_object_collection()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/vobjects")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["objects"]) == 2
        assert result["objects"][0]["name"] == "test_object__v"

    @patch("requests.request")
    def test_describe_objects(self, mock_request):
        """Test describe_objects method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "objects": [
                {"name": "test_object__v", "label": "Test Object"},
                {"name": "product__v", "label": "Product"},
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test
        result = metadata_service.describe_objects()

        # Verify it returns a DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["name", "label"]
        assert result.iloc[0]["name"] == "test_object__v"

    @patch("requests.request")
    def test_retrieve_limits_on_objects(self, mock_request):
        """Test retrieve_limits_on_objects method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "limits": {
                "records_per_object": 1000000,
                "custom_objects": {"max": 50, "remaining": 30},
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
        metadata_service = ObjectMetadataService(client)

        # Call method to test
        result = metadata_service.retrieve_limits_on_objects()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/vobjects/limits")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["limits"]["records_per_object"] == 1000000
        assert result["limits"]["custom_objects"]["max"] == 50


@mark.integration
@mark.veevavault
class TestObjectMetadataServiceIntegration:
    """
    Integration tests for ObjectMetadataService using real API calls
    """

    def test_retrieve_object_collection(self, authenticated_vault_client, vault_config):
        """Test retrieving object collection with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        metadata_service = ObjectMetadataService(authenticated_vault_client)

        # This test can usually be run safely since it just lists objects
        result = metadata_service.retrieve_object_collection()

        # Basic validations
        assert result["responseStatus"] == "SUCCESS"
        assert "objects" in result
        assert isinstance(result["objects"], list)
