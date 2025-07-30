from pytest import mark, fixture
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.lifecycle_and_workflow import ObjectLifecycleWorkflowService


@fixture(scope="function")
def obj_lifecycle_service(authenticated_vault_client):
    """Returns an ObjectLifecycleWorkflowService instance using the authenticated Vault client"""
    return ObjectLifecycleWorkflowService(authenticated_vault_client)


@fixture(scope="function")
def mock_object_user_actions_data():
    """Provides standard mock data for object user actions tests"""
    return {
        "responseStatus": "SUCCESS",
        "actions": [
            {
                "name": "Objectlifecyclestateuseraction.product__v.draft__c.submit_for_approval__c",
                "label": "Submit for Approval",
                "type": "state_change",
                "url": "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectlifecyclestateuseraction.product__v.draft__c.submit_for_approval__c",
                "links": [
                    {
                        "rel": "execute",
                        "href": "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectlifecyclestateuseraction.product__v.draft__c.submit_for_approval__c",
                        "method": "POST",
                    }
                ],
            },
            {
                "name": "Objectaction.product__v.initiate_review__c",
                "label": "Initiate Review",
                "type": "workflow",
                "url": "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectaction.product__v.initiate_review__c",
                "links": [
                    {
                        "rel": "self",
                        "href": "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectaction.product__v.initiate_review__c",
                        "method": "GET",
                    }
                ],
            },
        ],
    }


@fixture(scope="function")
def mock_object_action_details_data():
    """Provides standard mock data for object action details tests"""
    return {
        "responseStatus": "SUCCESS",
        "action": {
            "name": "Objectaction.product__v.initiate_review__c",
            "label": "Initiate Review",
            "type": "workflow",
            "controls": [
                {
                    "name": "instructions__v",
                    "label": "Instructions",
                    "type": "instructions",
                    "value": "Please provide all necessary information for the review.",
                },
                {
                    "name": "reviewer__v",
                    "label": "Reviewer",
                    "type": "participant",
                    "prompts": [
                        {
                            "name": "assignment_type__c",
                            "label": "Assignment Type",
                            "type": "picklist",
                            "required": true,
                            "values": [
                                {"value": "assigned__c", "label": "Assigned"},
                                {"value": "available__c", "label": "Available"},
                            ],
                            "currentSetting": null,
                        }
                    ],
                },
            ],
            "links": [
                {
                    "rel": "execute",
                    "href": "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectaction.product__v.initiate_review__c",
                    "method": "POST",
                }
            ],
        },
    }


@fixture(scope="function")
def mock_multi_workflows_data():
    """Provides standard mock data for multi-record workflow tests"""
    return {
        "responseStatus": "SUCCESS",
        "workflows": [
            {
                "name": "batch_approval__c",
                "label": "Batch Approval",
                "type": "workflow",
                "cardinality": "object",
            },
            {
                "name": "multi_product_review__c",
                "label": "Multi-Product Review",
                "type": "workflow",
                "cardinality": "object",
            },
        ],
    }


@fixture(scope="function")
def mock_workflow_details_data():
    """Provides standard mock data for workflow details tests"""
    return {
        "responseStatus": "SUCCESS",
        "workflow": {
            "name": "batch_approval__c",
            "label": "Batch Approval",
            "type": "workflow",
            "cardinality": "object",
            "controls": [
                {
                    "name": "contents__sys",
                    "label": "Contents",
                    "type": "content_records",
                    "required": True,
                },
                {
                    "name": "description__sys",
                    "label": "Description",
                    "type": "description",
                    "required": True,
                },
                {
                    "name": "approver__c",
                    "label": "Approver",
                    "type": "participant",
                    "required": True,
                },
            ],
        },
    }


@mark.unit
@mark.veevavault
class TestObjectLifecycleWorkflowUnit:
    """
    Unit tests for ObjectLifecycleWorkflowService class using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_object_record_user_actions(
        self, mock_request, authenticated_vault_client, mock_object_user_actions_data
    ):
        """Test retrieve_object_record_user_actions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_object_user_actions_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_object_record_user_actions(
            "product__v", "PV000000001001"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/PV000000001001/actions"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["actions"]) == 2
        assert (
            result["actions"][0]["name"]
            == "Objectlifecyclestateuseraction.product__v.draft__c.submit_for_approval__c"
        )
        assert (
            result["actions"][1]["name"] == "Objectaction.product__v.initiate_review__c"
        )

    @patch("requests.request")
    def test_retrieve_object_user_action_details(
        self, mock_request, authenticated_vault_client, mock_object_action_details_data
    ):
        """Test retrieve_object_user_action_details method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_object_action_details_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_object_user_action_details(
            "product__v", "PV000000001001", "Objectaction.product__v.initiate_review__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectaction.product__v.initiate_review__c"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["action"]["name"] == "Objectaction.product__v.initiate_review__c"
        assert result["action"]["type"] == "workflow"
        assert len(result["action"]["controls"]) == 2
        assert result["action"]["controls"][0]["name"] == "instructions__v"
        assert result["action"]["controls"][1]["name"] == "reviewer__v"

    @patch("requests.request")
    def test_initiate_object_action_on_single_record(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_object_action_on_single_record method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "record_url": "/workflow/123",
            "record_id__v": "123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {
            "reviewer__v": "user:user_123",
            "assignment_type__c": "assigned__c",
            "comments__c": "Please review this product",
        }

        # Call method to test
        result = service.initiate_object_action_on_single_record(
            "product__v",
            "PV000000001001",
            "Objectaction.product__v.initiate_review__c",
            test_data,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/PV000000001001/actions/Objectaction.product__v.initiate_review__c"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"] == test_data

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["record_id__v"] == "123"

    @patch("requests.request")
    def test_initiate_object_action_on_multiple_records(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_object_action_on_multiple_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": "PV000000001001",
                    "responseStatus": "SUCCESS",
                    "workflow_id__v": "wf_123",
                },
                {
                    "id": "PV000000001002",
                    "responseStatus": "SUCCESS",
                    "workflow_id__v": "wf_124",
                },
                {
                    "id": "PV000000001003",
                    "responseStatus": "FAILURE",
                    "errors": [
                        {
                            "type": "INVALID_STATE",
                            "message": "Record is not in required state",
                        }
                    ],
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {
            "reviewer__v": "user:user_123",
            "assignment_type__c": "assigned__c",
        }
        record_ids = "PV000000001001,PV000000001002,PV000000001003"

        # Call method to test
        result = service.initiate_object_action_on_multiple_records(
            "product__v",
            "Objectaction.product__v.initiate_review__c",
            record_ids,
            test_data,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/product__v/actions/Objectaction.product__v.initiate_review__c"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["ids"] == record_ids
        assert kwargs["data"]["reviewer__v"] == "user:user_123"
        assert kwargs["data"]["assignment_type__c"] == "assigned__c"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 3
        assert result["data"][0]["responseStatus"] == "SUCCESS"
        assert result["data"][0]["workflow_id__v"] == "wf_123"
        assert result["data"][2]["responseStatus"] == "FAILURE"

    @patch("requests.request")
    def test_retrieve_all_multi_record_workflows(
        self, mock_request, authenticated_vault_client, mock_multi_workflows_data
    ):
        """Test retrieve_all_multi_record_workflows method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_multi_workflows_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_all_multi_record_workflows()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/objectworkflows/actions")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["workflows"]) == 2
        assert result["workflows"][0]["name"] == "batch_approval__c"
        assert result["workflows"][1]["name"] == "multi_product_review__c"

    @patch("requests.request")
    def test_retrieve_multi_record_workflow_details(
        self, mock_request, authenticated_vault_client, mock_workflow_details_data
    ):
        """Test retrieve_multi_record_workflow_details method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_workflow_details_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_multi_record_workflow_details("batch_approval__c")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/objectworkflows/actions/batch_approval__c"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["workflow"]["name"] == "batch_approval__c"
        assert len(result["workflow"]["controls"]) == 3
        assert result["workflow"]["controls"][0]["name"] == "contents__sys"
        assert result["workflow"]["controls"][2]["name"] == "approver__c"

    @patch("requests.request")
    def test_initiate_multi_record_workflow(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_multi_record_workflow method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "record_url": "/workflow/456",
            "record_id__v": "456",
            "workflow_id": "wf_456",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = ObjectLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {
            "contents__sys": "Object:product__v.PV000000001001,Object:product__v.PV000000001002",
            "description__sys": "Batch approval for multiple products",
            "approver__c": "user:user_456",
        }

        # Call method to test
        result = service.initiate_multi_record_workflow("batch_approval__c", test_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/objectworkflows/actions/batch_approval__c"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == test_data

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["record_id__v"] == "456"
        assert result["workflow_id"] == "wf_456"


@mark.integration
@mark.veevavault
class TestObjectLifecycleWorkflowIntegration:
    """
    Integration tests for ObjectLifecycleWorkflowService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_object_record_user_actions(
        self, obj_lifecycle_service, authenticated_vault_client, vault_config
    ):
        """Test retrieve_object_record_user_actions method with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # This test requires an existing object record ID, so we'll skip it
        pytest.skip("Requires a real object record ID to test")

    def test_retrieve_all_multi_record_workflows(
        self, obj_lifecycle_service, authenticated_vault_client, vault_config
    ):
        """Test retrieve_all_multi_record_workflows method with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Get all multi-record workflows
        result = obj_lifecycle_service.retrieve_all_multi_record_workflows()

        # Basic validation
        assert result["responseStatus"] == "SUCCESS"
        # We can't assert specific workflows as they depend on the Vault configuration
