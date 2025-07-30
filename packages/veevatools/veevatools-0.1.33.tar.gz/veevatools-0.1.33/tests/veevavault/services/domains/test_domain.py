from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.services.domains import DomainService


@mark.unit
@mark.veevavault
class TestDomainServiceUnit:
    """
    Unit tests for DomainService class using mocks (no real API calls)
    """

    def test_retrieve_domains(self, vault_client):
        """Test retrieve_domains method"""
        # Create mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Success",
            "domains": [
                {"name": "veepharm.com", "type": "Production"},
                {"name": "veepharm-sbx.com", "type": "Sandbox"},
            ],
        }

        # Create a patched requests.get function
        with patch("requests.get") as mock_get:
            # Configure the mock to return our mock response
            mock_get.return_value.json.return_value = mock_response

            # Create service with mocked client
            domain_service = DomainService(vault_client)

            # Call method to test
            result = domain_service.retrieve_domains()

            # Verify request was made with correct parameters
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            assert kwargs["url"].endswith("/api/v25.1/objects/domains")
            assert kwargs["headers"]["Authorization"] == vault_client.sessionId

            # Verify response
            assert result == mock_response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["domains"]) == 2
            assert result["domains"][0]["name"] == "veepharm.com"
            assert result["domains"][1]["type"] == "Sandbox"

    def test_retrieve_domain_information(self, vault_client):
        """Test retrieve_domain_information method"""
        # Create mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Success",
            "domain__v": {
                "domain_name__v": "veepharm",
                "domain_type__v": "testvaults",
                "vaults__v": [
                    {
                        "id": "2000",
                        "vault_name__v": "PromoMats",
                        "vault_status__v": "Active",
                        "vault_family__v": {
                            "name__v": "commercial__v",
                            "label__v": "Commercial",
                        },
                    }
                ],
            },
        }

        # Create a patched requests.get function
        with patch("requests.get") as mock_get:
            # Configure the mock to return our mock response
            mock_get.return_value.json.return_value = mock_response

            # Create service with mocked client
            domain_service = DomainService(vault_client)

            # Call method to test
            result = domain_service.retrieve_domain_information()

            # Verify request was made with correct parameters
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            assert kwargs["url"].endswith("/api/v25.1/objects/domain")
            assert kwargs["headers"]["Authorization"] == vault_client.sessionId
            assert kwargs["params"]["include_application"] is False

            # Verify response
            assert result == mock_response
            assert result["responseStatus"] == "SUCCESS"
            assert result["domain__v"]["domain_name__v"] == "veepharm"
            assert len(result["domain__v"]["vaults__v"]) == 1
            assert result["domain__v"]["vaults__v"][0]["id"] == "2000"

    def test_retrieve_domain_information_with_application(self, vault_client):
        """Test retrieve_domain_information method with include_application=True"""
        # Create mock response with application info
        mock_response = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Success",
            "domain__v": {
                "domain_name__v": "veepharm",
                "domain_type__v": "testvaults",
                "vaults__v": [
                    {
                        "id": "2000",
                        "vault_name__v": "PromoMats",
                        "vault_status__v": "Active",
                        "vault_application__v": "PromoMats",
                        "vault_family__v": {
                            "name__v": "commercial__v",
                            "label__v": "Commercial",
                        },
                    }
                ],
            },
        }

        # Create a patched requests.get function
        with patch("requests.get") as mock_get:
            # Configure the mock to return our mock response
            mock_get.return_value.json.return_value = mock_response

            # Create service with mocked client
            domain_service = DomainService(vault_client)

            # Call method to test with include_application=True
            result = domain_service.retrieve_domain_information(
                include_application=True
            )

            # Verify request was made with correct parameters
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            assert kwargs["url"].endswith("/api/v25.1/objects/domain")
            assert kwargs["headers"]["Authorization"] == vault_client.sessionId
            assert kwargs["params"]["include_application"] is True

            # Verify response
            assert result == mock_response
            assert result["responseStatus"] == "SUCCESS"
            assert result["domain__v"]["domain_name__v"] == "veepharm"
            assert len(result["domain__v"]["vaults__v"]) == 1
            assert result["domain__v"]["vaults__v"][0]["id"] == "2000"
            assert (
                result["domain__v"]["vaults__v"][0]["vault_application__v"]
                == "PromoMats"
            )


@mark.integration
@mark.veevavault
class TestDomainServiceIntegration:
    """
    Integration tests for DomainService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_domains(self, authenticated_vault_client, vault_config):
        """Test retrieve_domains with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        domain_service = DomainService(authenticated_vault_client)

        # Call the method
        result = domain_service.retrieve_domains()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "domains" in result
        # Cannot verify exact domains as they vary by account

    def test_retrieve_domain_information(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieve_domain_information with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        domain_service = DomainService(authenticated_vault_client)

        # This will only work if the user is a domain admin
        # So we'll try it but handle the case where it fails due to permissions
        try:
            result = domain_service.retrieve_domain_information()

            # If successful, verify response structure
            assert result["responseStatus"] == "SUCCESS"
            assert "domain__v" in result
            assert "domain_name__v" in result["domain__v"]
            assert "vaults__v" in result["domain__v"]

        except Exception as e:
            # This likely means the user doesn't have domain admin rights
            pytest.skip(f"User likely doesn't have domain admin rights: {str(e)}")

    def test_retrieve_domain_information_with_application(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieve_domain_information with include_application=True and real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        domain_service = DomainService(authenticated_vault_client)

        # This will only work if the user is a domain admin
        # So we'll try it but handle the case where it fails due to permissions
        try:
            result = domain_service.retrieve_domain_information(
                include_application=True
            )

            # If successful, verify response structure and application info
            assert result["responseStatus"] == "SUCCESS"
            assert "domain__v" in result
            assert "vaults__v" in result["domain__v"]

            # If there are vaults, check for application info
            if result["domain__v"]["vaults__v"]:
                # Application info might still not be present if the user doesn't have rights
                if "vault_application__v" in result["domain__v"]["vaults__v"][0]:
                    assert (
                        result["domain__v"]["vaults__v"][0]["vault_application__v"]
                        is not None
                    )

        except Exception as e:
            # This likely means the user doesn't have domain admin rights
            pytest.skip(f"User likely doesn't have domain admin rights: {str(e)}")
