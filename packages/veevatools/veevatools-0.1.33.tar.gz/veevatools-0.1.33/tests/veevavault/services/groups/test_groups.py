from pytest import mark, fixture, skip
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.groups import GroupsService


@mark.unit
@mark.veevavault
class TestGroupsServiceUnit:
    """
    Unit tests for GroupsService class using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_group_metadata(
        self, mock_request, authenticated_vault_client, mock_group_data
    ):
        """Test retrieve_group_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "name__v": {"type": "string", "required": True},
                "label__v": {"type": "string", "required": True},
                "group_description__v": {"type": "string", "required": False},
                "active__v": {"type": "boolean", "required": True},
                "allow_delegation_among_members__v": {
                    "type": "boolean",
                    "required": False,
                },
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test
        result = groups_service.retrieve_group_metadata()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/objects/groups")
        assert kwargs["method"] == "GET"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "name__v" in result["properties"]
        assert "label__v" in result["properties"]

    @patch("requests.request")
    def test_retrieve_all_groups(
        self, mock_request, authenticated_vault_client, mock_group_data
    ):
        """Test retrieve_all_groups method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_group_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test
        result = groups_service.retrieve_all_groups()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/groups")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert "includeImplied" not in kwargs["params"]

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "groups" in result
        assert len(result["groups"]) == 2
        assert result["groups"][0]["id"] == 123
        assert result["groups"][1]["id"] == 456

    @patch("requests.request")
    def test_retrieve_all_groups_with_implied(
        self, mock_request, authenticated_vault_client, mock_group_data
    ):
        """Test retrieve_all_groups method with include_implied=True"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_group_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with include_implied=True
        result = groups_service.retrieve_all_groups(include_implied=True)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/groups")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert kwargs["params"].get("includeImplied") == "true"

    @patch("requests.request")
    def test_retrieve_auto_managed_groups(
        self, mock_request, authenticated_vault_client
    ):
        """Test retrieve_auto_managed_groups method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "groups": [
                {
                    "id": 789,
                    "name__v": "auto_managed_group_1",
                    "label__v": "Auto Managed Group 1",
                    "active__v": True,
                    "members__v": [3001, 3002],
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test
        result = groups_service.retrieve_auto_managed_groups(limit=500, offset=10)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/groups/auto")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert kwargs["params"].get("limit") == 500
        assert kwargs["params"].get("offset") == 10

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "groups" in result
        assert len(result["groups"]) == 1
        assert result["groups"][0]["id"] == 789

    @patch("requests.request")
    def test_retrieve_group(
        self, mock_request, authenticated_vault_client, mock_group_data
    ):
        """Test retrieve_group method"""
        # Set up mock response for a single group
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "group": mock_group_data["groups"][0],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test
        group_id = 123
        result = groups_service.retrieve_group(group_id)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert "includeImplied" not in kwargs["params"]

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "group" in result
        assert result["group"]["id"] == group_id
        assert result["group"]["name__v"] == "test_group_1"

    @patch("requests.request")
    def test_retrieve_group_with_implied(
        self, mock_request, authenticated_vault_client, mock_group_data
    ):
        """Test retrieve_group method with include_implied=True"""
        # Set up mock response for a single group
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "group": mock_group_data["groups"][0],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with include_implied=True
        group_id = 123
        result = groups_service.retrieve_group(group_id, include_implied=True)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "GET"
        assert "params" in kwargs
        assert kwargs["params"].get("includeImplied") == "true"

    @patch("requests.request")
    def test_create_group(self, mock_request, authenticated_vault_client):
        """Test create_group method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": 123,
            "name__v": "test_group_1",
            "url": "/api/v25.1/objects/groups/123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with all parameters
        result = groups_service.create_group(
            label="Test Group 1",
            members=[1001, 1002, 1003],
            security_profiles=["Standard"],
            active=True,
            description="This is a test group",
            allow_delegation_among_members=False,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/groups")
        assert kwargs["method"] == "POST"
        assert "data" in kwargs

        # Check data parameters
        data = kwargs["data"]
        assert data["label__v"] == "Test Group 1"
        assert data["members__v"] == "1001,1002,1003"
        assert data["security_profiles__v"] == "Standard"
        assert "active__v" not in data  # Default is True, so not included
        assert data["group_description__v"] == "This is a test group"
        assert "allow_delegation_among_members__v" not in data  # Default is False

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 123

    @patch("requests.request")
    def test_create_group_minimal(self, mock_request, authenticated_vault_client):
        """Test create_group method with minimal parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "id": 456,
            "name__v": "test_group_2",
            "url": "/api/v25.1/objects/groups/456",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with minimal parameters (only label is required)
        result = groups_service.create_group(label="Test Group 2")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/groups")
        assert kwargs["method"] == "POST"
        assert "data" in kwargs

        # Check data parameters - should only have label
        data = kwargs["data"]
        assert data == {"label__v": "Test Group 2"}

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == 456

    @patch("requests.request")
    def test_update_group(self, mock_request, authenticated_vault_client):
        """Test update_group method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with all parameters
        group_id = 123
        result = groups_service.update_group(
            group_id=group_id,
            label="Updated Group Name",
            members=[1001, 1002, 1003],
            security_profiles=["Standard"],
            active=True,
            description="Updated description",
            allow_delegation_among_members=True,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "PUT"
        assert "data" in kwargs

        # Check data parameters
        data = kwargs["data"]
        assert data["label__v"] == "Updated Group Name"
        assert data["members__v"] == "1001,1002,1003"
        assert data["security_profiles__v"] == "Standard"
        assert data["active__v"] == "true"
        assert data["group_description__v"] == "Updated description"
        assert data["allow_delegation_among_members__v"] == "true"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == group_id

    @patch("requests.request")
    def test_update_group_with_add_members(
        self, mock_request, authenticated_vault_client
    ):
        """Test update_group method with adding members"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with add members operation
        group_id = 123
        result = groups_service.update_group(
            group_id=group_id,
            members=["add", 1001, 1002],  # Special format for adding members
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "PUT"
        assert "data" in kwargs

        # Check data parameters - should use special format for members
        data = kwargs["data"]
        assert data["members__v"] == "add (1001,1002)"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == group_id

    @patch("requests.request")
    def test_update_group_with_delete_members(
        self, mock_request, authenticated_vault_client
    ):
        """Test update_group method with deleting members"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test with delete members operation
        group_id = 123
        result = groups_service.update_group(
            group_id=group_id,
            members=["delete", 2001, 2002],  # Special format for deleting members
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "PUT"
        assert "data" in kwargs

        # Check data parameters - should use special format for members
        data = kwargs["data"]
        assert data["members__v"] == "delete (2001,2002)"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == group_id

    @patch("requests.request")
    def test_delete_group(self, mock_request, authenticated_vault_client):
        """Test delete_group method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS", "id": 123}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create service with mocked client
        groups_service = GroupsService(authenticated_vault_client)

        # Call method to test
        group_id = 123
        result = groups_service.delete_group(group_id)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(f"/api/v25.1/objects/groups/{group_id}")
        assert kwargs["method"] == "DELETE"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["id"] == group_id


@mark.integration
@mark.veevavault
class TestGroupsServiceIntegration:
    """
    Integration tests for GroupsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_group_metadata(self, groups_service, vault_config):
        """Test retrieve_group_metadata with real API"""
        # Skip if running in mock mode or no credentials
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Call the API method
        response = groups_service.retrieve_group_metadata()

        # Verify the response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "properties" in response

    def test_retrieve_all_groups(self, groups_service, vault_config):
        """Test retrieve_all_groups with real API"""
        # Skip if running in mock mode or no credentials
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Call the API method
        response = groups_service.retrieve_all_groups()

        # Verify the response structure
        assert response["responseStatus"] == "SUCCESS"
        # Note: The response may or may not contain groups depending on the vault

    def test_retrieve_auto_managed_groups(self, groups_service, vault_config):
        """Test retrieve_auto_managed_groups with real API"""
        # Skip if running in mock mode or no credentials
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Skip test - needs a vault with Dynamic Access Control enabled
        pytest.skip("This test requires a vault with Dynamic Access Control enabled")

        # If test is not skipped, call the API method
        # response = groups_service.retrieve_auto_managed_groups()
        # assert response["responseStatus"] == "SUCCESS"

    def test_retrieve_group(self, groups_service, vault_config):
        """Test retrieve_group with real API"""
        # Skip if running in mock mode or no credentials
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Skip test - need a specific group ID to test with
        pytest.skip("This test requires a known group ID to test with")

        # If test is not skipped, call the API method with a real group ID
        # group_id = 123  # Replace with a real group ID
        # response = groups_service.retrieve_group(group_id)
        # assert response["responseStatus"] == "SUCCESS"
        # assert "group" in response
        # assert response["group"]["id"] == group_id

    def test_create_update_delete_group_flow(self, groups_service, vault_config):
        """Test the entire group lifecycle (create, update, delete) with real API"""
        # Skip if running in mock mode or no credentials
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")

        # Skip test - modifying data in production systems needs careful consideration
        pytest.skip(
            "This test would modify data in the vault and is disabled for safety"
        )

        # If test is not skipped, perform the following steps:
        # 1. Create a test group
        # 2. Verify creation
        # 3. Update the group
        # 4. Verify update
        # 5. Delete the group
        # 6. Verify deletion
