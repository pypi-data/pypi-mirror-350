from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.documents.tokens_service import DocumentTokensService


@mark.unit
@mark.veevavault
class TestDocumentTokensServiceUnit:
    """
    Unit tests for DocumentTokensService using mocks (no real API calls)
    """

    @patch("requests.request")
    def test_create_tokens(self, mock_request):
        """Test create_tokens method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "tokens": [
                {
                    "document_id__v": 101,
                    "token__v": "3003-cb6e5c3b-4df9-411c-abc2-6e7ae120ede7",
                },
                {
                    "document_id__v": 102,
                    "token__v": "3003-1174154c-ac8e-4eb9-b453-2855de273bec",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTokensService(client)

        # Call method to test with single doc ID as string
        result = service.create_tokens(
            "101,102", expiry_date_offset=30, download_option="PDF"
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/tokens")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"]["docIds"] == "101,102"
        assert kwargs["data"]["expiryDateOffset"] == 30
        assert kwargs["data"]["downloadOption"] == "PDF"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "tokens" in result
        assert len(result["tokens"]) == 2
        assert result["tokens"][0]["document_id__v"] == 101
        assert result["tokens"][1]["document_id__v"] == 102
        assert "token__v" in result["tokens"][0]
        assert "token__v" in result["tokens"][1]

    @patch("requests.request")
    def test_create_tokens_with_list(self, mock_request):
        """Test create_tokens method with list of document IDs"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "tokens": [
                {
                    "document_id__v": 101,
                    "token__v": "3003-cb6e5c3b-4df9-411c-abc2-6e7ae120ede7",
                },
                {
                    "document_id__v": 102,
                    "token__v": "3003-1174154c-ac8e-4eb9-b453-2855de273bec",
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Create client and service
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        service = DocumentTokensService(client)

        # Call method to test with list of doc IDs
        result = service.create_tokens(
            ["101", "102"],
            expiry_date_offset=30,
            download_option="PDF",
            channel="web_channel_1",
            token_group="document_group_1",
            steady_state=True,
        )

        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"].endswith("/api/v25.1/objects/documents/tokens")
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert kwargs["data"]["docIds"] == "101,102"
        assert kwargs["data"]["expiryDateOffset"] == 30
        assert kwargs["data"]["downloadOption"] == "PDF"
        assert kwargs["data"]["channel"] == "web_channel_1"
        assert kwargs["data"]["tokenGroup"] == "document_group_1"
        assert kwargs["data"]["steadyState"] == "true"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert "tokens" in result
        assert len(result["tokens"]) == 2


@mark.integration
@mark.veevavault
class TestDocumentTokensServiceIntegration:
    """
    Integration tests for DocumentTokensService using real API calls
    """

    def test_document_tokens_service(self, authenticated_vault_client):
        """Test basic tokens service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        service = DocumentTokensService(authenticated_vault_client)

        # Just verify the service is instantiated properly
        assert service is not None
        assert service.client is authenticated_vault_client

    @pytest.mark.skip(
        reason="Creating tokens requires specific document IDs and permissions"
    )
    def test_create_tokens_integration(self, authenticated_vault_client):
        """Test creating document tokens with real API"""
        # This test requires specific document IDs to work
        pass
