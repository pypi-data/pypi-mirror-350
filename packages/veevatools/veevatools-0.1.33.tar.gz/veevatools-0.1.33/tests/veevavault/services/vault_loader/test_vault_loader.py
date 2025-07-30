import pytest
from pytest import mark
from unittest.mock import MagicMock

from veevavault.services.vault_loader.vault_loader import VaultLoaderService


@mark.unit
@mark.veevavault
class TestVaultLoaderServiceUnit:
    """Unit tests for VaultLoaderService methods using mocks"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_client = MagicMock()
        # Use a non-default version to ensure URL construction is dynamic
        self.mock_client.LatestAPIversion = "v99.9"
        self.service = VaultLoaderService(self.mock_client)

    def test_extract_data_files_without_notification(self):
        extract_objects = [
            {
                "object_type": "vobjects__v",
                "object": "product__v",
                "fields": ["id", "name__v"],
            }
        ]
        expected = {
            "responseStatus": "SUCCESS",
            "url": "dummy",
            "job_id": 1,
            "tasks": {"t1": "id"},
        }
        self.mock_client.api_call.return_value = expected

        result = self.service.extract_data_files(extract_objects)

        self.mock_client.api_call.assert_called_once_with(
            "api/v99.9/services/loader/extract",
            method="POST",
            json=extract_objects,
            params={},
        )
        assert result == expected

    def test_extract_data_files_with_notification(self):
        extract_objects = [{"object_type": "documents__v", "fields": ["id", "type__v"]}]
        expected = {"responseStatus": "SUCCESS"}
        self.mock_client.api_call.return_value = expected

        result = self.service.extract_data_files(
            extract_objects, send_notification=True
        )

        self.mock_client.api_call.assert_called_once_with(
            "api/v99.9/services/loader/extract",
            method="POST",
            json=extract_objects,
            params={"sendNotification": "true"},
        )
        assert result == expected

    def test_retrieve_loader_extract_results(self):
        job_id, task_id = 123, "task-abc"
        csv_content = "col1,col2\nval1,val2"
        self.mock_client.api_call.return_value = csv_content

        result = self.service.retrieve_loader_extract_results(job_id, task_id)

        self.mock_client.api_call.assert_called_once_with(
            f"api/v99.9/services/loader/{job_id}/tasks/{task_id}/results",
            headers={"Accept": "text/csv"},
            raw_response=True,
        )
        assert result == csv_content

    def test_retrieve_loader_extract_renditions_results(self):
        job_id, task_id = 456, "task-def"
        csv_content = "rendition_path\n/path/to/file"
        self.mock_client.api_call.return_value = csv_content

        result = self.service.retrieve_loader_extract_renditions_results(
            job_id, task_id
        )

        self.mock_client.api_call.assert_called_once_with(
            f"api/v99.9/services/loader/{job_id}/tasks/{task_id}/results/renditions",
            headers={"Accept": "text/csv"},
            raw_response=True,
        )
        assert result == csv_content

    def test_load_data_objects_without_notification(self):
        load_objects = [
            {
                "object_type": "groups__v",
                "action": "insert",
                "file": "gs://bucket/file.csv",
            }
        ]
        expected = {"responseStatus": "SUCCESS"}
        self.mock_client.api_call.return_value = expected

        result = self.service.load_data_objects(load_objects)

        self.mock_client.api_call.assert_called_once_with(
            "api/v99.9/services/loader/load",
            method="POST",
            json=load_objects,
            params={},
        )
        assert result == expected

    def test_load_data_objects_with_notification(self):
        load_objects = [
            {
                "object_type": "groups__v",
                "action": "update",
                "file": "gs://bucket/file.csv",
            }
        ]
        expected = {"responseStatus": "SUCCESS"}
        self.mock_client.api_call.return_value = expected

        result = self.service.load_data_objects(load_objects, send_notification=True)

        self.mock_client.api_call.assert_called_once_with(
            "api/v99.9/services/loader/load",
            method="POST",
            json=load_objects,
            params={"sendNotification": "true"},
        )
        assert result == expected

    def test_retrieve_load_success_log(self):
        job_id, task_id = 789, "task-ghi"
        csv_content = "responseStatus,id\nSUCCESS,00X"
        self.mock_client.api_call.return_value = csv_content

        result = self.service.retrieve_load_success_log(job_id, task_id)

        self.mock_client.api_call.assert_called_once_with(
            f"api/v99.9/services/loader/{job_id}/tasks/{task_id}/successlog",
            headers={"Accept": "text/csv"},
            raw_response=True,
        )
        assert result == csv_content

    def test_retrieve_load_failure_log(self):
        job_id, task_id = 101, "task-jkl"
        csv_content = "responseStatus,errors\nFAILURE,Some error"
        self.mock_client.api_call.return_value = csv_content

        result = self.service.retrieve_load_failure_log(job_id, task_id)

        self.mock_client.api_call.assert_called_once_with(
            f"api/v99.9/services/loader/{job_id}/tasks/{task_id}/failurelog",
            headers={"Accept": "text/csv"},
            raw_response=True,
        )
        assert result == csv_content


@mark.integration
@mark.veevavault
class TestVaultLoaderServiceIntegration:
    """Integration tests for VaultLoaderService (skipping non-testable methods)"""

    def test_extract_data_files(self, authenticated_vault_client, vault_config):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        service = VaultLoaderService(authenticated_vault_client)
        extract_objects = [
            {
                "object_type": "vobjects__v",
                "object": "product__v",
                "fields": ["id", "name__v"],
            }
        ]

        response = service.extract_data_files(extract_objects)
        assert response["responseStatus"] == "SUCCESS"
        assert "job_id" in response
        assert "tasks" in response

    def test_load_data_objects(self, authenticated_vault_client, vault_config):
        pytest.skip("Load cannot be integration tested without pre-staged CSV files")

    def test_retrieve_loader_extract_results(
        self, authenticated_vault_client, vault_config
    ):
        pytest.skip(
            "Cannot integration test retrieve_loader_extract_results without valid job_id/task_id"
        )

    def test_retrieve_loader_extract_renditions_results(
        self, authenticated_vault_client, vault_config
    ):
        pytest.skip(
            "Cannot integration test retrieve_loader_extract_renditions_results without valid job_id/task_id"
        )

    def test_retrieve_load_success_log(self, authenticated_vault_client, vault_config):
        pytest.skip(
            "Cannot integration test retrieve_load_success_log without valid job_id/task_id"
        )

    def test_retrieve_load_failure_log(self, authenticated_vault_client, vault_config):
        pytest.skip(
            "Cannot integration test retrieve_load_failure_log without valid job_id/task_id"
        )
