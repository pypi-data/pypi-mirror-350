from pytest import mark, fixture, skip
import pytest
import json
import requests
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.mdl import MDLService


@mark.unit
@mark.veevavault
class TestMDLServiceUnit:
    """
    Unit tests for MDLService class using mocks (no real API calls)
    """

    @fixture
    def mock_client(self):
        """Setup mock client fixture"""
        client = MagicMock()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"
        return client

    @fixture
    def mdl_service(self, mock_client):
        """Setup MDLService with mock client"""
        return MDLService(mock_client)

    @patch("requests.post")
    def test_execute_mdl_script(self, mock_post, mdl_service):
        """Test execute_mdl_script method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "script_execution": {
                "code": "SUCCESS",
                "message": "MDL script executed successfully",
                "warnings": [],
                "failures": [],
                "exceptions": [],
                "components_affected": 2,
                "execution_time": 1034,
            },
            "statement_execution": [
                {
                    "statement": "CREATE PICKLIST color__c...",
                    "code": "SUCCESS",
                    "message": "Statement executed successfully",
                }
            ],
        }
        mock_post.return_value = mock_response

        # Test MDL script
        mdl_script = "CREATE PICKLIST color__c (RED, GREEN, BLUE)"

        # Call method
        result = mdl_service.execute_mdl_script(mdl_script)

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["url"] == "https://test.veevavault.com/api/mdl/execute"
        assert kwargs["headers"]["Authorization"] == "test-session-id"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["data"] == mdl_script

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["script_execution"]["code"] == "SUCCESS"
        assert len(result["statement_execution"]) == 1

    @patch("requests.post")
    def test_execute_mdl_script_async(self, mock_post, mdl_service):
        """Test execute_mdl_script_async method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "script_execution": {
                "code": "SUCCESS",
                "message": "MDL script queued for execution",
            },
            "job_id": 12345,
            "url": "https://test.veevavault.com/api/mdl/execute_async/12345/results",
        }
        mock_post.return_value = mock_response

        # Test MDL script
        mdl_script = "ALTER OBJECT contact__v ADD FIELD new_field__c TEXT"

        # Call method
        result = mdl_service.execute_mdl_script_async(mdl_script)

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["url"] == "https://test.veevavault.com/api/mdl/execute_async"
        assert kwargs["headers"]["Authorization"] == "test-session-id"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["data"] == mdl_script

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["script_execution"]["code"] == "SUCCESS"
        assert result["job_id"] == 12345
        assert "url" in result

    @patch("requests.get")
    def test_retrieve_async_mdl_script_results(self, mock_get, mdl_service):
        """Test retrieve_async_mdl_script_results method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "script_execution": {
                "code": "SUCCESS",
                "message": "MDL script executed successfully",
                "warnings": [],
                "failures": [],
                "exceptions": [],
                "components_affected": 1,
                "execution_time": 2345,
            },
            "statement_execution": [
                {
                    "statement": "ALTER OBJECT contact__v...",
                    "code": "SUCCESS",
                    "message": "Statement executed successfully",
                }
            ],
        }
        mock_get.return_value = mock_response

        # Call method with job ID
        job_id = 12345
        result = mdl_service.retrieve_async_mdl_script_results(job_id)

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/mdl/execute_async/12345/results"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["script_execution"]["code"] == "SUCCESS"
        assert len(result["statement_execution"]) == 1

    @patch("requests.post")
    def test_cancel_raw_object_deployment(self, mock_post, mdl_service):
        """Test cancel_raw_object_deployment method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Deployment cancelled successfully",
        }
        mock_post.return_value = mock_response

        # Call method
        object_name = "contact__v"
        result = mdl_service.cancel_raw_object_deployment(object_name)

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/v25.1/metadata/vobjects/contact__v/actions/canceldeployment"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.get")
    def test_retrieve_all_component_metadata(self, mock_get, mdl_service):
        """Test retrieve_all_component_metadata method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "components": [
                {
                    "url": "/api/v25.1/metadata/components/Picklist",
                    "name": "Picklist",
                    "class": "metadata",
                    "abbreviation": "PCL",
                    "label": "Picklist",
                    "label_plural": "Picklists",
                    "cacheable": True,
                    "cache_type_class": "vault.component.picklist.PicklistCache",
                    "vobject": None,
                },
                {
                    "url": "/api/v25.1/metadata/components/Object",
                    "name": "Object",
                    "class": "metadata",
                    "abbreviation": "OBJ",
                    "label": "Object",
                    "label_plural": "Objects",
                    "cacheable": True,
                    "cache_type_class": "vault.component.object.ObjectCache",
                    "vobject": "objects__v",
                },
            ],
        }
        mock_get.return_value = mock_response

        # Call method
        result = mdl_service.retrieve_all_component_metadata()

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"] == "https://test.veevavault.com/api/v25.1/metadata/components"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["components"]) == 2
        assert result["components"][0]["name"] == "Picklist"
        assert result["components"][1]["name"] == "Object"

    @patch("requests.get")
    def test_retrieve_component_type_metadata(self, mock_get, mdl_service):
        """Test retrieve_component_type_metadata method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "component": {
                "name": "Picklist",
                "class": "metadata",
                "abbreviation": "PCL",
                "active": True,
                "attributes": [
                    {"name": "name", "type": "STRING", "required": True},
                    {"name": "label", "type": "STRING", "required": True},
                    {"name": "shared", "type": "BOOLEAN", "required": False},
                ],
                "sub_components": [
                    {
                        "name": "PicklistValue",
                        "abbreviation": "PCLV",
                        "attributes": [
                            {"name": "value", "type": "STRING", "required": True},
                            {"name": "label", "type": "STRING", "required": True},
                            {"name": "active", "type": "BOOLEAN", "required": False},
                        ],
                    }
                ],
            },
        }
        mock_get.return_value = mock_response

        # Call method
        component_type = "Picklist"
        result = mdl_service.retrieve_component_type_metadata(component_type)

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/v25.1/metadata/components/Picklist"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["component"]["name"] == "Picklist"
        assert len(result["component"]["attributes"]) == 3
        assert len(result["component"]["sub_components"]) == 1

    @patch("requests.get")
    def test_retrieve_component_record_collection(self, mock_get, mdl_service):
        """Test retrieve_component_record_collection method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "components": [
                {
                    "name": "color__c",
                    "label": "Color",
                    "shared": True,
                    "values": [
                        {"value": "RED", "label": "Red", "active": True},
                        {"value": "GREEN", "label": "Green", "active": True},
                        {"value": "BLUE", "label": "Blue", "active": True},
                    ],
                },
                {
                    "name": "status__v",
                    "label": "Status",
                    "shared": True,
                    "values": [
                        {"value": "ACTIVE", "label": "Active", "active": True},
                        {"value": "INACTIVE", "label": "Inactive", "active": True},
                    ],
                },
            ],
        }
        mock_get.return_value = mock_response

        # Call method
        component_type = "Picklist"
        result = mdl_service.retrieve_component_record_collection(component_type)

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/v25.1/configuration/Picklist"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["components"]) == 2
        assert result["components"][0]["name"] == "color__c"
        assert len(result["components"][0]["values"]) == 3

    @patch("requests.get")
    def test_retrieve_component_record(self, mock_get, mdl_service):
        """Test retrieve_component_record method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "component": {
                "name": "color__c",
                "label": "Color",
                "shared": True,
                "values": [
                    {"value": "RED", "label": "Red", "active": True},
                    {"value": "GREEN", "label": "Green", "active": True},
                    {"value": "BLUE", "label": "Blue", "active": True},
                ],
            },
        }
        mock_get.return_value = mock_response

        # Call method without localization
        component_type_and_record_name = "Picklist.color__c"
        result = mdl_service.retrieve_component_record(component_type_and_record_name)

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/v25.1/configuration/Picklist.color__c"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["component"]["name"] == "color__c"
        assert len(result["component"]["values"]) == 3

        # Reset mock for second test
        mock_get.reset_mock()

        # Test with localization parameter
        mock_get.return_value = mock_response
        result = mdl_service.retrieve_component_record(
            component_type_and_record_name, loc=True
        )

        # Verify URL has loc parameter
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/v25.1/configuration/Picklist.color__c?loc=true"
        )

    @patch("requests.get")
    def test_retrieve_component_record_mdl(self, mock_get, mdl_service):
        """Test retrieve_component_record_mdl method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = (
            "RECREATE PICKLIST color__c (RED 'Red', GREEN 'Green', BLUE 'Blue');"
        )
        mock_get.return_value = mock_response

        # Call method
        component_type_and_record_name = "Picklist.color__c"
        result = mdl_service.retrieve_component_record_mdl(
            component_type_and_record_name
        )

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/mdl/components/Picklist.color__c"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert "RECREATE PICKLIST color__c" in result
        assert "RED 'Red'" in result

    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_upload_content_file(self, mock_file, mock_post, mdl_service):
        """Test upload_content_file method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "name__v": "test_file.pdf",
            "format__v": "pdf",
            "size__v": 16,
            "sha1_checksum__v": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
        }
        mock_post.return_value = mock_response

        # Call method
        file_path = "/path/to/test_file.pdf"
        result = mdl_service.upload_content_file(file_path)

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["url"] == "https://test.veevavault.com/api/mdl/files"
        assert kwargs["headers"]["Authorization"] == "test-session-id"
        assert "files" in kwargs

        # Verify file was opened correctly
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert result["name__v"] == "test_file.pdf"
        assert result["format__v"] == "pdf"
        assert result["size__v"] == 16

    @patch("requests.get")
    def test_retrieve_content_file(self, mock_get, mdl_service):
        """Test retrieve_content_file method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "links": [
                {
                    "rel": "self",
                    "href": "https://test.veevavault.com/api/mdl/components/Formattedoutput.my_output__c/files",
                    "method": "GET",
                    "accept": "application/json",
                },
                {
                    "rel": "content",
                    "href": "https://test.veevavault.com/api/mdl/components/Formattedoutput.my_output__c/files/content",
                    "method": "GET",
                    "accept": "application/octet-stream",
                },
            ],
            "data": {
                "name__v": "my_output_template.docx",
                "original_name__v": "template.docx",
                "format__v": "docx",
                "size__v": 24680,
                "sha1_checksum__v": "f1d2d2f924e986ac86fdf7b36c94bcdf32beec15",
            },
        }
        mock_get.return_value = mock_response

        # Call method
        component_type_and_record_name = "Formattedoutput.my_output__c"
        result = mdl_service.retrieve_content_file(component_type_and_record_name)

        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            kwargs["url"]
            == "https://test.veevavault.com/api/mdl/components/Formattedoutput.my_output__c/files"
        )
        assert kwargs["headers"]["Authorization"] == "test-session-id"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["links"]) == 2
        assert result["data"]["name__v"] == "my_output_template.docx"
        assert result["data"]["format__v"] == "docx"
        assert result["data"]["size__v"] == 24680


@mark.integration
@mark.veevavault
class TestMDLServiceIntegration:
    """
    Integration tests for MDLService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture(scope="function")
    def mdl_service(self, authenticated_vault_client):
        """Returns a MDLService instance using the authenticated Vault client"""
        return MDLService(authenticated_vault_client)

    def test_execute_mdl_script(self, mdl_service, vault_config):
        """Test executing an MDL script"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test involves executing MDL which could alter vault configuration
        # This could be dangerous in a production environment, so skipping for safety
        pytest.skip(
            "Skipping actual MDL execution to prevent altering vault configuration"
        )

    def test_retrieve_all_component_metadata(self, mdl_service, vault_config):
        """Test retrieving all component metadata"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This is a relatively safe read-only operation
        response = mdl_service.retrieve_all_component_metadata()

        # Basic validation of response
        assert response["responseStatus"] == "SUCCESS"
        assert "components" in response
        assert isinstance(response["components"], list)
        assert len(response["components"]) > 0

        # Verify a few expected component types exist
        component_names = [comp["name"] for comp in response["components"]]
        assert "Picklist" in component_names
        assert "Object" in component_names
        assert "Docfield" in component_names

    def test_retrieve_component_type_metadata(self, mdl_service, vault_config):
        """Test retrieving metadata for a specific component type"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Get metadata for Picklist component type
        response = mdl_service.retrieve_component_type_metadata("Picklist")

        # Basic validation of response
        assert response["responseStatus"] == "SUCCESS"
        assert "component" in response
        assert response["component"]["name"] == "Picklist"
        assert "attributes" in response["component"]
        assert "sub_components" in response["component"]

    def test_retrieve_component_record_collection(self, mdl_service, vault_config):
        """Test retrieving all records for a component type"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Get all records for Doctype component
        response = mdl_service.retrieve_component_record_collection("Doctype")

        # Basic validation of response
        assert response["responseStatus"] == "SUCCESS"
        assert "components" in response
        assert isinstance(response["components"], list)
        # There should be at least one doctype in any vault
        assert len(response["components"]) > 0

    def test_upload_content_file(self, mdl_service, vault_config):
        """Test uploading a content file"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need to create a temporary file to upload, which could alter vault
        # configuration, so skipping for safety
        pytest.skip("Skipping file upload test to prevent altering vault configuration")

    def test_retrieve_component_record(self, mdl_service, vault_config):
        """Test retrieving metadata for a specific component record"""
        # Skip if no authenticated session
        if not mdl_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # First, we need to find a valid component record to retrieve
        # Get all doctypes
        doc_types_response = mdl_service.retrieve_component_record_collection("Doctype")

        if (
            "components" not in doc_types_response
            or not doc_types_response["components"]
        ):
            pytest.skip("No Doctype components found to test with")

        # Get the first doctype's name
        doctype_name = doc_types_response["components"][0]["name"]

        # Now retrieve the specific component record
        response = mdl_service.retrieve_component_record(f"Doctype.{doctype_name}")

        # Basic validation of response
        assert response["responseStatus"] == "SUCCESS"
        assert "component" in response
        assert response["component"]["name"] == doctype_name
