import pytest
from unittest.mock import MagicMock
from veevavault.services.workflows.workflow_service import WorkflowService


@pytest.mark.unit
@pytest.mark.veevavault
class TestWorkflowServiceUnit:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = MagicMock()
        self.client.LatestAPIversion = "v25.1"
        self.service = WorkflowService(self.client)

    def test_retrieve_workflows_by_object_record(self):
        expected = {"workflows": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflows(object_name="obj__v", record_id="123")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows",
            params={"object__v": "obj__v", "record_id__v": "123"},
        )
        assert result == expected

    def test_retrieve_workflows_by_participant(self):
        expected = {"workflows": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflows(participant="me()")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows",
            params={"participant": "me()"},
        )
        assert result == expected

    def test_retrieve_workflows_with_filters(self):
        expected = {"workflows": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflows(
            status=["active__v", "completed__v"], offset=5, page_size=50, loc=True
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows",
            params={
                "status__v": "active__v,completed__v",
                "offset": 5,
                "page_size": 50,
                "loc": "true",
            },
        )
        assert result == expected

    def test_retrieve_workflow_details(self):
        expected = {"id": "wf1"}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_details("wf1", loc=True)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/wf1",
            params={"loc": "true"},
        )
        assert result == expected

    def test_retrieve_workflow_actions(self):
        expected = {"actions": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_actions("wf1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/wf1/actions",
            params={},
        )
        assert result == expected

    def test_retrieve_workflow_action_details(self):
        expected = {"action": {}}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_action_details("wf1", "act1", loc=True)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/wf1/actions/act1",
            params={"loc": "true"},
        )
        assert result == expected

    def test_initiate_workflow_action(self):
        expected = {"status": "OK"}
        self.client.api_call.return_value = expected
        payload = {"key": "value"}

        result = self.service.initiate_workflow_action("wf1", "act1", payload)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/wf1/actions/act1",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data='{"key": "value"}',
        )
        assert result == expected


@pytest.mark.integration
@pytest.mark.veevavault
class TestWorkflowServiceIntegration:
    def test_retrieve_workflows_and_details(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = WorkflowService(authenticated_vault_client)

        result = service.retrieve_workflows(participant="me()")
        assert "workflows" in result
        workflows = result.get("workflows") or []
        if not workflows:
            pytest.skip("No workflows available to test details")

        wf_id = workflows[0].get("id")
        details = service.retrieve_workflow_details(wf_id)
        assert details.get("id") == wf_id

    def test_retrieve_workflow_actions_and_details(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = WorkflowService(authenticated_vault_client)

        workflows = (
            service.retrieve_workflows(participant="me()").get("workflows") or []
        )
        if not workflows:
            pytest.skip("No workflows available to test actions")
        wf_id = workflows[0].get("id")

        actions = service.retrieve_workflow_actions(wf_id).get("actions") or []
        if not actions:
            pytest.skip("No workflow actions available to test action details")
        action_name = actions[0].get("name")

        action_details = service.retrieve_workflow_action_details(wf_id, action_name)
        assert "name" in action_details

    def test_initiate_workflow_action(self, authenticated_vault_client):
        pytest.skip(
            "Skipping integration test for initiate_workflow_action because it may change workflow state"
        )
