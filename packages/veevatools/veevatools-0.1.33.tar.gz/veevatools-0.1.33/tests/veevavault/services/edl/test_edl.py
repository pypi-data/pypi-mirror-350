from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.edl import EDLService


@mark.unit
@mark.veevavault
class TestEDLServiceUnit:
    """
    Unit tests for EDLService class using mocks (no real API calls)
    """

    @fixture
    def edl_service(self):
        """Returns a EDLService with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return EDLService(client)

    def test_create_placeholder_from_edl_item_list(self, edl_service):
        """Test create_placeholder_from_edl_item with a list of IDs"""
        # Mock the client's api_call method
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": 84201,
            "url": "/api/v25.1/services/jobs/84201",
        }

        # Call the method with a list of IDs
        result = edl_service.create_placeholder_from_edl_item(["EDL001", "EDL002"])

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert args[0] == "api/v25.1/vobjects/edl_item__v/actions/createplaceholder"
        assert kwargs["method"] == "POST"
        assert kwargs["headers"] == {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        assert kwargs["data"] == {"edlItemIds": "EDL001, EDL002"}

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == 84201

    def test_create_placeholder_from_edl_item_string(self, edl_service):
        """Test create_placeholder_from_edl_item with a string of IDs"""
        # Mock the client's api_call method
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": 84201,
            "url": "/api/v25.1/services/jobs/84201",
        }

        # Call the method with a string of IDs
        result = edl_service.create_placeholder_from_edl_item("EDL001, EDL002")

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert args[0] == "api/v25.1/vobjects/edl_item__v/actions/createplaceholder"
        assert kwargs["method"] == "POST"
        assert kwargs["headers"] == {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        assert kwargs["data"] == {"edlItemIds": "EDL001, EDL002"}

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == 84201

    def test_retrieve_all_root_nodes_default(self, edl_service):
        """Test retrieve_all_root_nodes with default hierarchy"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": "0000000000000JIT",
                    "order__v": 1,
                    "ref_type__v": "edl__v",
                    "ref_name__v": "NewEDL",
                    "url": "/vobjects/edl__v/0EL000000001901",
                    "ref_id__v": "0EL000000001901",
                    "parent_id__v": None,
                }
            ],
        }

        # Call the method with default hierarchy
        result = edl_service.retrieve_all_root_nodes()

        # Verify the API call
        edl_service.client.api_call.assert_called_once_with(
            "api/v25.1/composites/trees/edl_hierarchy__v"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "0000000000000JIT"
        assert result["data"][0]["ref_type__v"] == "edl__v"

    def test_retrieve_all_root_nodes_template(self, edl_service):
        """Test retrieve_all_root_nodes with template hierarchy"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": "0000000000000JIT",
                    "order__v": 1,
                    "ref_type__v": "edl_template__v",
                    "ref_name__v": "Template EDL",
                    "url": "/vobjects/edl_template__v/0EL000000001901",
                    "ref_id__v": "0EL000000001901",
                    "parent_id__v": None,
                }
            ],
        }

        # Call the method with template hierarchy
        result = edl_service.retrieve_all_root_nodes("edl_template__v")

        # Verify the API call
        edl_service.client.api_call.assert_called_once_with(
            "api/v25.1/composites/trees/edl_template__v"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["ref_type__v"] == "edl_template__v"

    def test_retrieve_specific_root_nodes(self, edl_service):
        """Test retrieve_specific_root_nodes"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "id": "0000000000000IR1",
                    "ref_id__v": "0EL000000000401",
                }
            ],
        }

        # Call the method
        result = edl_service.retrieve_specific_root_nodes(["0EL000000000401"])

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert (
            args[0] == "api/v25.1/composites/trees/edl_hierarchy__v/actions/listnodes"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == [{"ref_id__v": "0EL000000000401"}]

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "0000000000000IR1"

    def test_retrieve_node_children(self, edl_service):
        """Test retrieve_node_children"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": "0000000000000JLL",
                    "order__v": 1,
                    "ref_type__v": "edl_item__v",
                    "ref_name__v": "NewEDL Child",
                    "url": "/vobjects/edl_item__v/0EI000000009401",
                    "ref_id__v": "0EI000000009401",
                    "parent_id__v": "0000000000000JIT",
                }
            ],
        }

        # Call the method
        result = edl_service.retrieve_node_children("0000000000000JIT")

        # Verify the API call
        edl_service.client.api_call.assert_called_once_with(
            "api/v25.1/composites/trees/edl_hierarchy__v/0000000000000JIT/children"
        )

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "0000000000000JLL"
        assert result["data"][0]["parent_id__v"] == "0000000000000JIT"

    def test_update_node_order(self, edl_service):
        """Test update_node_order"""
        # Mock response
        edl_service.client.api_call.return_value = {"responseStatus": "SUCCESS"}

        # Call the method
        result = edl_service.update_node_order(
            "0000000000000JIT", "0000000000000JLL", 2
        )

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert (
            args[0]
            == "api/v25.1/composites/trees/edl_hierarchy__v/0000000000000JIT/children"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["json"] == {"id": "0000000000000JLL", "order__v": "2"}

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"

    def test_add_edl_matched_documents(self, edl_service):
        """Test add_edl_matched_documents"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "id": "0EI000000001234",
                    "document_id": "DOC001",
                }
            ],
        }

        # Test data
        matches = [
            {
                "id": "0EI000000001234",
                "document_id": "DOC001",
                "major_version_number__v": 1,
                "minor_version_number__v": 0,
                "lock": True,
            }
        ]

        # Call the method
        result = edl_service.add_edl_matched_documents(matches)

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert args[0] == "api/v25.1/objects/edl_matched_documents/batch/actions/add"
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == matches

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"][0]["id"] == "0EI000000001234"
        assert result["data"][0]["document_id"] == "DOC001"

    def test_remove_edl_matched_documents(self, edl_service):
        """Test remove_edl_matched_documents"""
        # Mock response
        edl_service.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "responseStatus": "SUCCESS",
                    "id": "0EI000000001234",
                    "document_id": "DOC001",
                }
            ],
        }

        # Test data
        matches = [
            {
                "id": "0EI000000001234",
                "document_id": "DOC001",
                "major_version_number__v": 1,
                "minor_version_number__v": 0,
                "remove_locked": True,
            }
        ]

        # Call the method
        result = edl_service.remove_edl_matched_documents(matches)

        # Verify the API call
        edl_service.client.api_call.assert_called_once()
        args, kwargs = edl_service.client.api_call.call_args
        assert args[0] == "api/v25.1/objects/edl_matched_documents/batch/actions/remove"
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == matches

        # Verify the result
        assert result["responseStatus"] == "SUCCESS"
        assert result["data"][0]["id"] == "0EI000000001234"
        assert result["data"][0]["document_id"] == "DOC001"


@mark.integration
@mark.veevavault
class TestEDLServiceIntegration:
    """
    Integration tests for EDLService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def edl_service(self, authenticated_vault_client):
        """Returns a EDLService with an authenticated client"""
        return EDLService(authenticated_vault_client)

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_create_placeholder_from_edl_item(self, edl_service):
        """Test create_placeholder_from_edl_item with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test is skipped because it requires existing EDL items
        # and would create actual placeholders in the system

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_retrieve_all_root_nodes(self, edl_service):
        """Test retrieve_all_root_nodes with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call the method
        result = edl_service.retrieve_all_root_nodes()

        # Basic verification
        assert result["responseStatus"] == "SUCCESS"
        assert "data" in result

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_retrieve_specific_root_nodes(self, edl_service):
        """Test retrieve_specific_root_nodes with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test is skipped because it requires existing EDL records

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_retrieve_node_children(self, edl_service):
        """Test retrieve_node_children with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # First get available root nodes
        root_nodes = edl_service.retrieve_all_root_nodes()
        if not root_nodes.get("data") or len(root_nodes["data"]) == 0:
            pytest.skip("No EDL root nodes available for testing")

        # Get the ID of the first root node
        node_id = root_nodes["data"][0]["id"]

        # Call the method
        result = edl_service.retrieve_node_children(node_id)

        # Basic verification
        assert result["responseStatus"] == "SUCCESS"
        assert "data" in result

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_update_node_order(self, edl_service):
        """Test update_node_order with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test is skipped because it would modify actual node ordering
        # in the system and requires specific node setup

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_add_edl_matched_documents(self, edl_service):
        """Test add_edl_matched_documents with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test is skipped because it would add actual document matches
        # and requires Application: EDL Matching: Edit Document Matches permission

    @pytest.mark.skip("EDL integration tests require specific EDL data setup")
    def test_remove_edl_matched_documents(self, edl_service):
        """Test remove_edl_matched_documents with real API"""
        # Skip if not authenticated
        if not edl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test is skipped because it would remove actual document matches
        # and requires Application: EDL Matching: Edit Document Matches permission
