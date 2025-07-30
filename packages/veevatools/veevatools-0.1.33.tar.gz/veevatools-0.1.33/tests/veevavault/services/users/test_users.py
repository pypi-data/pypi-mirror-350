from pytest import mark, skip
import pytest
from unittest.mock import patch

from veevavault.client import VaultClient
from veevavault.services.users.users import UserService


@mark.unit
@mark.veevavault
class TestUserServiceUnit:
    def setup_method(self):
        # Initialize a VaultClient and UserService for testing
        self.client = VaultClient()
        self.client.vaultURL = "https://test.veevavault.com"
        self.client.sessionId = "test-session-id"
        self.service = UserService(self.client)

    @patch.object(VaultClient, "api_call")
    def test_retrieve_user_metadata(self, mock_api_call):
        expected = {"fields": ["id", "user_name__v"]}
        mock_api_call.return_value = expected

        result = self.service.retrieve_user_metadata()

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/metadata/objects/users"
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_retrieve_all_users_default(self, mock_api_call):
        expected = {"users": []}
        mock_api_call.return_value = expected

        result = self.service.retrieve_all_users()

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            params={
                "exclude_vault_membership": "true",
                "exclude_app_licensing": "true",
                "limit": 200,
                "start": 0,
                "sort": "id asc",
            },
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_retrieve_all_users_with_vaults_list(self, mock_api_call):
        expected = {"users": []}
        mock_api_call.return_value = expected

        result = self.service.retrieve_all_users(
            vaults=["100", "200"],
            exclude_vault_membership=False,
            exclude_app_licensing=False,
            limit=50,
            start=5,
            sort="name desc",
        )

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            params={
                "exclude_vault_membership": "false",
                "exclude_app_licensing": "false",
                "limit": 50,
                "start": 5,
                "sort": "name desc",
                "vaults": "100,200",
            },
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_retrieve_user(self, mock_api_call):
        expected = {"user": {"id": "1"}}
        mock_api_call.return_value = expected

        result = self.service.retrieve_user(
            1, exclude_vault_membership=False, exclude_app_licensing=False
        )

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1",
            params={
                "exclude_vault_membership": "false",
                "exclude_app_licensing": "false",
            },
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_create_user_default(self, mock_api_call):
        user_data = {"user_name__v": "newuser"}
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.create_user(user_data)

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            method="POST",
            data=user_data,
            params={},
            files=None,
        )
        assert result == expected

    def test_create_user_with_profile_image(self):
        # File upload handling not testable in unit tests
        pytest.skip("File upload handling not testable in unit tests")

    @patch.object(VaultClient, "api_call")
    def test_create_multiple_users_json(self, mock_api_call):
        users = [{"user_name__v": "u1"}, {"user_name__v": "u2"}]
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.create_multiple_users(users)

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            method="POST",
            json=users,
            params={},
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_create_multiple_users_csv(self, mock_api_call):
        csv_data = "id,user_name__v\n1,u1"
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.create_multiple_users(
            csv_data, operation="upsert", id_param="user_name__v"
        )

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            method="POST",
            data=csv_data,
            params={"operation": "upsert", "idParam": "user_name__v"},
            headers={"Content-Type": "text/csv"},
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_update_user(self, mock_api_call):
        update_data = {"user_first_name__v": "Test"}
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.update_user("1", update_data)

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1",
            method="PUT",
            data=update_data,
        )
        assert result == expected

    @patch.object(UserService, "update_user")
    def test_update_my_user(self, mock_update):
        mock_update.return_value = {"responseStatus": "SUCCESS"}

        result = self.service.update_my_user({"key": "value"})

        mock_update.assert_called_once_with("me", {"key": "value"})
        assert result == {"responseStatus": "SUCCESS"}

    @patch.object(VaultClient, "api_call")
    def test_update_multiple_users_json(self, mock_api_call):
        users = [{"id": "1", "user_last_name__v": "Last"}]
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.update_multiple_users(users)

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users",
            method="PUT",
            json=users,
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_update_multiple_users_csv(self, mock_api_call):
        csv_data = "id,user_email__v\n1,test@example.com"
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.update_multiple_users(csv_data)

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1",
            method="PUT",
            data=csv_data,
            headers={"Content-Type": "text/csv"},
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_disable_user(self, mock_api_call):
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        # without domain
        self.service.disable_user("1")
        mock_api_call.assert_called_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1",
            method="DELETE",
            params={},
        )
        # with domain
        self.service.disable_user("1", domain=True)
        mock_api_call.assert_called_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1",
            method="DELETE",
            params={"domain": "true"},
        )

    @patch.object(VaultClient, "api_call")
    def test_change_my_password(self, mock_api_call):
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.change_my_password("oldp", "newp")

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/me/password",
            method="POST",
            data={"password__v": "oldp", "new_password__v": "newp"},
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_update_vault_membership(self, mock_api_call):
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.update_vault_membership(
            "1",
            "100",
            active=False,
            security_profile="profile__v",
            license_type="license__v",
        )

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1/vault_membership/100",
            method="PUT",
            data={
                "active__v": "false",
                "security_profile__v": "profile__v",
                "license_type__v": "license__v",
            },
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_retrieve_application_license_usage(self, mock_api_call):
        expected = {"doc_count": 10, "applications": []}
        mock_api_call.return_value = expected

        result = self.service.retrieve_application_license_usage()

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/licenses",
            method="GET",
        )
        assert result == expected

    @patch.object(VaultClient, "api_call")
    def test_retrieve_user_permissions(self, mock_api_call):
        expected = {"permissions": []}
        mock_api_call.return_value = expected

        # without filter
        self.service.retrieve_user_permissions("1")
        mock_api_call.assert_called_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1/permissions",
            method="GET",
            params={},
        )
        # with filter
        self.service.retrieve_user_permissions(
            "1", permission_name="object.Test.read_actions"
        )
        mock_api_call.assert_called_with(
            f"api/{self.client.LatestAPIversion}/objects/users/1/permissions",
            method="GET",
            params={"filter": "name__v::object.Test.read_actions"},
        )

    @patch.object(UserService, "retrieve_user_permissions")
    def test_retrieve_my_permissions(self, mock_retrieve):
        mock_retrieve.return_value = {"permissions": []}

        result = self.service.retrieve_my_permissions("object.Test.create_actions")
        mock_retrieve.assert_called_once_with("me", "object.Test.create_actions")
        assert result == {"permissions": []}

    @patch.object(VaultClient, "api_call")
    def test_validate_session_user(self, mock_api_call):
        expected = {"responseStatus": "SUCCESS"}
        mock_api_call.return_value = expected

        result = self.service.validate_session_user(
            exclude_vault_membership=False, exclude_app_licensing=False
        )

        mock_api_call.assert_called_once_with(
            f"api/{self.client.LatestAPIversion}/objects/users/me",
            method="GET",
            params={
                "exclude_vault_membership": "false",
                "exclude_app_licensing": "false",
            },
        )
        assert result == expected


@mark.integration
@mark.veevavault
class TestUserServiceIntegration:
    """
    Integration tests for UserService against real Vault API
    """

    def test_retrieve_user_metadata(self, authenticated_vault_client, vault_config):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.retrieve_user_metadata()
        assert isinstance(result, dict)

    def test_retrieve_all_users(self, authenticated_vault_client, vault_config):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.retrieve_all_users(limit=1)
        assert result.get("responseStatus") == "SUCCESS"
        assert isinstance(result, dict)

    def test_retrieve_user(self, authenticated_vault_client, vault_config):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.retrieve_user("me")
        assert result.get("responseStatus") == "SUCCESS"
        assert isinstance(result, dict)

    def test_retrieve_application_license_usage(
        self, authenticated_vault_client, vault_config
    ):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.retrieve_application_license_usage()
        assert result.get("responseStatus") == "SUCCESS"
        assert "applications" in result

    def test_retrieve_my_permissions(self, authenticated_vault_client, vault_config):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.retrieve_my_permissions()
        assert result.get("responseStatus") == "SUCCESS"

    def test_validate_session_user(self, authenticated_vault_client, vault_config):
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")
        service = UserService(authenticated_vault_client)
        result = service.validate_session_user()
        assert result.get("responseStatus") == "SUCCESS"
