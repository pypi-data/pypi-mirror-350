from pytest import mark, fixture
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.lifecycle_and_workflow import DocumentLifecycleWorkflowService


@fixture(scope="function")
def doc_lifecycle_service(authenticated_vault_client):
    """Returns a DocumentLifecycleWorkflowService instance using the authenticated Vault client"""
    return DocumentLifecycleWorkflowService(authenticated_vault_client)


@fixture(scope="function")
def mock_user_actions_data():
    """Provides standard mock data for document user actions tests"""
    return {
        "responseStatus": "SUCCESS",
        "lifecycle_actions": [
            {
                "name__v": "submit_for_review__c",
                "label__v": "Submit for Review",
                "lifecycle_action_type__v": "state_change",
                "lifecycle__v": "document_lifecycle__c",
                "state__v": "draft__c",
                "executable__v": True,
                "entry_requirements__v": False,
            },
            {
                "name__v": "review_approval_workflow__c",
                "label__v": "Review & Approval",
                "lifecycle_action_type__v": "workflow",
                "lifecycle__v": "document_lifecycle__c",
                "state__v": "draft__c",
                "executable__v": True,
                "entry_requirements__v": True,
            },
        ],
    }


@fixture(scope="function")
def mock_entry_criteria_data():
    """Provides standard mock data for document entry criteria tests"""
    return {
        "responseStatus": "SUCCESS",
        "entry_requirements": [
            {
                "name": "reason_for_change__c",
                "description": "Reason for Change",
                "type": "picklist",
                "required": True,
                "editable": True,
                "values": [
                    {"value": "initial_version__c", "label": "Initial Version"},
                    {"value": "update__c", "label": "Update"},
                    {"value": "correction__c", "label": "Correction"},
                ],
                "currentSetting": None,
            },
            {
                "name": "comments__c",
                "description": "Comments",
                "type": "string",
                "required": False,
                "editable": True,
                "currentSetting": None,
            },
        ],
    }


@fixture(scope="function")
def mock_workflow_data():
    """Provides standard mock data for document workflow tests"""
    return {
        "responseStatus": "SUCCESS",
        "workflows": [
            {
                "name": "review_workflow__c",
                "label": "Review Workflow",
                "type": "workflow",
                "cardinality": "document",
            },
            {
                "name": "approval_workflow__c",
                "label": "Approval Workflow",
                "type": "workflow",
                "cardinality": "document",
            },
        ],
    }


@mark.unit
@mark.veevavault
class TestDocumentLifecycleWorkflowUnit:
    """
    Unit tests for DocumentLifecycleWorkflowService class using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_user_actions(
        self, mock_request, authenticated_vault_client, mock_user_actions_data
    ):
        """Test retrieve_document_user_actions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_user_actions_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_document_user_actions("doc_123", "1", "0")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/doc_123/versions/1/0/lifecycle_actions"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["lifecycle_actions"]) == 2
        assert result["lifecycle_actions"][0]["name__v"] == "submit_for_review__c"
        assert (
            result["lifecycle_actions"][1]["name__v"] == "review_approval_workflow__c"
        )

    @patch("requests.request")
    def test_retrieve_user_actions_on_multiple_documents(
        self, mock_request, authenticated_vault_client, mock_user_actions_data
    ):
        """Test retrieve_user_actions_on_multiple_documents method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_user_actions_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_user_actions_on_multiple_documents("123:1:0,124:1:0")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/lifecycle_actions")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"]["docIds"] == "123:1:0,124:1:0"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["lifecycle_actions"]) == 2

    @patch("requests.request")
    def test_retrieve_document_entry_criteria(
        self, mock_request, authenticated_vault_client, mock_entry_criteria_data
    ):
        """Test retrieve_document_entry_criteria method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_entry_criteria_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_document_entry_criteria(
            "doc_123", "1", "0", "review_approval_workflow__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/doc_123/versions/1/0/lifecycle_actions/review_approval_workflow__c/entry_requirements"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["entry_requirements"]) == 2
        assert result["entry_requirements"][0]["name"] == "reason_for_change__c"
        assert result["entry_requirements"][0]["required"] == True

    @patch("requests.request")
    def test_initiate_document_user_action(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_document_user_action method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "workflow_id__v": "wf_123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {
            "reason_for_change__c": "initial_version__c",
            "comments__c": "Test comment",
        }

        # Call method to test
        result = service.initiate_document_user_action(
            "doc_123", "1", "0", "review_approval_workflow__c", test_data
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/doc_123/versions/1/0/lifecycle_actions/review_approval_workflow__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"] == test_data

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["workflow_id__v"] == "wf_123"

    @patch("requests.request")
    def test_download_controlled_copy_job_results(
        self, mock_request, authenticated_vault_client
    ):
        """Test download_controlled_copy_job_results method"""
        # Set up mock response
        mock_response = MagicMock()
        # For binary responses, content is accessed directly rather than json()
        mock_response.content = b"Test file content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.download_controlled_copy_job_results(
            "doc_lifecycle__c.approved__c.controlled_copy__c", "job_123"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/actions/doc_lifecycle__c.approved__c.controlled_copy__c/job_123/results"
        )
        assert kwargs["method"] == "GET"

        # For this test we're not verifying the content as the method would return the raw response

    @patch("requests.request")
    def test_initiate_bulk_document_user_actions(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_bulk_document_user_actions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job_456",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {"reason_for_change__c": "update__c"}

        # Call method to test
        result = service.initiate_bulk_document_user_actions(
            "review_workflow__c",
            "123:1:0,124:1:0,125:1:0",
            "document_lifecycle__c",
            "draft__c",
            test_data,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/lifecycle_actions/review_workflow__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"]["docIds"] == "123:1:0,124:1:0,125:1:0"
        assert kwargs["data"]["lifecycle"] == "document_lifecycle__c"
        assert kwargs["data"]["state"] == "draft__c"
        assert kwargs["data"]["reason_for_change__c"] == "update__c"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job_456"

    @patch("requests.request")
    def test_retrieve_binder_user_actions(
        self, mock_request, authenticated_vault_client, mock_user_actions_data
    ):
        """Test retrieve_binder_user_actions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_user_actions_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_binder_user_actions("binder_123", "1", "0")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/binders/binder_123/versions/1/0/lifecycle_actions"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["lifecycle_actions"]) == 2

    @patch("requests.request")
    def test_retrieve_user_actions_on_multiple_binders(
        self, mock_request, authenticated_vault_client, mock_user_actions_data
    ):
        """Test retrieve_user_actions_on_multiple_binders method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_user_actions_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_user_actions_on_multiple_binders("123:1:0,124:1:0")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/binders/lifecycle_actions")
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["docIds"] == "123:1:0,124:1:0"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["lifecycle_actions"]) == 2

    @patch("requests.request")
    def test_retrieve_binder_entry_criteria(
        self, mock_request, authenticated_vault_client, mock_entry_criteria_data
    ):
        """Test retrieve_binder_entry_criteria method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_entry_criteria_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_binder_entry_criteria(
            "binder_123", "1", "0", "review_workflow__c"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/binders/binder_123/versions/1/0/lifecycle_actions/review_workflow__c/entry_requirements"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["entry_requirements"]) == 2

    @patch("requests.request")
    def test_initiate_binder_user_action(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_binder_user_action method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "workflow_id__v": "wf_123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {"reason_for_change__c": "update__c", "comments__c": "Test comment"}

        # Call method to test
        result = service.initiate_binder_user_action(
            "binder_123", "1", "0", "review_workflow__c", test_data
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/binders/binder_123/versions/1/0/lifecycle_actions/review_workflow__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"] == test_data

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["workflow_id__v"] == "wf_123"

    @patch("requests.request")
    def test_initiate_bulk_binder_user_actions(
        self, mock_request, authenticated_vault_client
    ):
        """Test initiate_bulk_binder_user_actions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job_456",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {"reason_for_change__c": "update__c"}

        # Call method to test
        result = service.initiate_bulk_binder_user_actions(
            "review_workflow__c",
            "123:1:0,124:1:0",
            "binder_lifecycle__c",
            "draft__c",
            test_data,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/binders/lifecycle_actions/review_workflow__c"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["data"]["docIds"] == "123:1:0,124:1:0"
        assert kwargs["data"]["lifecycle"] == "binder_lifecycle__c"
        assert kwargs["data"]["state"] == "draft__c"
        assert kwargs["data"]["reason_for_change__c"] == "update__c"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job_456"

    @patch("requests.request")
    def test_retrieve_lifecycle_role_assignment_rules(
        self, mock_request, authenticated_vault_client
    ):
        """Test retrieve_lifecycle_role_assignment_rules method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "roleAssignmentRules": [
                {
                    "lifecycle__v": "document_lifecycle__c",
                    "role__v": "owner__v",
                    "allowed_users__v": ["user1", "user2"],
                    "allowed_groups__v": ["group1"],
                    "allowed_default_users__v": ["user1"],
                    "allowed_default_groups__v": [],
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_lifecycle_role_assignment_rules(
            lifecycle="document_lifecycle__c", role="owner__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/configuration/role_assignment_rule")
        assert kwargs["method"] == "GET"
        assert kwargs["params"]["lifecycle__v"] == "document_lifecycle__c"
        assert kwargs["params"]["role__v"] == "owner__v"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["roleAssignmentRules"]) == 1
        assert (
            result["roleAssignmentRules"][0]["lifecycle__v"] == "document_lifecycle__c"
        )
        assert result["roleAssignmentRules"][0]["role__v"] == "owner__v"

    @patch("requests.request")
    def test_create_lifecycle_role_assignment_override_rules(
        self, mock_request, authenticated_vault_client
    ):
        """Test create_lifecycle_role_assignment_override_rules method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "roleAssignmentRules": [
                {
                    "responseStatus": "SUCCESS",
                    "lifecycle__v": "document_lifecycle__c",
                    "role__v": "owner__v",
                    "product__v": "product1",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_rules = [
            {
                "lifecycle__v": "document_lifecycle__c",
                "role__v": "owner__v",
                "product__v": "product1",
                "allowed_users__v": ["user1", "user2"],
                "allowed_default_users__v": ["user1"],
            }
        ]

        # Call method to test
        result = service.create_lifecycle_role_assignment_override_rules(test_rules)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/configuration/role_assignment_rule")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify the sent data was properly JSON serialized
        import json

        sent_data = json.loads(kwargs["data"])
        assert sent_data[0]["lifecycle__v"] == "document_lifecycle__c"
        assert sent_data[0]["role__v"] == "owner__v"
        assert sent_data[0]["product__v"] == "product1"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["roleAssignmentRules"]) == 1
        assert (
            result["roleAssignmentRules"][0]["lifecycle__v"] == "document_lifecycle__c"
        )

    @patch("requests.request")
    def test_update_lifecycle_role_assignment_rules(
        self, mock_request, authenticated_vault_client
    ):
        """Test update_lifecycle_role_assignment_rules method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "roleAssignmentRules": [
                {
                    "responseStatus": "SUCCESS",
                    "lifecycle__v": "document_lifecycle__c",
                    "role__v": "owner__v",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_rules = [
            {
                "lifecycle__v": "document_lifecycle__c",
                "role__v": "owner__v",
                "allowed_users__v": ["user1", "user3"],
                "allowed_default_users__v": ["user1"],
            }
        ]

        # Call method to test
        result = service.update_lifecycle_role_assignment_rules(test_rules)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/configuration/role_assignment_rule")
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify the sent data was properly JSON serialized
        import json

        sent_data = json.loads(kwargs["data"])
        assert sent_data[0]["lifecycle__v"] == "document_lifecycle__c"
        assert sent_data[0]["role__v"] == "owner__v"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["roleAssignmentRules"]) == 1

    @patch("requests.request")
    def test_delete_lifecycle_role_assignment_override_rules(
        self, mock_request, authenticated_vault_client
    ):
        """Test delete_lifecycle_role_assignment_override_rules method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "rules_deleted": 1,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.delete_lifecycle_role_assignment_override_rules(
            lifecycle="document_lifecycle__c", role="owner__v", product="product1"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/configuration/role_assignment_rule")
        assert kwargs["method"] == "DELETE"
        assert kwargs["params"]["lifecycle__v"] == "document_lifecycle__c"
        assert kwargs["params"]["role__v"] == "owner__v"
        assert kwargs["params"]["product__v"] == "product1"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["rules_deleted"] == 1

    @patch("requests.request")
    def test_retrieve_all_document_workflows(
        self, mock_request, authenticated_vault_client, mock_workflow_data
    ):
        """Test retrieve_all_document_workflows method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_workflow_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_all_document_workflows()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/actions")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["workflows"]) == 2
        assert result["workflows"][0]["name"] == "review_workflow__c"
        assert result["workflows"][1]["name"] == "approval_workflow__c"

    @patch("requests.request")
    def test_retrieve_document_workflow_details(
        self, mock_request, authenticated_vault_client
    ):
        """Test retrieve_document_workflow_details method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "workflow": {
                "name": "review_workflow__c",
                "label": "Review Workflow",
                "type": "workflow",
                "cardinality": "document",
                "controls": [
                    {
                        "name": "documents__sys",
                        "label": "Documents",
                        "type": "documents",
                        "required": True,
                    },
                    {
                        "name": "reviewer__v",
                        "label": "Reviewer",
                        "type": "participant",
                        "required": True,
                    },
                ],
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Call method to test
        result = service.retrieve_document_workflow_details("review_workflow__c")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/actions/review_workflow__c"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["workflow"]["name"] == "review_workflow__c"
        assert len(result["workflow"]["controls"]) == 2
        assert result["workflow"]["controls"][0]["name"] == "documents__sys"
        assert result["workflow"]["controls"][1]["name"] == "reviewer__v"

    @patch("requests.request")
    def test_initiate_document_workflow(self, mock_request, authenticated_vault_client):
        """Test initiate_document_workflow method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "record_url": "/workflow/123",
            "record_id__v": "123",
            "workflow_id": "wf_123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        service = DocumentLifecycleWorkflowService(authenticated_vault_client)

        # Test data
        test_data = {
            "documents__sys": "doc_123,doc_124",
            "description__sys": "Test workflow",
            "reviewer__v": "user:user_123",
        }

        # Call method to test
        result = service.initiate_document_workflow("review_workflow__c", test_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/actions/review_workflow__c"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["record_id__v"] == "123"
        assert result["workflow_id"] == "wf_123"


@mark.integration
@mark.veevavault
class TestDocumentLifecycleWorkflowIntegration:
    """
    Integration tests for DocumentLifecycleWorkflowService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_document_user_actions(
        self, doc_lifecycle_service, authenticated_vault_client, vault_config
    ):
        """Test retrieve_document_user_actions method with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # This test requires an existing document ID, so we'll skip it
        pytest.skip("Requires a real document ID to test")

    def test_retrieve_all_document_workflows(
        self, doc_lifecycle_service, authenticated_vault_client, vault_config
    ):
        """Test retrieve_all_document_workflows method with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Get all document workflows
        result = doc_lifecycle_service.retrieve_all_document_workflows()

        # Basic validation
        assert result["responseStatus"] == "SUCCESS"
        # We can't assert specific workflows as they depend on the Vault configuration
