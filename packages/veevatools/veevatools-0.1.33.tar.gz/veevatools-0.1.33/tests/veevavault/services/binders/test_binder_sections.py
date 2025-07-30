from pytest import mark, fixture
import pytest
import json
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderSectionsService


@mark.unit
@mark.veevavault
class TestBinderSectionsServiceUnit:
    """
    Unit tests for BinderSectionsService using mocks
    """

    def test_retrieve_binder_sections(self):
        """Test retrieving sections of a binder from the top-level root node"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "binder": {
                    "nodes": [
                        {
                            "id": "section_001",
                            "parent_id__v": None,
                            "type__v": "section",
                            "order__v": 0,
                            "name__v": "Section 1",
                            "section_number__v": "1.0",
                        },
                        {
                            "id": "section_002",
                            "parent_id__v": None,
                            "type__v": "section",
                            "order__v": 1,
                            "name__v": "Section 2",
                            "section_number__v": "2.0",
                        },
                    ]
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
            sections_service = BinderSectionsService(client)

            # Call method to test
            result = sections_service.retrieve_binder_sections("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["binder"]["nodes"]) == 2
            assert result["binder"]["nodes"][0]["name__v"] == "Section 1"
            assert result["binder"]["nodes"][1]["name__v"] == "Section 2"

    def test_retrieve_specific_binder_section(self):
        """Test retrieving a specific section of a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "binder": {
                    "nodes": [
                        {
                            "id": "doc_001",
                            "parent_id__v": "section_001",
                            "type__v": "document",
                            "order__v": 0,
                            "name__v": "Document 1",
                            "document_id__v": "123",
                        },
                        {
                            "id": "section_003",
                            "parent_id__v": "section_001",
                            "type__v": "section",
                            "order__v": 1,
                            "name__v": "Subsection 1.1",
                            "section_number__v": "1.1",
                        },
                    ]
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
            sections_service = BinderSectionsService(client)

            # Call method to test with specific section ID
            result = sections_service.retrieve_binder_sections("123", "section_001")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections/section_001"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["binder"]["nodes"]) == 2
            assert result["binder"]["nodes"][0]["type__v"] == "document"
            assert result["binder"]["nodes"][1]["type__v"] == "section"

    def test_retrieve_binder_version_section(self):
        """Test retrieving sections of a specific binder version"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "binder": {
                    "nodes": [
                        {
                            "id": "section_001",
                            "parent_id__v": None,
                            "type__v": "section",
                            "order__v": 0,
                            "name__v": "Section 1",
                            "section_number__v": "1.0",
                        }
                    ]
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
            sections_service = BinderSectionsService(client)

            # Call method to test with version
            result = sections_service.retrieve_binder_version_section("123", 1, 0)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/versions/1/0/sections"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["binder"]["nodes"]) == 1

    def test_create_binder_section(self):
        """Test creating a new section in a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "section_new_001",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            sections_service = BinderSectionsService(client)

            # Call method to test
            result = sections_service.create_binder_section(
                binder_id="123",
                name="New Section",
                section_number="3.0",
                parent_id=None,
                order=2,
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections"
            )
            assert kwargs["method"] == "POST"
            assert kwargs["headers"]["Content-Type"] == "application/json"

            # Parse the JSON data
            data = json.loads(kwargs["data"])
            assert data["name__v"] == "New Section"
            assert data["section_number__v"] == "3.0"
            assert data["order__v"] == 2

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "section_new_001"

    def test_update_binder_section(self):
        """Test updating a binder section"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "section_001",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            sections_service = BinderSectionsService(client)

            # Call method to test
            result = sections_service.update_binder_section(
                binder_id="123",
                node_id="section_001",
                name="Updated Section Name",
                section_number="1.5",
                order=1,
                parent_id="section_002",
            )

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections/section_001"
            )
            assert kwargs["method"] == "PUT"
            assert kwargs["headers"]["Content-Type"] == "application/json"

            # Parse the JSON data
            data = json.loads(kwargs["data"])
            assert data["name__v"] == "Updated Section Name"
            assert data["section_number__v"] == "1.5"
            assert data["order__v"] == 1
            assert data["parent_id__v"] == "section_002"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "section_001"

    def test_delete_binder_section(self):
        """Test deleting a section from a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "id": "section_001",
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            sections_service = BinderSectionsService(client)

            # Call method to test
            result = sections_service.delete_binder_section("123", "section_001")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/sections/section_001"
            )
            assert kwargs["method"] == "DELETE"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["id"] == "section_001"


@mark.integration
@mark.veevavault
class TestBinderSectionsServiceIntegration:
    """
    Integration tests for BinderSectionsService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_binder_sections(self, authenticated_vault_client, vault_config):
        """Test retrieving binder sections with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        sections_service = BinderSectionsService(authenticated_vault_client)

        # Skip - requires existing binder ID
        pytest.skip("This test requires an existing binder ID to be configured")

        # # Call method with a real binder ID
        # result = sections_service.retrieve_binder_sections("actual_binder_id")
        #
        # # Verify response structure
        # assert result["responseStatus"] == "SUCCESS"
        # assert "binder" in result
        # assert "nodes" in result["binder"]

    def test_create_update_delete_binder_section(
        self, authenticated_vault_client, vault_config
    ):
        """Test creating, updating, and deleting a binder section with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        sections_service = BinderSectionsService(authenticated_vault_client)

        # Skip - would modify actual data
        pytest.skip(
            "Skipping to prevent modifying data in production. Requires existing binder ID."
        )
