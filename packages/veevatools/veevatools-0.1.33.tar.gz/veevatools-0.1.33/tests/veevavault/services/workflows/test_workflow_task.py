import pytest
from unittest.mock import MagicMock
from veevavault.services.workflows.task_service import WorkflowTaskService


@pytest.mark.unit
@pytest.mark.veevavault
class TestWorkflowTaskServiceUnit:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = MagicMock()
        self.client.LatestAPIversion = "v25.1"
        self.service = WorkflowTaskService(self.client)

    def test_retrieve_workflow_tasks_by_object_record(self):
        expected = {"tasks": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_tasks(
            object_name="obj__v", record_id="123"
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks",
            params={"object__v": "obj__v", "record_id__v": "123"},
        )
        assert result == expected

    def test_retrieve_workflow_tasks_by_assignee(self):
        expected = {"tasks": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_tasks(assignee="me()")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks",
            params={"assignee__v": "me()"},
        )
        assert result == expected

    def test_retrieve_workflow_tasks_with_filters_and_loc(self):
        expected = {"tasks": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_tasks(
            status=["available__v", "completed__v"],
            offset=10,
            page_size=25,
            loc=True,
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks",
            params={
                "status__v": "available__v,completed__v",
                "offset": 10,
                "page_size": 25,
                "loc": "true",
            },
        )
        assert result == expected

    def test_retrieve_workflow_task_details(self):
        expected = {"id": "task1"}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_task_details("task1", loc=True)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1",
            params={"loc": "true"},
        )
        assert result == expected

    def test_retrieve_workflow_task_actions(self):
        expected = {"actions": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_task_actions("task1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions",
            params={},
        )
        assert result == expected

    def test_retrieve_workflow_task_action_details(self):
        expected = {"details": {}}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_workflow_task_action_details(
            "task1", "act1", loc=False
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/act1",
            params={},
        )
        assert result == expected

    def test_accept_multi_item_workflow_task(self):
        expected = {"status": "accepted"}
        self.client.api_call.return_value = expected

        result = self.service.accept_multi_item_workflow_task("task1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/mdwaccept",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        assert result == expected

    def test_accept_single_record_workflow_task(self):
        expected = {"status": "accepted"}
        self.client.api_call.return_value = expected

        result = self.service.accept_single_record_workflow_task("task2")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task2/actions/accept",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        assert result == expected

    def test_undo_workflow_task_acceptance(self):
        expected = {"status": "undo"}
        self.client.api_call.return_value = expected

        result = self.service.undo_workflow_task_acceptance("task1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/undoaccept",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        assert result == expected

    def test_complete_multi_item_workflow_task(self):
        import json

        payload = {"key": "value"}
        expected = {"status": "complete"}
        self.client.api_call.return_value = expected

        result = self.service.complete_multi_item_workflow_task("task1", payload)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/mdwcomplete",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps(payload),
        )
        assert result == expected

    def test_complete_single_record_workflow_task(self):
        payload = {"key": "value"}
        expected = {"status": "complete"}
        self.client.api_call.return_value = expected

        result = self.service.complete_single_record_workflow_task("task1", payload)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/complete",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data=payload,
        )
        assert result == expected

    def test_reassign_multi_item_workflow_task(self):
        import json

        expected = {"status": "reassigned"}
        self.client.api_call.return_value = expected

        result = self.service.reassign_multi_item_workflow_task("task1", "user:100")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/mdwreassign",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps({"task_assignee__v": "user:100"}),
        )
        assert result == expected

    def test_reassign_single_record_workflow_task(self):
        expected = {"status": "reassigned"}
        self.client.api_call.return_value = expected

        result = self.service.reassign_single_record_workflow_task("task1", "user:100")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/reassign",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"task_assignee__v": "user:100"},
        )
        assert result == expected

    def test_update_workflow_task_due_date(self):
        expected = {"status": "updated"}
        self.client.api_call.return_value = expected

        result = self.service.update_workflow_task_due_date("task1", "2025-04-20")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/updateduedate",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"task_due_date__v": "2025-04-20"},
        )
        assert result == expected

    def test_cancel_workflow_task(self):
        expected = {"status": "cancelled"}
        self.client.api_call.return_value = expected

        result = self.service.cancel_workflow_task("task1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/cancel",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        assert result == expected

    def test_manage_multi_item_workflow_content(self):
        import json

        payload = {"contents__sys": []}
        expected = {"status": "ok"}
        self.client.api_call.return_value = expected

        result = self.service.manage_multi_item_workflow_content("task1", payload)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/objectworkflows/tasks/task1/actions/mdwmanagecontent",
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps(payload),
        )
        assert result == expected


@pytest.mark.integration
@pytest.mark.veevavault
class TestWorkflowTaskServiceIntegration:
    def test_retrieve_workflow_tasks(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = WorkflowTaskService(authenticated_vault_client)
        result = service.retrieve_workflow_tasks(assignee="me()")
        assert "tasks" in result
        tasks = result.get("tasks") or []
        if not tasks:
            pytest.skip("No workflow tasks available to test further")

    def test_retrieve_task_details_and_actions(self, authenticated_vault_client):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = WorkflowTaskService(authenticated_vault_client)
        tasks = service.retrieve_workflow_tasks(assignee="me()").get("tasks") or []
        if not tasks:
            pytest.skip("No tasks available to test details")
        task_id = tasks[0].get("id")

        details = service.retrieve_workflow_task_details(task_id)
        assert details.get("id") == task_id

        actions = service.retrieve_workflow_task_actions(task_id).get("actions") or []
        if not actions:
            pytest.skip("No actions available to test action details")
        action_name = actions[0].get("name")

        action_details = service.retrieve_workflow_task_action_details(
            task_id, action_name
        )
        assert "name" in action_details

    def test_task_actions_interactions(self, authenticated_vault_client):
        pytest.skip(
            "Skipping integration tests for task action interactions due to potential state changes"
        )
