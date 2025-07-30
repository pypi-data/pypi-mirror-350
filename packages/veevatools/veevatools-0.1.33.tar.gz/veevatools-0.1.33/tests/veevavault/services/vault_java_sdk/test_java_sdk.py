import pytest
from pytest import mark
from unittest.mock import MagicMock, patch
from io import BytesIO

from veevavault.services.vault_java_sdk.vault_java_sdk import VaultJavaSdkService


@mark.unit
@mark.veevavault
class TestVaultJavaSdkUnit:
    """Unit tests for VaultJavaSdkService methods using mocks"""

    def setup_method(self):
        self.client = MagicMock()
        self.client.LatestAPIversion = "v25.1"
        self.service = VaultJavaSdkService(self.client)

    def test_retrieve_source_code_file(self):
        self.client.api_call.return_value = "public class Test {}"
        result = self.service.retrieve_source_code_file("com.example.TestClass")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/code/com.example.TestClass", return_raw=True
        )
        assert result == "public class Test {}"

    def test_enable_vault_extension(self):
        self.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Enabled",
        }
        result = self.service.enable_vault_extension("com.example.TriggerClass")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/code/com.example.TriggerClass/enable", method="PUT"
        )
        assert result["responseStatus"] == "SUCCESS"

    def test_disable_vault_extension(self):
        self.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Disabled",
        }
        result = self.service.disable_vault_extension("com.example.TriggerClass")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/code/com.example.TriggerClass/disable", method="PUT"
        )
        assert result["responseStatus"] == "SUCCESS"

    @patch("builtins.open", return_value=BytesIO(b"dummy code"), create=True)
    def test_add_or_replace_source_code_file(self, mock_open):
        self.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Modified file",
            "url": "https://test.veevavault.com/api/v25.1/code/com/example/TestClass.java",
        }
        file_path = "TestClass.java"
        result = self.service.add_or_replace_source_code_file(file_path)

        mock_open.assert_called_once_with(file_path, "rb")
        self.client.api_call.assert_called_once()
        (called_url,) = self.client.api_call.call_args[0]
        kwargs = self.client.api_call.call_args[1]
        assert called_url == "api/v25.1/code"
        assert kwargs["method"] == "PUT"
        assert "files" in kwargs and "file" in kwargs["files"]
        assert result["responseMessage"] == "Modified file"

    def test_delete_source_code_file(self):
        self.client.api_call.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Deleted file",
        }
        result = self.service.delete_source_code_file("com.example.TestClass")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/code/com.example.TestClass", method="DELETE"
        )
        assert result["responseStatus"] == "SUCCESS"

    def test_validate_imported_package(self):
        self.client.api_call.return_value = {
            "summary": "All good",
            "package_id": "PKG001",
        }
        result = self.service.validate_imported_package("PKG001")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/services/vobject/vault_package__v/PKG001/actions/validate",
            method="POST",
        )
        assert result["package_id"] == "PKG001"

    def test_retrieve_signing_certificate(self):
        pem = "-----BEGIN CERTIFICATE-----abc-----END CERTIFICATE-----"
        self.client.api_call.return_value = pem
        result = self.service.retrieve_signing_certificate("CERT123")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/services/certificate/CERT123", return_raw=True
        )
        assert "BEGIN CERTIFICATE" in result

    def test_retrieve_all_queues(self):
        data = {"responseStatus": "SUCCESS", "data": [{"name": "q1"}]}
        self.client.api_call.return_value = data
        result = self.service.retrieve_all_queues()
        self.client.api_call.assert_called_once_with("api/v25.1/services/queues")
        assert result == data

    def test_retrieve_queue_status(self):
        status = {"name": "q1", "status": "active"}
        self.client.api_call.return_value = status
        result = self.service.retrieve_queue_status("q1")
        self.client.api_call.assert_called_once_with("api/v25.1/services/queues/q1")
        assert result == status

    def test_disable_queue_delivery(self):
        resp = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = resp
        result = self.service.disable_queue_delivery("q1")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/services/queues/q1/actions/disable_delivery", method="PUT"
        )
        assert result["responseStatus"] == "SUCCESS"

    def test_enable_queue_delivery(self):
        resp = {"responseStatus": "SUCCESS"}
        self.client.api_call.return_value = resp
        result = self.service.enable_queue_delivery("q1")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/services/queues/q1/actions/enable_delivery", method="PUT"
        )
        assert result["responseStatus"] == "SUCCESS"

    def test_reset_queue(self):
        resp = {"responseStatus": "SUCCESS", "responseMessage": "Queue reset"}
        self.client.api_call.return_value = resp
        result = self.service.reset_queue("q1")
        self.client.api_call.assert_called_once_with(
            "api/v25.1/services/queues/q1/actions/reset", method="PUT"
        )
        assert result["responseMessage"] == "Queue reset"


@mark.integration
@mark.veevavault
class TestVaultJavaSdkIntegration:
    """Integration tests for VaultJavaSdkService (skipping destructive or untestable cases)"""

    def test_retrieve_source_code_file(self, authenticated_vault_client, vault_config):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        service = VaultJavaSdkService(authenticated_vault_client)
        content = service.retrieve_source_code_file("com.example.TestClass")
        assert isinstance(content, str), "Expected raw source code string"

    def test_enable_vault_extension(self, authenticated_vault_client):
        pytest.skip("Requires a deployed extension class in Vault; skipping by default")

    def test_disable_vault_extension(self, authenticated_vault_client):
        pytest.skip("Requires a deployed extension class in Vault; skipping by default")

    def test_add_or_replace_source_code_file(self, authenticated_vault_client):
        pytest.skip("Cannot upload a real .java file in CI; skipping by default")

    def test_delete_source_code_file(self, authenticated_vault_client):
        pytest.skip("Requires an existing source file in Vault; skipping by default")

    def test_validate_imported_package(self, authenticated_vault_client):
        pytest.skip(
            "Requires an existing imported package in Vault; skipping by default"
        )

    def test_retrieve_signing_certificate(self, authenticated_vault_client):
        pytest.skip("Requires a real certificate ID; skipping by default")

    def test_retrieve_all_queues(self, authenticated_vault_client):
        response = VaultJavaSdkService(authenticated_vault_client).retrieve_all_queues()
        assert response.get("responseStatus") == "SUCCESS"
        assert isinstance(response.get("data"), list)

    def test_retrieve_queue_status(self, authenticated_vault_client):
        queues = VaultJavaSdkService(authenticated_vault_client).retrieve_all_queues()
        if not queues.get("data"):
            pytest.skip("No queues found in this Vault; skipping status test")
        name = queues["data"][0]["name"]
        status = VaultJavaSdkService(authenticated_vault_client).retrieve_queue_status(
            name
        )
        assert status.get("name") == name

    def test_disable_queue_delivery(self, authenticated_vault_client):
        pytest.skip("Destructive action; skipping by default")

    def test_enable_queue_delivery(self, authenticated_vault_client):
        pytest.skip("Destructive action; skipping by default")

    def test_reset_queue(self, authenticated_vault_client):
        pytest.skip("Destructive action; skipping by default")
