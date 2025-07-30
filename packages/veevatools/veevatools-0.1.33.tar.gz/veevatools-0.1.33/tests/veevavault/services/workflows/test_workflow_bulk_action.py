import pytest
from unittest.mock import MagicMock
from veevavault.services.workflows.bulk_action_service import BulkWorkflowActionService


@pytest.mark.unit
@pytest.mark.veevavault
class TestBulkWorkflowActionServiceUnit:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = MagicMock()
        self.client.LatestAPIversion = "v25.1"
        self.service = BulkWorkflowActionService(self.client)

    def test_retrieve_bulk_workflow_actions(self):
        expected = {"actions": [{"name": "action1", "label": "Action 1"}]}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_bulk_workflow_actions()

        self.client.api_call.assert_called_once_with(
            "api/v25.1/object/workflow/actions",
            headers={"Accept": "application/json"},
        )
        assert result == expected

    def test_retrieve_bulk_workflow_action_details(self):
        action = "action1"
        expected = {"name": action, "fields": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_bulk_workflow_action_details(action)

        self.client.api_call.assert_called_once_with(
            f"api/v25.1/object/workflow/actions/{action}",
            headers={"Accept": "application/json"},
        )
        assert result == expected

    def test_initiate_bulk_workflow_action(self):
        action = "action1"
        payload = {"param": "value"}
        expected = {"job_id": "job123"}
        self.client.api_call.return_value = expected

        result = self.service.initiate_bulk_workflow_action(action, payload)

        self.client.api_call.assert_called_once_with(
            f"api/v25.1/object/workflow/actions/{action}",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data=payload,
        )
        assert result == expected


@pytest.mark.integration
@pytest.mark.veevavault
class TestBulkWorkflowActionServiceIntegration:
    def test_retrieve_bulk_workflow_actions(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = BulkWorkflowActionService(authenticated_vault_client)
        result = service.retrieve_bulk_workflow_actions()
        assert "actions" in result
        assert isinstance(result["actions"], list)

    def test_retrieve_bulk_workflow_action_details(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = BulkWorkflowActionService(authenticated_vault_client)
        actions = service.retrieve_bulk_workflow_actions().get("actions") or []
        if not actions:
            pytest.skip("No bulk workflow actions available to retrieve details for")
        action_name = actions[0].get("name")
        result = service.retrieve_bulk_workflow_action_details(action_name)
        assert "name" in result

    def test_initiate_bulk_workflow_action(self, authenticated_vault_client):
        pytest.skip(
            "Skipping integration test for initiate_bulk_workflow_action because it initiates background jobs"
        )
