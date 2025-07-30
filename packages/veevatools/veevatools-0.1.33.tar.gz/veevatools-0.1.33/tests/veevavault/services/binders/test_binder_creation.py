from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderCreationService


@mark.unit
@mark.veevavault
class TestBinderCreationServiceUnit:
    """
    Unit tests for BinderCreationService using mocks
    """

    def test_create_binder(self):
        """Test creating a new binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "563",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            creation_service = BinderCreationService(client)

            # Test data
            binder_data = {
                "name__v": "Test Binder",
                "type__v": "compliance_binder__v",
                "subtype__v": "labeling__v",
                "lifecycle__v": "compliance_binder_lifecycle__v",
            }

            # Call method to test
            result = creation_service.create_binder(binder_data)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"] == "https://test.veevavault.com/api/v25.1/objects/binders"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == binder_data

            # Verify response
            assert result == {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "563",
            }

    def test_create_binder_with_async_indexing(self):
        """Test creating a new binder with async indexing"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "564",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            creation_service = BinderCreationService(client)

            # Test data
            binder_data = {
                "name__v": "Test Binder Async",
                "type__v": "compliance_binder__v",
                "subtype__v": "labeling__v",
                "lifecycle__v": "compliance_binder_lifecycle__v",
            }

            # Call method to test with async_indexing=True
            result = creation_service.create_binder(binder_data, async_indexing=True)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"] == "https://test.veevavault.com/api/v25.1/objects/binders"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["params"] == {"async": "true"}
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == binder_data

            # Verify response
            assert result == {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "564",
            }

    def test_create_binder_from_template(self):
        """Test creating a new binder from a template"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "565",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            creation_service = BinderCreationService(client)

            # Test data
            template_name = "ectd_compliance_package_template__v"
            binder_data = {
                "name__v": "Test Binder From Template",
                "type__v": "compliance_binder__v",
                "subtype__v": "labeling__v",
                "lifecycle__v": "compliance_binder_lifecycle__v",
            }

            # Call method to test
            result = creation_service.create_binder_from_template(
                template_name, binder_data
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"] == "https://test.veevavault.com/api/v25.1/objects/binders"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )

            # Verify the template name was added to the data
            assert "fromTemplate" in kwargs["data"]
            assert kwargs["data"]["fromTemplate"] == template_name

            # Verify response
            assert result == {
                "responseStatus": "SUCCESS",
                "responseMessage": "Successfully created binder.",
                "id": "565",
            }

    def test_create_binder_version(self):
        """Test creating a new version of an existing binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "New draft successfully created",
                "major_version_number__v": 0,
                "minor_version_number__v": 4,
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            creation_service = BinderCreationService(client)

            # Call method to test
            result = creation_service.create_binder_version("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Accept"] == "application/json"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["responseMessage"] == "New draft successfully created"
            assert result["major_version_number__v"] == 0
            assert result["minor_version_number__v"] == 4


@mark.integration
@mark.veevavault
class TestBinderCreationServiceIntegration:
    """
    Integration tests for BinderCreationService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_create_binder(self, authenticated_vault_client, vault_config):
        """Test creating a new binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        creation_service = BinderCreationService(authenticated_vault_client)

        # Skip - would create actual data
        pytest.skip("Skipping to prevent creating data in production")

        # # Create test data - adjust for your Vault's document types and lifecycles
        # binder_data = {
        #     "name__v": f"Test Binder {datetime.now().strftime('%Y%m%d%H%M%S')}",
        #     "type__v": "YOUR_BINDER_TYPE",
        #     "lifecycle__v": "YOUR_LIFECYCLE"
        # }
        #
        # # Call method to test
        # result = creation_service.create_binder(binder_data)
        #
        # # Verify response
        # assert result["responseStatus"] == "SUCCESS"
        # assert "id" in result

    def test_create_binder_from_template(
        self, authenticated_vault_client, vault_config
    ):
        """Test creating a new binder from a template with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        creation_service = BinderCreationService(authenticated_vault_client)

        # Skip - would create actual data and requires template knowledge
        pytest.skip(
            "Skipping to prevent creating data in production and requires template configuration"
        )

    def test_create_binder_version(self, authenticated_vault_client, vault_config):
        """Test creating a new version of an existing binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        creation_service = BinderCreationService(authenticated_vault_client)

        # Skip - would create actual data and requires existing binder
        pytest.skip(
            "Skipping to prevent creating data in production and requires existing binder ID"
        )
