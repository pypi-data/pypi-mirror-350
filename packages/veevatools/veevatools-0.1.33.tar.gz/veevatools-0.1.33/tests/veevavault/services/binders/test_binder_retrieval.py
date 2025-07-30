from pytest import mark, fixture
import pytest
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.binders import BinderRetrievalService


@fixture
def mock_binder_response():
    """Fixture providing mock binder response data"""
    return {
        "responseStatus": "SUCCESS",
        "document": {
            "id": "123",
            "name__v": "Test Binder",
            "type__v": "compliance_binder__v",
            "binder__v": True,
            "major_version_number__v": 1,
            "minor_version_number__v": 0,
        },
        "binder": {
            "nodes": [
                {
                    "id": "node_001",
                    "parent_id__v": None,
                    "type__v": "section",
                    "order__v": 0,
                    "name__v": "Section 1",
                    "section_number__v": "1.0",
                },
                {
                    "id": "node_002",
                    "parent_id__v": "node_001",
                    "type__v": "document",
                    "order__v": 0,
                    "name__v": "Document 1",
                    "document_id__v": "doc_123",
                },
            ]
        },
    }


@mark.unit
@mark.veevavault
class TestBinderRetrievalServiceUnit:
    """
    Unit tests for BinderRetrievalService using mocks
    """

    def test_retrieve_all_binders(self):
        """Test retrieving all binders in the vault"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "size": 2,
                "start": 0,
                "limit": 200,
                "documents": [
                    {
                        "document": {
                            "id": "101",
                            "binder__v": True,
                            "name__v": "CholeCap Presentation",
                        }
                    },
                    {
                        "document": {
                            "id": "102",
                            "binder__v": True,
                            "name__v": "Regulatory Submission",
                        }
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
            retrieval_service = BinderRetrievalService(client)

            # Call method to test
            result = retrieval_service.retrieve_all_binders()

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/documents"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["documents"]) == 2
            assert result["documents"][0]["document"]["binder__v"] == True

    def test_retrieve_binder(self, mock_binder_response):
        """Test retrieving details of a specific binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_binder_response
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            retrieval_service = BinderRetrievalService(client)

            # Call method to test
            result = retrieval_service.retrieve_binder("123")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["document"]["id"] == "123"
            assert result["document"]["binder__v"] == True
            assert len(result["binder"]["nodes"]) == 2

    def test_retrieve_binder_with_depth(self, mock_binder_response):
        """Test retrieving details of a specific binder with depth parameter"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_binder_response
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            retrieval_service = BinderRetrievalService(client)

            # Call method to test with depth parameter
            result = retrieval_service.retrieve_binder("123", depth="all")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123"
            )
            assert kwargs["params"]["depth"] == "all"

            # Verify response
            assert result["responseStatus"] == "SUCCESS"

    def test_retrieve_all_binder_versions(self):
        """Test retrieving all versions of a specific binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "responseStatus": "SUCCESS",
                "versions": [
                    {
                        "number": "0.1",
                        "value": "https://vault-domain.veevavault.com/api/v25.1/objects/binders/29/versions/0/1",
                    },
                    {
                        "number": "0.2",
                        "value": "https://vault-domain.veevavault.com/api/v25.1/objects/binders/29/versions/0/2",
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
            retrieval_service = BinderRetrievalService(client)

            # Call method to test
            result = retrieval_service.retrieve_all_binder_versions("29")

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/29/versions"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert len(result["versions"]) == 2
            assert result["versions"][0]["number"] == "0.1"
            assert result["versions"][1]["number"] == "0.2"

    def test_retrieve_binder_version(self, mock_binder_response):
        """Test retrieving a specific version of a binder"""
        # Set up mock response
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_binder_response
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            # Create client with basic configuration
            client = VaultClient()
            client.vaultURL = "https://test.veevavault.com"
            client.sessionId = "test-session-id"
            client.LatestAPIversion = "v25.1"

            # Create service with mocked client
            retrieval_service = BinderRetrievalService(client)

            # Call method to test
            result = retrieval_service.retrieve_binder_version("123", 1, 0)

            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert (
                kwargs["url"]
                == "https://test.veevavault.com/api/v25.1/objects/binders/123/versions/1/0"
            )

            # Verify response
            assert result["responseStatus"] == "SUCCESS"
            assert result["document"]["major_version_number__v"] == 1
            assert result["document"]["minor_version_number__v"] == 0


@mark.integration
@mark.veevavault
class TestBinderRetrievalServiceIntegration:
    """
    Integration tests for BinderRetrievalService using real API calls
    These tests will be skipped if no credentials are available
    """

    def test_retrieve_all_binders(self, authenticated_vault_client, vault_config):
        """Test retrieving all binders with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        retrieval_service = BinderRetrievalService(authenticated_vault_client)

        # Call method to test - this is a read-only operation so should be safe
        result = retrieval_service.retrieve_all_binders()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "documents" in result

    def test_retrieve_binder(self, authenticated_vault_client, vault_config):
        """Test retrieving a specific binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        retrieval_service = BinderRetrievalService(authenticated_vault_client)

        # Skip - requires existing binder ID
        pytest.skip("This test requires an existing binder ID to be configured")

        # # Call method with a real binder ID
        # result = retrieval_service.retrieve_binder("actual_binder_id")
        #
        # # Verify response contains expected keys
        # assert result["responseStatus"] == "SUCCESS"
        # assert "document" in result
        # assert "binder" in result

    def test_retrieve_all_binder_versions(
        self, authenticated_vault_client, vault_config
    ):
        """Test retrieving all versions of a binder with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        retrieval_service = BinderRetrievalService(authenticated_vault_client)

        # Skip - requires existing binder ID
        pytest.skip("This test requires an existing binder ID to be configured")
