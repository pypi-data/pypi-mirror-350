from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.roles_service import DocumentRolesService


@mark.unit
@mark.veevavault
class TestDocumentRolesServiceUnit:
    """
    Unit tests for DocumentRolesService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_retrieve_document_roles(self, mock_request):
        """Test retrieve_document_roles method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "roles": [
                {
                    "name": "reviewer__v",
                    "label": "Reviewer",
                    "assignedUsers": [12021],
                    "assignedGroups": [3311303],
                    "availableUsers": [12021, 12022],
                    "availableGroups": [3311303, 3311404],
                },
                {
                    "name": "owner__v",
                    "label": "Owner",
                    "assignedUsers": [12022],
                    "assignedGroups": [],
                    "availableUsers": [12021, 12022],
                    "availableGroups": [3311303, 3311404],
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRolesService(client)

        # Call method to test
        result = service.retrieve_document_roles("123")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/roles")
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "roles" in result
        assert len(result["roles"]) == 2
        assert result["roles"][0]["name"] == "reviewer__v"
        assert result["roles"][1]["name"] == "owner__v"
        assert 12021 in result["roles"][0]["assignedUsers"]
        assert 3311303 in result["roles"][0]["assignedGroups"]

    @patch("requests.request")
    def test_assign_users_groups_to_document_roles(self, mock_request):
        """Test assign_users_groups_to_document_roles method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "Document roles updated",
            "updatedRoles": {
                "reviewer__v": {"users": [12021, 12022], "groups": [3311303, 3311404]}
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRolesService(client)

        # Call method to test
        role_assignments = {
            "reviewer__v.users": "12021,12022",
            "reviewer__v.groups": "3311303,3311404",
        }
        result = service.assign_users_groups_to_document_roles("123", role_assignments)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/123/roles")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"] == role_assignments

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseMessage"] == "Document roles updated"
        assert "updatedRoles" in result
        assert "reviewer__v" in result["updatedRoles"]
        assert len(result["updatedRoles"]["reviewer__v"]["users"]) == 2
        assert len(result["updatedRoles"]["reviewer__v"]["groups"]) == 2

    @patch("requests.request")
    def test_remove_user_group_from_document_role(self, mock_request):
        """Test remove_user_group_from_document_role method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "responseMessage": "User/group deleted from document role",
            "updatedRoles": {"consumer__v": {"users": [1008313]}},
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentRolesService(client)

        # Call method to test
        result = service.remove_user_group_from_document_role(
            "123", "consumer__v.user", "1008313"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/123/roles/consumer__v.user/1008313"
        )
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["responseMessage"] == "User/group deleted from document role"
        assert "updatedRoles" in result
        assert "consumer__v" in result["updatedRoles"]
        assert 1008313 in result["updatedRoles"]["consumer__v"]["users"]


@mark.integration
@mark.veevavault
class TestDocumentRolesServiceIntegration:
    """
    Integration tests for DocumentRolesService using real API calls
    """

    def test_document_roles_service(self, authenticated_vault_client):
        """Test basic roles service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentRolesService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Requires document to test and might modify document roles"
    )
    def test_retrieve_document_roles_integration(self, authenticated_vault_client):
        """Test retrieving document roles with real API"""
        pass
