from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderTemplatesService


@mark.unit
@mark.veevavault
class TestBinderTemplatesServiceUnit:
    """
    Unit tests for BinderTemplatesService using mocks
    """

    def test_retrieve_binder_template_metadata(self):
        """Test retrieving metadata which defines the shape of binder templates"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "properties": {
                    "name__v": {
                        "type": "String",
                        "requiredness": "true",
                        "editable": "false",
                        "multi_value": "false",
                    },
                    "label__v": {
                        "type": "String",
                        "requiredness": "true",
                        "editable": "true",
                        "multi_value": "false",
                    },
                    "active__v": {
                        "type": "Boolean",
                        "requiredness": "true",
                        "editable": "true",
                        "multi_value": "false",
                    },
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
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.retrieve_binder_template_metadata()

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/metadata/objects/binders/templates"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert "properties" in result
            assert "name__v" in result["properties"]
            assert "label__v" in result["properties"]
            assert "active__v" in result["properties"]

    def test_retrieve_binder_template_node_metadata(self):
        """Test retrieving metadata which defines the shape of binder template nodes"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "properties": {
                    "id": {
                        "type": "ID",
                        "requiredness": "true",
                        "editable": "true",
                        "multi_value": "false",
                    },
                    "parent_id__v": {
                        "type": "ID",
                        "requiredness": "false",
                        "editable": "true",
                        "multi_value": "false",
                    },
                    "node_type__v": {
                        "type": "Enum",
                        "requiredness": "true",
                        "editable": "true",
                        "multi_value": "false",
                    },
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
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.retrieve_binder_template_node_metadata()

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/metadata/objects/binders/templates/bindernodes"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert "properties" in result
            assert "id" in result["properties"]
            assert "parent_id__v" in result["properties"]
            assert "node_type__v" in result["properties"]

    def test_retrieve_binder_template_collection(self):
        """Test retrieving the collection of all binder templates"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "templates": [
                    {
                        "name__v": "ectd_binder_template__v",
                        "label__v": "eCTD Binder Template",
                        "active__v": "true",
                        "type__v": "regulatory_submission__v",
                        "subtype__v": "ectd__v",
                        "classification__v": "unclassified__v",
                    },
                    {
                        "name__v": "clinical_trial_binder_template__v",
                        "label__v": "Clinical Trial Binder Template",
                        "active__v": "true",
                        "type__v": "clinical_trial__v",
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
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.retrieve_binder_template_collection()

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert "templates" in result
            assert len(result["templates"]) == 2
            assert result["templates"][0]["name__v"] == "ectd_binder_template__v"
            assert (
                result["templates"][1]["name__v"] == "clinical_trial_binder_template__v"
            )

    def test_retrieve_binder_template_attributes(self):
        """Test retrieving attributes of a specific binder template"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "template": {
                    "name__v": "ectd_binder_template__v",
                    "label__v": "eCTD Binder Template",
                    "active__v": "true",
                    "type__v": "regulatory_submission__v",
                    "subtype__v": "ectd__v",
                    "classification__v": "unclassified__v",
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
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.retrieve_binder_template_attributes(
                "ectd_binder_template__v"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates/ectd_binder_template__v"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert "template" in result
            assert result["template"]["name__v"] == "ectd_binder_template__v"
            assert result["template"]["label__v"] == "eCTD Binder Template"

    def test_retrieve_binder_template_node_attributes(self):
        """Test retrieving attributes of each node of a binder template"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "nodes": [
                    {
                        "id": "node_001",
                        "parent_id__v": "",
                        "node_type__v": "section",
                        "label__v": "Module 1",
                        "number__v": "1.0",
                        "order__v": 0,
                    },
                    {
                        "id": "node_002",
                        "parent_id__v": "node_001",
                        "node_type__v": "planned_document",
                        "label__v": "Cover Letter",
                        "order__v": 0,
                        "type__v": "regulatory_submission__v",
                        "subtype__v": "cover_letter__v",
                        "lifecycle__v": "general_lifecycle__v",
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
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.retrieve_binder_template_node_attributes(
                "ectd_binder_template__v"
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates/ectd_binder_template__v/bindernodes"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert "nodes" in result
            assert len(result["nodes"]) == 2
            assert result["nodes"][0]["node_type__v"] == "section"
            assert result["nodes"][1]["node_type__v"] == "planned_document"

    def test_create_binder_template(self):
        """Test creating a new binder template"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "name__v": "new_template__v",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.create_binder_template(
                label_v="New Template",
                type_v="regulatory_submission__v",
                active_v=True,
                name_v="new_template__v",
                subtype_v="form__v",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Content-Type"] == "application/json"

            # Parse the JSON data
            data = json.loads(kwargs["data"])
            assert data["label__v"] == "New Template"
            assert data["type__v"] == "regulatory_submission__v"
            assert data["active__v"] == "true"
            assert data["name__v"] == "new_template__v"
            assert data["subtype__v"] == "form__v"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["name__v"] == "new_template__v"

    def test_bulk_create_binder_templates(self):
        """Test bulk creating binder templates"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "data": [
                    {"name__v": "template1__v", "responseStatus": "SUCCESS"},
                    {"name__v": "template2__v", "responseStatus": "SUCCESS"},
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
            templates_service = BinderTemplatesService(client)

            # Test CSV data
            csv_data = """name__v,label__v,type__v,active__v
template1__v,Template 1,regulatory_submission__v,true
template2__v,Template 2,regulatory_submission__v,true"""

            # Call method to test
            result = templates_service.bulk_create_binder_templates(csv_data)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Content-Type"] == "text/csv"
            assert kwargs["data"] == csv_data

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["data"]) == 2
            assert result["data"][0]["name__v"] == "template1__v"
            assert result["data"][1]["name__v"] == "template2__v"

    def test_delete_binder_template(self):
        """Test deleting an existing binder template"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"responseStatus": "SUCCESS"}
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            templates_service = BinderTemplatesService(client)

            # Call method to test
            result = templates_service.delete_binder_template("template_to_delete__v")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/templates/template_to_delete__v"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestBinderTemplatesServiceIntegration:
    """
    Integration tests for BinderTemplatesService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_binder_template_metadata(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving binder template metadata with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        templates_service = BinderTemplatesService(authenticated_vault_client)

        # Call method to test - this is a read-only operation so should be safe
        result = templates_service.retrieve_binder_template_metadata()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result

    def test_retrieve_binder_template_node_metadata(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving binder template node metadata with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        templates_service = BinderTemplatesService(authenticated_vault_client)

        # Call method to test - this is a read-only operation so should be safe
        result = templates_service.retrieve_binder_template_node_metadata()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result

    def test_retrieve_binder_template_collection(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving binder template collection with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        templates_service = BinderTemplatesService(authenticated_vault_client)

        # Call method to test - this is a read-only operation so should be safe
        result = templates_service.retrieve_binder_template_collection()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        # There may be no templates, so just check the key exists
        assert "templates" in result

    def test_create_and_delete_operations(
        self, authenticated_vault_client, vault_config
    ):
        """Test creating and deleting operations with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        templates_service = BinderTemplatesService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip("Skipping to prevent modifying data in production")
