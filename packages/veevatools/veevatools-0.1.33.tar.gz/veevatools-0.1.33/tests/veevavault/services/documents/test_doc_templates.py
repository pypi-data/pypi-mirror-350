from pytest import mark, fixture
import pytest
import requests
import json
import os
from unittest.mock import patch, MagicMock, mock_open

from veevavault.client import VaultClient
from veevavault.services.documents.templates_service import DocumentTemplatesService


@mark.unit
@mark.veevavault
class TestDocumentTemplatesServiceUnit:
    """
    Unit tests for DocumentTemplatesService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_get_template_metadata(self, mock_request):
        """Test get_template_metadata method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "properties": {
                "name__v": {"type": "string", "label": "Name"},
                "label__v": {"type": "string", "label": "Label"},
                "type__v": {"type": "picklist", "label": "Type"},
                "active__v": {"type": "boolean", "label": "Active"},
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        result = service.get_template_metadata()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/metadata/objects/documents/templates")
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        assert "name__v" in result["properties"]
        assert "label__v" in result["properties"]
        assert "type__v" in result["properties"]
        assert "active__v" in result["properties"]

    @patch("requests.request")
    def test_get_templates(self, mock_request):
        """Test get_templates method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "templates": [
                {
                    "name__v": "template_1",
                    "label__v": "Template 1",
                    "type__v": "document_type_1__v",
                    "active__v": True,
                },
                {
                    "name__v": "template_2",
                    "label__v": "Template 2",
                    "type__v": "document_type_2__v",
                    "active__v": False,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        result = service.get_templates()

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/templates")
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "templates" in result
        assert len(result["templates"]) == 2
        assert result["templates"][0]["name__v"] == "template_1"
        assert result["templates"][1]["name__v"] == "template_2"

    @patch("requests.request")
    def test_get_template(self, mock_request):
        """Test get_template method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "template": {
                "name__v": "template_1",
                "label__v": "Template 1",
                "type__v": "document_type_1__v",
                "active__v": True,
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        result = service.get_template("template_1")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/templates/template_1"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "template" in result
        assert result["template"]["name__v"] == "template_1"
        assert result["template"]["label__v"] == "Template 1"

    @patch("requests.request")
    def test_download_template_file(self, mock_request):
        """Test download_template_file method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.content = b"template file content"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        result = service.download_template_file("template_1")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/templates/template_1/file"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["raw_response"] == True

        # Verify response
        assert result == b"template file content"

    @patch("requests.request")
    def test_create_template(self, mock_request):
        """Test create_template method with placeholder template"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "name__v": "template_new",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        template_data = {
            "label__v": "New Template",
            "type__v": "document_type_1__v",
            "active__v": True,
        }
        result = service.create_template(template_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/templates")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert json.loads(kwargs["data"]) == template_data

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["name__v"] == "template_new"

    @patch("requests.request")
    def test_update_template(self, mock_request):
        """Test update_template method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        update_data = {"label__v": "Updated Template", "active__v": False}
        result = service.update_template("template_1", update_data)

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/templates/template_1"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["data"] == update_data

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_delete_template(self, mock_request):
        """Test delete_template method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"responseStatus": "SUCCESS"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTemplatesService(client)

        # Call method to test
        result = service.delete_template("template_1")

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith(
            "/api/v25.1/objects/documents/templates/template_1"
        )
        assert kwargs["method"] == "DELETE"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestDocumentTemplatesServiceIntegration:
    """
    Integration tests for DocumentTemplatesService using real API calls
    """

    def test_document_templates_service(self, authenticated_vault_client):
        """Test basic templates service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentTemplatesService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    def test_get_template_metadata_integration(self, authenticated_vault_client):
        """Test retrieving template metadata with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentTemplatesService(authenticated_vault_client)

        # Call method to test
        result = service.get_template_metadata()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "properties" in result
        # Should have standard template fields
        assert "name__v" in result["properties"]
        assert "label__v" in result["properties"]
        assert "type__v" in result["properties"]
        assert "active__v" in result["properties"]
