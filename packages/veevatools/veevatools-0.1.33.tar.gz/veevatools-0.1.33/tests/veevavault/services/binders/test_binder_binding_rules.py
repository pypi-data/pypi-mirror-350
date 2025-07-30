from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderBindingRulesService


@mark.unit
@mark.veevavault
class TestBinderBindingRulesServiceUnit:
    """
    Unit tests for BinderBindingRulesService using mocks
    """

    def test_update_binding_rule(self):
        """Test updating a binding rule for a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": "566"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            binding_rules_service = BinderBindingRulesService(client)

            # Call method to test
            result = binding_rules_service.update_binding_rule(
                "123", binding_rule__v="steady-state", binding_rule_override__v=True
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/binding_rule"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == {
                "binding_rule__v": "steady-state",
                "binding_rule_override__v": True,
            }

            # Verify response
            assert result == {"responseStatus": "SUCCESS", "id": "566"}

    def test_update_binder_section_binding_rule(self):
        """Test updating a binding rule for a binder section"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "1427491342404:-1828014479",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            binding_rules_service = BinderBindingRulesService(client)

            # Call method to test
            result = binding_rules_service.update_binder_section_binding_rule(
                "123", "456", binding_rule__v="current", binding_rule_override__v=False
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections/456/binding_rule"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == {
                "binding_rule__v": "current",
                "binding_rule_override__v": False,
            }

            # Verify response
            assert result == {
                "responseStatus": "SUCCESS",
                "id": "1427491342404:-1828014479",
            }

    def test_update_binder_document_binding_rule(self):
        """Test updating a binding rule for a binder document"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "1427491342404:-1828014479",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            binding_rules_service = BinderBindingRulesService(client)

            # Call method to test
            result = binding_rules_service.update_binder_document_binding_rule(
                "123",
                "456",
                binding_rule__v="specific",
                major_version_number__v="1",
                minor_version_number__v="0",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/documents/456/binding_rule"
            )
            assert kwargs["method"] == "PUT"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == {
                "binding_rule__v": "specific",
                "major_version_number__v": "1",
                "minor_version_number__v": "0",
            }

            # Verify response
            assert result == {
                "responseStatus": "SUCCESS",
                "id": "1427491342404:-1828014479",
            }


@mark.integration
@mark.veevavault
class TestBinderBindingRulesServiceIntegration:
    """
    Integration tests for BinderBindingRulesService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_update_binding_rule(self, authenticated_vault_client, vault_config):
        """Test updating a binding rule for a binder with real API"""
        # Skip if not authenticated or in mock mode
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        binding_rules_service = BinderBindingRulesService(authenticated_vault_client)

        # This test requires an existing binder
        pytest.skip("This test requires an existing binder ID to be configured")

        # # Call method with a real binder ID
        # result = binding_rules_service.update_binding_rule(
        #     "actual_binder_id", binding_rule__v="default"
        # )
        #
        # # Verify response contains expected keys
        # assert result["responseStatus"] == "SUCCESS"
        # assert "id" in result

    def test_update_binder_section_binding_rule(
        self, authenticated_vault_client, vault_config
    ):
        """Test updating a binding rule for a binder section with real API"""
        # Skip if not authenticated or in mock mode
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        binding_rules_service = BinderBindingRulesService(authenticated_vault_client)

        # This test requires an existing binder with sections
        pytest.skip(
            "This test requires an existing binder and section IDs to be configured"
        )

        # # Call method with real IDs
        # result = binding_rules_service.update_binder_section_binding_rule(
        #     "actual_binder_id", "actual_section_id", binding_rule__v="default"
        # )
        #
        # # Verify response contains expected keys
        # assert result["responseStatus"] == "SUCCESS"
        # assert "id" in result

    def test_update_binder_document_binding_rule(
        self, authenticated_vault_client, vault_config
    ):
        """Test updating a binding rule for a binder document with real API"""
        # Skip if not authenticated or in mock mode
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        binding_rules_service = BinderBindingRulesService(authenticated_vault_client)

        # This test requires an existing binder with documents
        pytest.skip(
            "This test requires an existing binder and document node IDs to be configured"
        )

        # # Call method with real IDs
        # result = binding_rules_service.update_binder_document_binding_rule(
        #     "actual_binder_id", "actual_document_node_id", binding_rule__v="specific",
        #     major_version_number__v="1", minor_version_number__v="0"
        # )
        #
        # # Verify response contains expected keys
        # assert result["responseStatus"] == "SUCCESS"
        # assert "id" in result
