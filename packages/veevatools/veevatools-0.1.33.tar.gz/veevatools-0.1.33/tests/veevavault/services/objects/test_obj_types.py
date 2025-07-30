from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.types_service import ObjectTypesService


@mark.unit
@mark.veevavault
class TestObjectTypesServiceUnit:
    """
    Unit tests for ObjectTypesService
    """

    @patch("requests.request")
    def test_retrieve_details_from_all_object_types(self, mock_request):
        """Test retrieve_details_from_all_object_types method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "objects": [
                {
                    "name": "customer__c",
                    "label": "Customer",
                    "types": [
                        {"name": "individual__c", "label": "Individual"},
                        {"name": "organization__c", "label": "Organization"},
                    ],
                },
                {
                    "name": "product__v",
                    "label": "Product",
                    "types": [
                        {"name": "device__c", "label": "Device"},
                        {"name": "drug__c", "label": "Drug"},
                    ],
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
        types_service = ObjectTypesService(client)

        # Call method to test
        result = types_service.retrieve_details_from_all_object_types()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/configuration/Objecttype")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["objects"]) == 2
        assert result["objects"][0]["name"] == "customer__c"
        assert len(result["objects"][0]["types"]) == 2
        assert result["objects"][1]["name"] == "product__v"

    @patch("requests.request")
    def test_retrieve_details_from_specific_object(self, mock_request):
        """Test retrieve_details_from_specific_object method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "object": {
                "name": "product__v",
                "label": "Product",
                "type": "drug__c",
                "type_label": "Drug",
                "fields": [
                    {"name": "name__v", "label": "Name", "type": "string"},
                    {
                        "name": "active_ingredient__c",
                        "label": "Active Ingredient",
                        "type": "string",
                    },
                    {"name": "dosage__c", "label": "Dosage", "type": "picklist"},
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
        types_service = ObjectTypesService(client)

        # Call method to test
        result = types_service.retrieve_details_from_specific_object(
            "Objecttype.product__v.drug__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/configuration/Objecttype.product__v.drug__c"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["object"]["name"] == "product__v"
        assert result["object"]["type"] == "drug__c"
        assert len(result["object"]["fields"]) == 3

    @patch("requests.request")
    def test_change_object_type(self, mock_request):
        """Test change_object_type method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "12345", "responseStatus": "SUCCESS"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        types_service = ObjectTypesService(client)

        # Test payload
        payload = {"records": [{"id": "12345", "object_type__v": "drug__c"}]}

        # Call method to test
        result = types_service.change_object_type("product__v", payload)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/actions/changetype"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert json.loads(kwargs["data"]) == payload

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "12345"


@mark.integration
@mark.veevavault
class TestObjectTypesServiceIntegration:
    """
    Integration tests for ObjectTypesService using real API calls
    """

    def test_retrieve_all_object_types(self, authenticated_vault_client, vault_config):
        """Test retrieving all object types with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        types_service = ObjectTypesService(authenticated_vault_client)

        # This test can usually be run safely since it just lists object types
        result = types_service.retrieve_details_from_all_object_types()

        # Basic validations
        assert result["responseStatus"] == "SUCCESS"
        assert "objects" in result
