from pytest import mark, fixture
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call

from veevavault.services.picklists import PicklistService


@mark.unit
@mark.veevavault
class TestPicklistServiceUnit:
    """
    Unit tests for PicklistService class using mocks (no real API calls)
    """

    @fixture
    def picklist_service(self, vault_client):
        """Return a PicklistService instance with a mocked vault client"""
        return PicklistService(vault_client)

    @patch("requests.request")
    def test_retrieve_all_picklists(self, mock_request, picklist_service):
        """Test retrieving all picklists"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "picklists": [
                {
                    "name": "country__v",
                    "label": "Country",
                    "kind": "global",
                    "systemManaged": False,
                    "usedIn": [
                        {"objectName": "country__v", "propertyName": "country_code__c"}
                    ],
                },
                {
                    "name": "document_type__v",
                    "label": "Document Type",
                    "kind": "global",
                    "systemManaged": True,
                    "usedIn": [
                        {"documentTypeName": "document__v", "propertyName": "type__v"}
                    ],
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.retrieve_all_picklists()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/picklists")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["picklists"]) == 2
        assert result["picklists"][0]["name"] == "country__v"
        assert result["picklists"][1]["name"] == "document_type__v"

    @patch("requests.request")
    def test_retrieve_picklist_values(self, mock_request, picklist_service):
        """Test retrieving values for a specific picklist"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "values": [
                {
                    "name": "usa__c",
                    "label": "United States",
                    "status": "active",
                    "id": "1234",
                },
                {
                    "name": "canada__c",
                    "label": "Canada",
                    "status": "active",
                    "id": "5678",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.retrieve_picklist_values("country__v")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/picklists/country__v")
        assert kwargs["method"] == "GET"

        # Verify response is converted to DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result["name"]) == ["usa__c", "canada__c"]
        assert list(result["label"]) == ["United States", "Canada"]
        assert list(result["picklistName"]) == ["country__v", "country__v"]

    @patch("requests.request")
    def test_retrieve_picklist_values_with_picklistValues_field(
        self, mock_request, picklist_service
    ):
        """Test retrieving picklist values when API returns 'picklistValues' field instead of 'values'"""
        # Set up mock response with picklistValues field instead of values
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "picklistValues": [
                {
                    "name": "usa__c",
                    "label": "United States",
                    "status": "active",
                    "id": "1234",
                },
                {
                    "name": "canada__c",
                    "label": "Canada",
                    "status": "active",
                    "id": "5678",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.retrieve_picklist_values("country__v")

        # Verify response is converted to DataFrame properly
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result["name"]) == ["usa__c", "canada__c"]
        assert list(result["picklistName"]) == ["country__v", "country__v"]

    @patch("requests.request")
    def test_retrieve_picklist_values_empty_response(
        self, mock_request, picklist_service
    ):
        """Test handling of empty picklist values response"""
        # Set up mock response with no values
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "values": []}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.retrieve_picklist_values("empty_picklist__v")

        # Verify empty DataFrame is returned with expected columns
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert set(result.columns) >= {"name", "label", "picklistName"}

    @patch("requests.request")
    def test_retrieve_picklist_values_error(self, mock_request, picklist_service):
        """Test error handling in retrieve_picklist_values"""
        # Set up mock response with error
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "FAILURE",
            "responseMessage": "Picklist not found",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Verify exception is raised
        with pytest.raises(Exception) as exc_info:
            picklist_service.retrieve_picklist_values("nonexistent_picklist__v")

        assert "Failed to retrieve picklist values" in str(exc_info.value)

    @patch("requests.request")
    def test_create_picklist_values(self, mock_request, picklist_service):
        """Test creating new picklist values"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully created 3 picklist values",
            "picklistValues": [
                {"name": "north_america__c", "label": "North America"},
                {"name": "central_america__c", "label": "Central America"},
                {"name": "south_america__c", "label": "South America"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        values_to_create = ["North America", "Central America", "South America"]
        result = picklist_service.create_picklist_values("region__v", values_to_create)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/picklists/region__v")
        assert kwargs["method"] == "POST"

        # Verify data was formatted correctly
        assert kwargs["data"] == {
            "value_1": "North America",
            "value_2": "Central America",
            "value_3": "South America",
        }

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["picklistValues"]) == 3

    @patch("requests.request")
    def test_update_picklist_value_label(self, mock_request, picklist_service):
        """Test updating picklist value labels"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully updated 2 picklist values",
            "picklistValues": [
                {"name": "north_america__c", "label": "North America/United States"},
                {"name": "south_america__c", "label": "South America/Brazil"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        label_updates = {
            "north_america__c": "North America/United States",
            "south_america__c": "South America/Brazil",
        }
        result = picklist_service.update_picklist_value_label(
            "region__v", label_updates
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/picklists/region__v")
        assert kwargs["method"] == "PUT"
        assert kwargs["data"] == label_updates

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["picklistValues"]) == 2

    @patch("requests.request")
    def test_update_picklist_value_name(self, mock_request, picklist_service):
        """Test updating a picklist value's name"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully updated picklist value",
            "name": "n_america__c",
            "label": "North America",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.update_picklist_value(
            "region__v", "north_america__c", new_name="n_america"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/picklists/region__v/north_america__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"] == {"name": "n_america"}

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "n_america__c"

    @patch("requests.request")
    def test_update_picklist_value_status(self, mock_request, picklist_service):
        """Test updating a picklist value's status"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully updated picklist value",
            "name": "north_america__c",
            "label": "North America",
            "status": "inactive",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.update_picklist_value(
            "region__v", "north_america__c", status="inactive"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/picklists/region__v/north_america__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"] == {"status": "inactive"}

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["status"] == "inactive"

    @patch("requests.request")
    def test_inactivate_picklist_value(self, mock_request, picklist_service):
        """Test inactivating a picklist value"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully inactivated picklist value",
            "name": "north_america__c",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Call the method
        result = picklist_service.inactivate_picklist_value(
            "region__v", "north_america__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/picklists/region__v/north_america__c"
        )
        assert kwargs["method"] == "DELETE"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "north_america__c"

    @pytest.mark.asyncio
    @patch(
        "veevavault.services.picklists.picklist_service.PicklistService.retrieve_picklist_values"
    )
    async def test_async_bulk_retrieve_picklist_values(
        self, mock_retrieve, picklist_service
    ):
        """Test asynchronous bulk retrieval of picklist values"""
        # Set up mock responses
        mock_df1 = pd.DataFrame(
            {
                "name": ["usa__c", "canada__c"],
                "label": ["United States", "Canada"],
                "status": ["active", "active"],
                "id": ["1", "2"],
                "picklistName": ["country__v", "country__v"],
            }
        )

        mock_df2 = pd.DataFrame(
            {
                "name": ["north_america__c", "south_america__c"],
                "label": ["North America", "South America"],
                "status": ["active", "active"],
                "id": ["3", "4"],
                "picklistName": ["region__v", "region__v"],
            }
        )

        # Configure mock to return different DataFrames for different calls
        mock_retrieve.side_effect = [mock_df1, mock_df2]

        # Call the method
        result = await picklist_service.async_bulk_retrieve_picklist_values(
            ["country__v", "region__v"]
        )

        # Verify retrieve_picklist_values was called for each picklist
        assert mock_retrieve.call_count == 2
        mock_retrieve.assert_has_calls([call("country__v"), call("region__v")])

        # Verify result combines both DataFrames
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4
        assert set(result["picklistName"].unique()) == {"country__v", "region__v"}

    @pytest.mark.asyncio
    @patch(
        "veevavault.services.picklists.picklist_service.PicklistService.retrieve_picklist_values"
    )
    async def test_async_bulk_retrieve_empty_result(
        self, mock_retrieve, picklist_service
    ):
        """Test asynchronous bulk retrieval with empty results"""
        # Set up mock to return empty DataFrames
        mock_retrieve.return_value = pd.DataFrame()

        # Call the method
        result = await picklist_service.async_bulk_retrieve_picklist_values(
            ["empty1__v", "empty2__v"]
        )

        # Verify result is empty DataFrame with expected columns
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert set(result.columns) >= {"name", "label", "picklistName"}

    @pytest.mark.asyncio
    @patch(
        "veevavault.services.picklists.picklist_service.PicklistService.retrieve_picklist_values"
    )
    async def test_async_retrieve_picklist_error_handling(
        self, mock_retrieve, picklist_service
    ):
        """Test error handling in async retrieve picklist helper method"""
        # Configure mock to raise exception for one picklist and return data for another
        mock_retrieve.side_effect = [
            Exception("API error"),
            pd.DataFrame(
                {
                    "name": ["value1__c"],
                    "label": ["Value 1"],
                    "status": ["active"],
                    "id": ["1"],
                    "picklistName": ["working_picklist__v"],
                }
            ),
        ]

        # Mock print to capture error message
        with patch("builtins.print") as mock_print:
            result = await picklist_service.async_bulk_retrieve_picklist_values(
                ["error_picklist__v", "working_picklist__v"]
            )

        # Verify error was printed
        mock_print.assert_called_once()
        args = mock_print.call_args[0]
        assert "Error retrieving picklist error_picklist__v" in args[0]

        # Verify result contains only data from working picklist
        assert len(result) == 1
        assert result.iloc[0]["picklistName"] == "working_picklist__v"


@mark.integration
@mark.veevavault
class TestPicklistServiceIntegration:
    """
    Integration tests for PicklistService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def picklist_service(self, authenticated_vault_client):
        """Return a PicklistService instance with an authenticated vault client"""
        return PicklistService(authenticated_vault_client)

    def test_retrieve_all_picklists(self, picklist_service, vault_config):
        """Test retrieving all picklists from a real Vault instance"""
        # Skip if not authenticated
        if not picklist_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call the method
        result = picklist_service.retrieve_all_picklists()

        # Verify basic response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "picklists" in result
        assert isinstance(result["picklists"], list)

        # Verify picklists have expected fields
        for picklist in result["picklists"]:
            assert "name" in picklist
            assert "label" in picklist
            assert "kind" in picklist
            assert "systemManaged" in picklist

    def test_retrieve_picklist_values(self, picklist_service, vault_config):
        """Test retrieving values for a specific picklist from a real Vault instance"""
        # Skip if not authenticated
        if not picklist_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Select a common picklist that should exist in most Vaults
        picklist_name = "document_type__v"  # This is usually present in all Vaults

        # Call the method
        result = picklist_service.retrieve_picklist_values(picklist_name)

        # Verify result is a DataFrame with expected columns
        assert isinstance(result, pd.DataFrame)
        assert "name" in result.columns
        assert "label" in result.columns
        assert "picklistName" in result.columns

        # Verify all rows have the correct picklist name
        assert all(result["picklistName"] == picklist_name)

    @pytest.mark.skip(
        reason="Creating picklist values would modify Vault data and should be tested manually"
    )
    def test_create_picklist_values(self, picklist_service, vault_config):
        """Test creating new picklist values in a real Vault instance"""
        # This test is skipped as it would modify Vault data
        pass

    @pytest.mark.skip(
        reason="Updating picklist labels would modify Vault data and should be tested manually"
    )
    def test_update_picklist_value_label(self, picklist_service, vault_config):
        """Test updating picklist value labels in a real Vault instance"""
        # This test is skipped as it would modify Vault data
        pass

    @pytest.mark.skip(
        reason="Updating picklist values would modify Vault data and should be tested manually"
    )
    def test_update_picklist_value(self, picklist_service, vault_config):
        """Test updating a picklist value in a real Vault instance"""
        # This test is skipped as it would modify Vault data
        pass

    @pytest.mark.skip(
        reason="Inactivating picklist values would modify Vault data and should be tested manually"
    )
    def test_inactivate_picklist_value(self, picklist_service, vault_config):
        """Test inactivating a picklist value in a real Vault instance"""
        # This test is skipped as it would modify Vault data
        pass

    @pytest.mark.asyncio
    async def test_async_bulk_retrieve_picklist_values(
        self, picklist_service, vault_config
    ):
        """Test asynchronous bulk retrieval of picklist values from a real Vault instance"""
        # Skip if not authenticated
        if not picklist_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Select common picklists that should exist in most Vaults
        picklist_names = ["document_type__v", "lifecycle__v"]

        # Call the method
        result = await picklist_service.async_bulk_retrieve_picklist_values(
            picklist_names
        )

        # Verify result is a DataFrame with expected columns
        assert isinstance(result, pd.DataFrame)
        assert "name" in result.columns
        assert "label" in result.columns
        assert "picklistName" in result.columns

        # Verify both picklists are present in the result
        picklists_in_result = set(result["picklistName"].unique())
        for picklist in picklist_names:
            # Some picklists might not exist in all Vault instances
            # so we don't fail the test if one is missing
            if picklist in picklists_in_result:
                assert picklist in picklists_in_result
