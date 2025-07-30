from pytest import mark, fixture
import pytest
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.custom_pages import CustomPagesService


@mark.unit
@mark.veevavault
class TestCustomPagesServiceUnit:
    """
    Unit tests for CustomPagesService class using mocks (no real API calls)
    """

    @fixture
    def custom_pages_service(self):
        """Fixture for CustomPagesService with mocked client"""
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"
        return CustomPagesService(client)

    @patch("veevavault.client.VaultClient.api_call")
    def test_retrieve_all_client_code_distributions(
        self, mock_api_call, custom_pages_service
    ):
        """Test retrieve_all_client_code_distributions method"""
        # Set up mock response
        mock_api_call.return_value = {
            "responseStatus": "SUCCESS",
            "distributions": [
                {"name": "distribution1", "checksum": "abc123", "size": 12345},
                {"name": "distribution2", "checksum": "def456", "size": 67890},
            ],
        }

        # Call the method
        result = custom_pages_service.retrieve_all_client_code_distributions()

        # Verify API call was made with correct parameters
        mock_api_call.assert_called_once_with("api/v25.1/uicode/distributions")

        # Verify response was parsed correctly
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["distributions"]) == 2
        assert result["distributions"][0]["name"] == "distribution1"
        assert result["distributions"][1]["checksum"] == "def456"

    @patch("veevavault.client.VaultClient.api_call")
    def test_retrieve_client_code_distribution(
        self, mock_api_call, custom_pages_service
    ):
        """Test retrieve_client_code_distribution method"""
        # Set up mock response
        mock_api_call.return_value = {
            "responseStatus": "SUCCESS",
            "name": "distribution1",
            "checksum": "abc123",
            "size": 12345,
            "pages": [{"name": "page1", "file": "page1.html", "export": "exportName1"}],
            "stylesheets": ["style1.css", "style2.css"],
            "importmap": {"imports": {"module1": "./module1.js"}},
        }

        # Call the method
        result = custom_pages_service.retrieve_client_code_distribution("distribution1")

        # Verify API call was made with correct parameters
        mock_api_call.assert_called_once_with(
            "api/v25.1/uicode/distributions/distribution1"
        )

        # Verify response was parsed correctly
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "distribution1"
        assert result["checksum"] == "abc123"
        assert len(result["pages"]) == 1
        assert result["pages"][0]["name"] == "page1"
        assert len(result["stylesheets"]) == 2
        assert "imports" in result["importmap"]

    @patch("veevavault.client.VaultClient.api_call")
    def test_download_client_code_distribution(
        self, mock_api_call, custom_pages_service
    ):
        """Test download_client_code_distribution method"""
        # Create mock binary content
        mock_response = MagicMock()
        mock_response.content = b"fake zip content"
        mock_response.headers = {"Content-Type": "application/zip;charset=UTF-8"}
        mock_api_call.return_value = mock_response

        # Call the method
        result = custom_pages_service.download_client_code_distribution("distribution1")

        # Verify API call was made with correct parameters
        mock_api_call.assert_called_once_with(
            "api/v25.1/uicode/distributions/distribution1/code", raw_response=True
        )

        # Verify the raw response was returned
        assert result == mock_response

    @patch("veevavault.client.VaultClient.api_call")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake zip content")
    def test_upload_client_code_distribution(
        self, mock_file_open, mock_api_call, custom_pages_service
    ):
        """Test upload_client_code_distribution method"""
        # Set up mock response
        mock_api_call.return_value = {
            "responseStatus": "SUCCESS",
            "name": "distribution1",
            "updateType": "ADDED",
            "checksum": "abc123",
        }

        # Call the method
        result = custom_pages_service.upload_client_code_distribution("fake_path.zip")

        # Verify file was opened
        mock_file_open.assert_called_once_with("fake_path.zip", "rb")

        # Verify API call was made with correct parameters
        mock_api_call.assert_called_once()
        args, kwargs = mock_api_call.call_args
        assert args[0] == "api/v25.1/uicode/distributions/"
        assert kwargs["method"] == "POST"
        assert "files" in kwargs

        # Verify response was parsed correctly
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == "distribution1"
        assert result["updateType"] == "ADDED"
        assert result["checksum"] == "abc123"

    @patch("veevavault.client.VaultClient.api_call")
    def test_delete_client_code_distribution(self, mock_api_call, custom_pages_service):
        """Test delete_client_code_distribution method"""
        # Set up mock response
        mock_api_call.return_value = {"responseStatus": "SUCCESS"}

        # Call the method
        result = custom_pages_service.delete_client_code_distribution("distribution1")

        # Verify API call was made with correct parameters
        mock_api_call.assert_called_once_with(
            "api/v25.1/uicode/distributions/distribution1", method="DELETE"
        )

        # Verify response was parsed correctly
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestCustomPagesServiceIntegration:
    """
    Integration tests for CustomPagesService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def custom_pages_service(self, authenticated_vault_client):
        """Fixture for authenticated CustomPagesService"""
        return CustomPagesService(authenticated_vault_client)

    def test_retrieve_all_client_code_distributions(
        self, custom_pages_service, vault_config
    ):
        """Test retrieve_all_client_code_distributions with real API"""
        # Skip if not authenticated
        if not custom_pages_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call the method
        result = custom_pages_service.retrieve_all_client_code_distributions()

        # Verify the response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "distributions" in result

    def test_retrieve_client_code_distribution(
        self, custom_pages_service, vault_config
    ):
        """Test retrieve_client_code_distribution with real API"""
        # Skip if not authenticated
        if not custom_pages_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Skip if there are no distributions available
        distributions = custom_pages_service.retrieve_all_client_code_distributions()
        if (
            "distributions" not in distributions
            or len(distributions["distributions"]) == 0
        ):
            pytest.skip("No client code distributions available to test with")

        # Get the first distribution name
        distribution_name = distributions["distributions"][0]["name"]

        # Call the method
        result = custom_pages_service.retrieve_client_code_distribution(
            distribution_name
        )

        # Verify the response structure
        assert result["responseStatus"] == "SUCCESS"
        assert result["name"] == distribution_name
        assert "checksum" in result
        assert "size" in result

    def test_download_client_code_distribution(
        self, custom_pages_service, vault_config
    ):
        """Test download_client_code_distribution with real API"""
        # Skip if not authenticated
        if not custom_pages_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Skip if there are no distributions available
        distributions = custom_pages_service.retrieve_all_client_code_distributions()
        if (
            "distributions" not in distributions
            or len(distributions["distributions"]) == 0
        ):
            pytest.skip("No client code distributions available to test with")

        # Get the first distribution name
        distribution_name = distributions["distributions"][0]["name"]

        # Call the method
        response = custom_pages_service.download_client_code_distribution(
            distribution_name
        )

        # Verify the response
        assert response.status_code == 200
        assert response.content  # Should have some content
        assert "application/zip" in response.headers.get("Content-Type", "")

    @pytest.mark.skip(
        reason="This test would create actual data in Vault and is not safe to run automatically"
    )
    def test_upload_client_code_distribution(self, custom_pages_service, vault_config):
        """Test upload_client_code_distribution with real API"""
        # This test is skipped as it would create actual data in Vault
        pass

    @pytest.mark.skip(
        reason="This test would delete actual data in Vault and is not safe to run automatically"
    )
    def test_delete_client_code_distribution(self, custom_pages_service, vault_config):
        """Test delete_client_code_distribution with real API"""
        # This test is skipped as it would delete actual data in Vault
        pass
