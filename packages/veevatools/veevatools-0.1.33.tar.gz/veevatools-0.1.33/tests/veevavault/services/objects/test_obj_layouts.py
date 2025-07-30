from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.layouts_service import ObjectLayoutsService


@mark.unit
@mark.veevavault
class TestObjectLayoutsServiceUnit:
    """
    Unit tests for ObjectLayoutsService
    """

    @patch("requests.request")
    def test_retrieve_page_layouts(self, mock_request):
        """Test retrieve_page_layouts method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "layouts": [
                {
                    "name": "standard_layout__c",
                    "label": "Standard Layout",
                    "object_type": None,
                    "default_layout": True,
                    "active": True,
                    "description": "Standard page layout for all object types",
                },
                {
                    "name": "drug_layout__c",
                    "label": "Drug Layout",
                    "object_type": "drug__c",
                    "default_layout": False,
                    "active": True,
                    "description": "Layout for drug products",
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
        layouts_service = ObjectLayoutsService(client)

        # Call method to test
        result = layouts_service.retrieve_page_layouts("product__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/configuration/objects/product__v/pagelayouts"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["layouts"]) == 2
        assert result["layouts"][0]["name"] == "standard_layout__c"
        assert result["layouts"][0]["default_layout"] == True
        assert result["layouts"][1]["name"] == "drug_layout__c"
        assert result["layouts"][1]["object_type"] == "drug__c"

    @patch("requests.request")
    def test_retrieve_page_layout_metadata(self, mock_request):
        """Test retrieve_page_layout_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "layout": {
                "name": "drug_layout__c",
                "label": "Drug Layout",
                "object_type": "drug__c",
                "default_layout": False,
                "active": True,
                "description": "Layout for drug products",
                "sections": [
                    {
                        "name": "general_section__c",
                        "label": "General Information",
                        "fields": [
                            {"name": "name__v", "editable": True, "required": True},
                            {"name": "dosage__c", "editable": True, "required": False},
                        ],
                    },
                    {
                        "name": "regulatory_section__c",
                        "label": "Regulatory Information",
                        "fields": [
                            {
                                "name": "approval_date__c",
                                "editable": True,
                                "required": False,
                            }
                        ],
                    },
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
        layouts_service = ObjectLayoutsService(client)

        # Call method to test
        result = layouts_service.retrieve_page_layout_metadata(
            "product__v", "drug_layout__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/configuration/objects/product__v/pagelayouts/drug_layout__c"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["layout"]["name"] == "drug_layout__c"
        assert len(result["layout"]["sections"]) == 2
        assert len(result["layout"]["sections"][0]["fields"]) == 2
        assert result["layout"]["sections"][0]["fields"][0]["name"] == "name__v"
        assert result["layout"]["sections"][0]["fields"][0]["required"] == True


@mark.integration
@mark.veevavault
class TestObjectLayoutsServiceIntegration:
    """
    Integration tests for ObjectLayoutsService using real API calls
    """

    def test_retrieve_page_layouts(self, authenticated_vault_client, vault_config):
        """Test retrieving page layouts with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        layouts_service = ObjectLayoutsService(authenticated_vault_client)

        # Skip actual API call in this template
        pytest.skip("Integration test requires a valid object type in your environment")
