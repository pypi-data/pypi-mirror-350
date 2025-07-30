from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.roles_service import ObjectRolesService


@mark.unit
@mark.veevavault
class TestObjectRolesServiceUnit:
    """
    Unit tests for ObjectRolesService
    """

    @patch("requests.request")
    def test_retrieve_object_record_roles(self, mock_request):
        """Test retrieve_object_record_roles method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "roles": [
                {
                    "name": "owner__v",
                    "label": "Owner",
                    "assignment_type": "manual_assignment",
                    "users": [{"id": "user123", "name": "Test User"}],
                    "groups": [],
                },
                {
                    "name": "viewer__v",
                    "label": "Viewer",
                    "assignment_type": "manual_assignment",
                    "users": [],
                    "groups": [{"id": "group456", "name": "Test Group"}],
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        roles_service = ObjectRolesService(client)

        # Call method to test
        result = roles_service.retrieve_object_record_roles("contact__v", "12345")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/contact__v/12345/roles")
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["roles"]) == 2
        assert result["roles"][0]["name"] == "owner__v"
        assert len(result["roles"][0]["users"]) == 1
        assert result["roles"][1]["name"] == "viewer__v"
        assert len(result["roles"][1]["groups"]) == 1

    @patch("requests.request")
    def test_retrieve_specific_object_role(self, mock_request):
        """Test retrieve_object_record_roles with specific role"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "role": {
                "name": "owner__v",
                "label": "Owner",
                "assignment_type": "manual_assignment",
                "users": [{"id": "user123", "name": "Test User"}],
                "groups": [],
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        roles_service = ObjectRolesService(client)

        # Call method to test with specific role
        result = roles_service.retrieve_object_record_roles(
            "contact__v", "12345", "owner__v"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/vobjects/contact__v/12345/roles/owner__v"
        )
        assert kwargs["method"] == "GET"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["role"]["name"] == "owner__v"
        assert len(result["role"]["users"]) == 1

    @patch("requests.request")
    def test_assign_users_groups_to_roles(self, mock_request):
        """Test assign_users_groups_to_roles_on_object_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully assigned users and groups to roles",
            "data": [{"responseStatus": "SUCCESS", "id": "12345"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        roles_service = ObjectRolesService(client)

        # Test payload
        payload = {
            "records": [
                {
                    "id": "12345",
                    "owner__v": {"users": ["user123"], "groups": []},
                    "viewer__v": {"users": [], "groups": ["group456"]},
                }
            ]
        }

        # Call method to test
        result = roles_service.assign_users_groups_to_roles_on_object_records(
            "contact__v", payload
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/contact__v/roles")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert json.loads(kwargs["data"]) == payload

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "12345"

    @patch("requests.request")
    def test_remove_users_groups_from_roles(self, mock_request):
        """Test remove_users_groups_from_roles_on_object_records method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Successfully removed users and groups from roles",
            "data": [{"responseStatus": "SUCCESS", "id": "12345"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        roles_service = ObjectRolesService(client)

        # Test payload
        payload = {
            "records": [
                {"id": "12345", "owner__v": {"users": ["user123"], "groups": []}}
            ]
        }

        # Call method to test
        result = roles_service.remove_users_groups_from_roles_on_object_records(
            "contact__v", payload
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/vobjects/contact__v/roles")
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert json.loads(kwargs["data"]) == payload

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == "12345"


@mark.integration
@mark.veevavault
class TestObjectRolesServiceIntegration:
    """
    Integration tests for ObjectRolesService using real API calls
    """

    def test_retrieve_object_record_roles(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving roles for an object record"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        roles_service = ObjectRolesService(authenticated_vault_client)

        # Skip actual API call in this template
        pytest.skip("Integration test requires a valid object record ID")
