from pytest import mark, fixture
import pytest
from unittest.mock import MagicMock

from veevavault.services.scim.scim import SCIMService


@mark.unit
@mark.veevavault
class TestSCIMServiceUnit:
    """
    Unit tests for SCIMService class using mocks
    """

    @fixture(autouse=True)
    def service(self):
        # Setup a mock client for SCIMService
        client = MagicMock()
        client.LatestAPIversion = "v25.1"
        return SCIMService(client)

    def test_retrieve_scim_provider(self, service):
        dummy = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"]
        }
        service.client.api_call.return_value = dummy

        result = service.retrieve_scim_provider()

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/ServiceProviderConfig"
        )
        assert result == dummy

    def test_retrieve_all_scim_schemas(self, service):
        dummy = {"Resources": [], "totalResults": 0}
        service.client.api_call.return_value = dummy

        result = service.retrieve_all_scim_schemas()

        service.client.api_call.assert_called_once_with("api/v25.1/scim/v2/Schemas")
        assert result == dummy

    def test_retrieve_single_scim_schema(self, service):
        schema_id = "urn:ietf:params:scim:schemas:core:2.0:User"
        dummy = {"id": schema_id, "attributes": []}
        service.client.api_call.return_value = dummy

        result = service.retrieve_single_scim_schema(schema_id)

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/Schemas/{schema_id}"
        )
        assert result == dummy

    def test_retrieve_all_resource_types(self, service):
        dummy = {"Resources": [], "totalResults": 0}
        service.client.api_call.return_value = dummy

        result = service.retrieve_all_scim_resource_types()

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/ResourceTypes"
        )
        assert result == dummy

    def test_retrieve_single_resource_type(self, service):
        resource = "User"
        dummy = {"id": resource, "endpoint": "/Users"}
        service.client.api_call.return_value = dummy

        result = service.retrieve_single_scim_resource_type(resource)

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/ResourceTypes/{resource}"
        )
        assert result == dummy

    def test_retrieve_all_users_defaults(self, service):
        dummy = {"Resources": [], "totalResults": 0}
        service.client.api_call.return_value = dummy

        result = service.retrieve_all_users()

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/Users",
            params={
                "sortOrder": "ascending",
                "count": 1000,
                "startIndex": 1,
            },
        )
        assert result == dummy

    def test_retrieve_users_with_filters(self, service):
        filters = {
            "filter": 'userName eq "john"',
            "attributes": "userName,emails",
            "excludedAttributes": "meta",
            "sortBy": "displayName",
            "sortOrder": "descending",
            "count": 50,
            "startIndex": 5,
        }
        dummy = {"Resources": []}
        service.client.api_call.return_value = dummy

        result = service.retrieve_all_users(
            filter=filters["filter"],
            attributes=filters["attributes"],
            excluded_attributes=filters["excludedAttributes"],
            sort_by=filters["sortBy"],
            sort_order=filters["sortOrder"],
            count=filters["count"],
            start_index=filters["startIndex"],
        )

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/Users", params=filters
        )
        assert result == dummy

    def test_retrieve_single_user(self, service):
        user_id = "12345"
        dummy = {"id": user_id}
        service.client.api_call.return_value = dummy

        result = service.retrieve_single_user(user_id, excluded_attributes="meta")

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/Users/{user_id}",
            params={"excludedAttributes": "meta"},
        )
        assert result == dummy

    def test_retrieve_current_user(self, service):
        dummy = {"id": "me"}
        service.client.api_call.return_value = dummy

        result = service.retrieve_current_user(attributes="emails")

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/Me",
            params={"attributes": "emails"},
        )
        assert result == dummy

    def test_update_current_user(self, service):
        payload = {"name": {"givenName": "Alice"}}
        dummy = {"id": "me", "name": {"givenName": "Alice"}}
        service.client.api_call.return_value = dummy

        result = service.update_current_user(payload, excluded_attributes="meta")

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/Me",
            method="PUT",
            json=payload,
            params={"excludedAttributes": "meta"},
        )
        assert result == dummy

    def test_create_user(self, service):
        user_data = {"schemas": [], "userName": "user@test.com"}
        dummy = {"id": "newid123"}
        service.client.api_call.return_value = dummy

        result = service.create_user(user_data)

        service.client.api_call.assert_called_once_with(
            "api/v25.1/scim/v2/Users",
            method="POST",
            json=user_data,
            headers={"Content-Type": "application/scim+json"},
        )
        assert result == dummy

    def test_update_user(self, service):
        user_id = "abcde"
        update = {"active": False}
        dummy = {"id": user_id, "active": False}
        service.client.api_call.return_value = dummy

        result = service.update_user(user_id, update)

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/Users/{user_id}",
            method="PUT",
            json=update,
            headers={"Content-Type": "application/scim+json"},
        )
        assert result == dummy

    def test_retrieve_scim_resources_defaults(self, service):
        resource = "Groups"
        dummy = {"Resources": []}
        service.client.api_call.return_value = dummy

        result = service.retrieve_scim_resources(resource)

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/{resource}",
            params={"sortOrder": "ascending", "count": 1000, "startIndex": 1},
        )
        assert result == dummy

    def test_retrieve_single_scim_resource(self, service):
        resource = "Groups"
        res_id = "g123"
        dummy = {"id": res_id}
        service.client.api_call.return_value = dummy

        result = service.retrieve_single_scim_resource(
            resource, res_id, attributes="emails"
        )

        service.client.api_call.assert_called_once_with(
            f"api/v25.1/scim/v2/{resource}/{res_id}",
            params={"attributes": "emails"},
        )
        assert result == dummy


@mark.integration
@mark.veevavault
class TestSCIMServiceIntegration:
    """
    Integration tests for SCIMService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture(autouse=True)
    def service(self, authenticated_vault_client, vault_config):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        return SCIMService(authenticated_vault_client)

    def test_retrieve_scim_provider_integration(self, service):
        response = service.retrieve_scim_provider()
        assert isinstance(response, dict)
        assert "schemas" in response or "documentationUri" in response

    def test_retrieve_all_scim_schemas_integration(self, service):
        response = service.retrieve_all_scim_schemas()
        assert isinstance(response, dict)
        assert "Resources" in response

    def test_retrieve_all_users_integration(self, service):
        response = service.retrieve_all_users(count=1)
        assert isinstance(response, dict)
        assert "Resources" in response

    def test_update_current_user_integration(self, service):
        pytest.skip("State-changing SCIM operations not safe for integration tests")

    def test_create_user_integration(self, service):
        pytest.skip("User creation not supported in integration environment")

    def test_update_user_integration(self, service):
        pytest.skip("User update not supported in integration environment")
