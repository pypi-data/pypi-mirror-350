from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderRolesService


@mark.unit
@mark.veevavault
class TestBinderRolesServiceUnit:
    """
    Unit tests for BinderRolesService using mocks
    """

    def test_retrieve_binder_roles(self):
        """Test retrieving all available roles on a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "roles": [
                    {
                        "name": "reviewer__v",
                        "label": "Reviewer",
                        "assignedUsers": [1234, 5678],
                        "assignedGroups": [9012],
                        "availableUsers": [1234, 5678, 8901],
                        "availableGroups": [9012, 3456],
                        "defaultUsers": [1234],
                        "defaultGroups": [],
                    },
                    {
                        "name": "owner__v",
                        "label": "Owner",
                        "assignedUsers": [5678],
                        "assignedGroups": [],
                        "availableUsers": [1234, 5678, 8901],
                        "availableGroups": [9012, 3456],
                        "defaultUsers": [5678],
                        "defaultGroups": [],
                    },
                ],
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            roles_service = BinderRolesService(client)

            # Call method to test
            result = roles_service.retrieve_binder_roles("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/roles"
            )
            assert kwargs["headers"]["Accept"] == "application/json"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["roles"]) == 2
            assert result["roles"][0]["name"] == "reviewer__v"
            assert result["roles"][1]["name"] == "owner__v"

    def test_retrieve_specific_binder_role(self):
        """Test retrieving a specific role on a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "roles": [
                    {
                        "name": "reviewer__v",
                        "label": "Reviewer",
                        "assignedUsers": [1234, 5678],
                        "assignedGroups": [9012],
                        "availableUsers": [1234, 5678, 8901],
                        "availableGroups": [9012, 3456],
                        "defaultUsers": [1234],
                        "defaultGroups": [],
                    }
                ],
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            roles_service = BinderRolesService(client)

            # Call method to test with specific role name
            result = roles_service.retrieve_binder_roles("123", "reviewer__v")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/roles/reviewer__v"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["roles"]) == 1
            assert result["roles"][0]["name"] == "reviewer__v"

    def test_assign_users_groups_to_binder_roles(self):
        """Test assigning users and groups to roles on a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "Roles updated",
                "updatedRoles": {
                    "reviewer__v": {
                        "users": [12021, 12022],
                        "groups": [3311303, 3311404],
                    }
                },
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            roles_service = BinderRolesService(client)

            # Test data
            role_assignments = {
                "reviewer__v.users": "12021,12022",
                "reviewer__v.groups": "3311303,3311404",
            }

            # Call method to test
            result = roles_service.assign_users_groups_to_binder_roles(
                "123", role_assignments
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/roles"
            )
            assert kwargs["method"] == "POST"
            assert (
                kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
            )
            assert kwargs["data"] == role_assignments

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["responseMessage"] == "Roles updated"
            assert "reviewer__v" in result["updatedRoles"]
            assert result["updatedRoles"]["reviewer__v"]["users"] == [12021, 12022]
            assert result["updatedRoles"]["reviewer__v"]["groups"] == [3311303, 3311404]

    def test_remove_user_from_binder_role(self):
        """Test removing a user from a role on a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "responseMessage": "User/group deleted from role",
                "updatedRoles": {"consumer__v": {"users": [1008313]}},
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            roles_service = BinderRolesService(client)

            # Call method to test
            result = roles_service.remove_user_group_from_binder_role(
                binder_id="123",
                role_name_and_user_or_group="consumer__v.user",
                id_value="1008313",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/roles/consumer__v.user/1008313"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["responseMessage"] == "User/group deleted from role"
            assert "consumer__v" in result["updatedRoles"]
            assert result["updatedRoles"]["consumer__v"]["users"] == [1008313]


@mark.integration
@mark.veevavault
class TestBinderRolesServiceIntegration:
    """
    Integration tests for BinderRolesService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_binder_roles(self, authenticated_vault_client, vault_config):
        """Test retrieving binder roles with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        roles_service = BinderRolesService(authenticated_vault_client)

        # Skip - requires existing binder ID
        pytest.skip("This test requires an existing binder ID to be configured")

        # # Call method with a real binder ID
        # result = roles_service.retrieve_binder_roles("actual_binder_id")
        #
        # # Verify response contains expected keys
        # assert result["responseStatus"] == "SUCCESS"
        # assert "roles" in result

    def test_assign_and_remove_users(self, authenticated_vault_client, vault_config):
        """Test assigning and removing users from binder roles with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        roles_service = BinderRolesService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder ID, roles, and user IDs."
        )
