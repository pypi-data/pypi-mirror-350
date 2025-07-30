from pytest import mark
import pytest
from unittest.mock import MagicMock

from veevavault.services.sandbox_vaults import SandboxVaultsService


@mark.unit
@mark.veevavault
class TestSandboxVaultsServiceUnit:
    def setup_method(self):
        self.client = MagicMock()
        self.client.LatestAPIversion = "v25.1"
        self.service = SandboxVaultsService(self.client)

    def test_retrieve_sandboxes(self):
        expected = {"entitlements": [], "active": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_sandboxes()

        self.client.api_call.assert_called_once_with("api/v25.1/objects/sandbox")
        assert result == expected

    def test_retrieve_sandbox_details(self):
        vault_id = 123
        expected = {"vault_id": vault_id, "name": "Sandbox1"}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_sandbox_details(vault_id)

        self.client.api_call.assert_called_once_with(
            f"api/v25.1/objects/sandbox/{vault_id}"
        )
        assert result == expected

    def test_recheck_sandbox_usage_limit(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.recheck_sandbox_usage_limit()

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/actions/recheckusage",
            method="POST",
        )
        assert result == expected

    def test_change_sandbox_size(self):
        changes = [{"name": "sb1", "size": "Medium"}]
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.change_sandbox_size(changes)

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/batch/changesize",
            method="POST",
            json=changes,
        )
        assert result == expected

    def test_set_sandbox_entitlements_without_temporary(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.set_sandbox_entitlements(
            name="sb1", size="Small", allowance=2, grant=True
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/entitlements/set",
            method="POST",
            data={"name": "sb1", "size": "Small", "allowance": 2, "grant": "true"},
        )
        assert result == expected

    def test_set_sandbox_entitlements_with_temporary(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.set_sandbox_entitlements(
            name="sb1",
            size="Large",
            allowance=1,
            grant=False,
            temporary_allowance=3,
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/entitlements/set",
            method="POST",
            data={
                "name": "sb1",
                "size": "Large",
                "allowance": 1,
                "grant": "false",
                "temporary_allowance": 3,
            },
        )
        assert result == expected

    def test_create_or_refresh_sandbox_basic(self):
        expected = {"job_id": "job1"}
        self.client.api_call.return_value = expected

        result = self.service.create_or_refresh_sandbox(
            name="sb1", size="Full", domain="sb1.example.com"
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox",
            method="POST",
            data={"name": "sb1", "size": "Full", "domain": "sb1.example.com"},
        )
        assert result == expected

    def test_create_or_refresh_sandbox_optional(self):
        expected = {"job_id": "job2"}
        self.client.api_call.return_value = expected

        result = self.service.create_or_refresh_sandbox(
            name="sb2",
            size="Medium",
            domain="sb2.ex",
            type="config",
            source="vault",
            source_snapshot="snap2",
            add_requester=False,
            release="limited",
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox",
            method="POST",
            data={
                "name": "sb2",
                "size": "Medium",
                "domain": "sb2.ex",
                "type": "config",
                "source": "vault",
                "source_snapshot": "snap2",
                "add_requester": "false",
                "release": "limited",
            },
        )
        assert result == expected

    def test_refresh_sandbox_from_snapshot(self):
        expected = {"job_id": "job3"}
        self.client.api_call.return_value = expected

        result = self.service.refresh_sandbox_from_snapshot(
            vault_id=456, source_snapshot="snap1"
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/456/actions/refresh",
            method="POST",
            data={"source_snapshot": "snap1"},
        )
        assert result == expected

    def test_delete_sandbox(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.delete_sandbox(name="sb1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/sb1", method="DELETE"
        )
        assert result == expected

    def test_create_sandbox_snapshot_basic(self):
        expected = {"job_id": "job4"}
        self.client.api_call.return_value = expected

        result = self.service.create_sandbox_snapshot(
            source_sandbox="sb1", name="snap1"
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot",
            method="POST",
            data={"source_sandbox": "sb1", "name": "snap1", "include_data": "false"},
        )
        assert result == expected

    def test_create_sandbox_snapshot_with_description_and_data(self):
        expected = {"job_id": "job5"}
        self.client.api_call.return_value = expected

        result = self.service.create_sandbox_snapshot(
            source_sandbox="sb1",
            name="snap1",
            description="desc",
            include_data=True,
        )

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot",
            method="POST",
            data={
                "source_sandbox": "sb1",
                "name": "snap1",
                "include_data": "true",
                "description": "desc",
            },
        )
        assert result == expected

    def test_retrieve_sandbox_snapshots(self):
        expected = {"snapshots": [{}]}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_sandbox_snapshots()

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot"
        )
        assert result == expected

    def test_delete_sandbox_snapshot(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.delete_sandbox_snapshot(api_name="snap1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot/snap1", method="DELETE"
        )
        assert result == expected

    def test_update_sandbox_snapshot(self):
        expected = {"job_id": "job6"}
        self.client.api_call.return_value = expected

        result = self.service.update_sandbox_snapshot(api_name="snap1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot/snap1/actions/update",
            method="POST",
        )
        assert result == expected

    def test_upgrade_sandbox_snapshot(self):
        expected = {"job_id": "job7"}
        self.client.api_call.return_value = expected

        result = self.service.upgrade_sandbox_snapshot(api_name="snap1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/snapshot/snap1/actions/upgrade",
            method="POST",
        )
        assert result == expected

    def test_build_production_vault(self):
        expected = {"job_id": "job8"}
        self.client.api_call.return_value = expected

        result = self.service.build_production_vault(source="preprod1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/actions/buildproduction",
            method="POST",
            data={"source": "preprod1"},
        )
        assert result == expected

    def test_promote_to_production(self):
        expected = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = expected

        result = self.service.promote_to_production(name="preprod1")

        self.client.api_call.assert_called_once_with(
            "api/v25.1/objects/sandbox/actions/promoteproduction",
            method="POST",
            data={"name": "preprod1"},
        )
        assert result == expected


@mark.integration
@mark.veevavault
class TestSandboxVaultsServiceIntegration:
    def test_retrieve_sandboxes(self, sandbox_vaults_service):
        """Integration: retrieve all sandboxes"""
        service = sandbox_vaults_service
        if not service.client.sessionId:
            pytest.skip("No authenticated session available")
        result = service.retrieve_sandboxes()
        assert isinstance(result, dict)
        assert "entitlements" in result
        assert "active" in result

    def test_retrieve_sandbox_details(self, sandbox_vaults_service):
        """Integration: retrieve sandbox details for first active sandbox"""
        service = sandbox_vaults_service
        if not service.client.sessionId:
            pytest.skip("No authenticated session available")
        active = service.retrieve_sandboxes().get("active", [])
        if not active:
            pytest.skip("No active sandboxes to retrieve details for")
        vault_id = active[0].get("vault_id")
        result = service.retrieve_sandbox_details(vault_id)
        assert isinstance(result, dict)
        assert result.get("vault_id") == vault_id

    def test_retrieve_sandbox_snapshots(self, sandbox_vaults_service):
        """Integration: retrieve sandbox snapshots"""
        service = sandbox_vaults_service
        if not service.client.sessionId:
            pytest.skip("No authenticated session available")
        result = service.retrieve_sandbox_snapshots()
        assert isinstance(result, dict)
        # Vaults with no snapshots may return {"available": 0, "snapshots": []}
        assert "snapshots" in result or "available" in result

    def test_recheck_sandbox_usage_limit(self, sandbox_vaults_service):
        pytest.skip("Mutating operation; skipping recheck usage limit integration test")

    def test_change_sandbox_size(self, sandbox_vaults_service):
        pytest.skip("Mutating operation; skipping change sandbox size integration test")

    def test_set_sandbox_entitlements(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping set sandbox entitlements integration test"
        )

    def test_create_or_refresh_sandbox(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping create or refresh sandbox integration test"
        )

    def test_refresh_sandbox_from_snapshot(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping refresh sandbox from snapshot integration test"
        )

    def test_delete_sandbox(self, sandbox_vaults_service):
        pytest.skip("Mutating operation; skipping delete sandbox integration test")

    def test_create_sandbox_snapshot(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping create sandbox snapshot integration test"
        )

    def test_delete_sandbox_snapshot(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping delete sandbox snapshot integration test"
        )

    def test_update_sandbox_snapshot(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping update sandbox snapshot integration test"
        )

    def test_upgrade_sandbox_snapshot(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping upgrade sandbox snapshot integration test"
        )

    def test_build_production_vault(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping build production vault integration test"
        )

    def test_promote_to_production(self, sandbox_vaults_service):
        pytest.skip(
            "Mutating operation; skipping promote to production integration test"
        )
