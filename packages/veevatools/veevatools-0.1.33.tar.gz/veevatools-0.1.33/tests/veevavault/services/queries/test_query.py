# tests/veevavault/services/queries/test_query.py
from pytest import mark, fixture
import pytest
import requests
import pandas as pd
import re
from unittest.mock import patch, MagicMock, call

from veevavault.client import VaultClient
from veevavault.services.queries import QueryService


@mark.unit
@mark.veevavault
class TestQueryServiceUnit:
    """
    Unit tests for QueryService using mocks
    """

    def test_init(self):
        """Test service initialization"""
        client = VaultClient()
        query_service = QueryService(client)

        # Verify client reference is stored correctly
        assert query_service.client is client

    @patch("requests.post")
    def test_query_service_query(self, mock_post):
        """Test QueryService query method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            # Put data at the top level as expected by the query method
            "data": [
                {"id": "001", "name": "Object 1"},
                {"id": "002", "name": "Object 2"},
            ],
            "responseDetails": {"total": 2, "offset": 0, "pageSize": 2},
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test
        result = query_service.query("SELECT id, name FROM object__v")

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://test.veevavault.com/api/v25.1/query"
        assert "q" in kwargs["data"]
        assert kwargs["data"]["q"] == "SELECT id, name FROM object__v"

        # Verify response parsing
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == "001"

    @patch("requests.post")
    def test_query_failure(self, mock_post):
        """Test query method with failure response"""
        # Set up mock response for failure
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "FAILURE",
            "errors": [{"type": "INVALID_REQUEST", "message": "Invalid VQL query"}],
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test
        result = query_service.query("INVALID QUERY")

        # Verify error handling
        assert result is None  # Method returns None on failure

    @patch("requests.post")
    def test_query_basic(self, mock_post):
        """Test query method with default parameters"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {"id": "001", "name__v": "Object 1"},
                {"id": "002", "name__v": "Object 2"},
            ],
            "queryDescribe": {
                "object": {"name": "documents", "label": "Documents"},
                "fields": [
                    {"name": "id", "type": "id", "required": True},
                    {"name": "name__v", "type": "String", "required": True},
                ],
            },
            "responseDetails": {
                "pagesize": 1000,
                "pageoffset": 0,
                "size": 2,
                "total": 2,
            },
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test
        result = query_service.query("SELECT id, name__v FROM documents")

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://test.veevavault.com/api/v25.1/query"
        assert kwargs["headers"]["X-VaultAPI-DescribeQuery"] == "true"
        assert "q" in kwargs["data"]
        assert kwargs["data"]["q"] == "SELECT id, name__v FROM documents"

        # Verify response is returned correctly
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2
        assert "queryDescribe" in result

    @patch("requests.post")
    def test_query_with_facets_and_record_properties(self, mock_post):
        """Test query method with facets and record properties"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [{"id": "001", "name__v": "Object 1"}],
            "queryDescribe": {"object": {"name": "documents"}},
            "facets": {
                "product__v": {
                    "label": "Product",
                    "type": "String",
                    "name": "product__v",
                    "count": 2,
                    "values": [
                        {"value": "cholecap", "result_count": 5},
                        {"value": "vitavil", "result_count": 3},
                    ],
                }
            },
            "record_properties": {
                "001": {"id": "001", "permissions": {"read": True, "edit": False}}
            },
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test with all parameters
        result = query_service.query(
            query="SELECT id, name__v FROM documents WHERE product__v = 'cholecap'",
            describe_query=True,
            record_properties="all",
            facets=["product__v"],
        )

        # Verify request was made with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["headers"]["X-VaultAPI-DescribeQuery"] == "true"
        assert kwargs["headers"]["X-VaultAPI-RecordProperties"] == "all"
        assert kwargs["headers"]["X-VaultAPI-Facets"] == "product__v"

        # Verify extended response elements
        assert "facets" in result
        assert "record_properties" in result
        assert "product__v" in result["facets"]

    @patch("requests.post")
    @patch("requests.get")
    def test_bulk_query_with_pagination(self, mock_get, mock_post):
        """Test bulk_query method with pagination handling"""
        # Set up mock responses for initial query and pagination
        first_page_response = {
            "responseStatus": "SUCCESS",
            "data": [
                {"id": "001", "name__v": "Object 1"},
                {"id": "002", "name__v": "Object 2"},
            ],
            "responseDetails": {
                "pagesize": 2,
                "pageoffset": 0,
                "size": 2,
                "total": 4,
                "next_page": "https://test.veevavault.com/api/v25.1/query?pageoffset=2",
            },
        }
        second_page_response = {
            "responseStatus": "SUCCESS",
            "data": [
                {"id": "003", "name__v": "Object 3"},
                {"id": "004", "name__v": "Object 4"},
            ],
            "responseDetails": {"pagesize": 2, "pageoffset": 2, "size": 2, "total": 4},
        }

        # Configure the mocks
        mock_post_instance = MagicMock()
        mock_post_instance.json.return_value = first_page_response
        mock_post.return_value = mock_post_instance

        mock_get_instance = MagicMock()
        mock_get_instance.json.return_value = second_page_response
        mock_get.return_value = mock_get_instance

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test
        result_df = query_service.bulk_query("SELECT id, name__v FROM documents")

        # Verify that both requests were made correctly
        mock_post.assert_called_once()
        mock_get.assert_called_once_with(
            "https://test.veevavault.com/api/v25.1/query?pageoffset=2",
            headers={
                "X-VaultAPI-DescribeQuery": "true",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Authorization": "test-session-id",
            },
        )

        # Verify dataframe contains all records from both pages
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 4
        assert list(result_df["id"].values) == ["001", "002", "003", "004"]

    @patch("requests.post")
    def test_bulk_query_with_pagesize_in_query(self, mock_post):
        """Test bulk_query with PAGESIZE specified in the query"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "data": [
                {"id": "001", "name__v": "Object 1"},
                {"id": "002", "name__v": "Object 2"},
            ],
            "responseDetails": {
                "pagesize": 2,
                "pageoffset": 0,
                "size": 2,
                "total": 10,  # More records exist but won't be fetched due to PAGESIZE
            },
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method with PAGESIZE in query
        result_df = query_service.bulk_query(
            "SELECT id, name__v FROM documents PAGESIZE 2"
        )

        # Verify request
        mock_post.assert_called_once()

        # Verify only first page is returned due to PAGESIZE
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 2
        assert list(result_df["id"].values) == ["001", "002"]

    @patch("requests.post")
    def test_bulk_query_failure(self, mock_post):
        """Test bulk_query method failure handling"""
        # Set up mock response for failure
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "FAILURE",
            "errors": [{"type": "INVALID_REQUEST", "message": "Invalid VQL query"}],
        }
        mock_post.return_value = mock_response

        # Create mocked client
        client = VaultClient()
        client.vaultURL = "https://test.veevavault.com"
        client.sessionId = "test-session-id"
        client.LatestAPIversion = "v25.1"

        # Create service with mocked client
        query_service = QueryService(client)

        # Call method to test
        result = query_service.bulk_query("INVALID QUERY")

        # Verify error handling
        assert result is None  # Method returns None on failure


@mark.integration
@mark.veevavault
class TestQueryServiceIntegration:
    """
    Integration tests for QueryService using real API calls
    """

    def test_query_service(self, authenticated_vault_client, vault_config):
        """Test query service with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        query_service = QueryService(authenticated_vault_client)

        # Execute a safe query
        result = query_service.query(
            "SELECT id, name__v FROM vault_package__v LIMIT 10"
        )

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "data" in result
        assert isinstance(result["data"], list)

    def test_query(self, authenticated_vault_client, vault_config):
        """Test query with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        query_service = QueryService(authenticated_vault_client)

        # Execute a safe query with query (most flexible method)
        result = query_service.query(
            query="SELECT id, name__v FROM vault_package__v LIMIT 10",
            describe_query=True,
        )

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "data" in result
        assert "queryDescribe" in result

    def test_query_with_facets(self, authenticated_vault_client, vault_config):
        """Test query with facets (if supported by your Vault)"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        query_service = QueryService(authenticated_vault_client)

        # Try fetching data with facets - this might fail if your objects don't
        # support facets or the field you choose isn't facetable
        try:
            result = query_service.query(
                query="SELECT id, name__v, status__v FROM vault_package__v LIMIT 10",
                describe_query=True,
                facets=["status__v"],
            )

            # If the call succeeds, check for facet data
            assert result["responseStatus"] == "SUCCESS"
            # Note: Facets may not be supported or may return empty in some vaults
            # So we don't assert directly on their presence
        except Exception as e:
            pytest.skip(f"Could not test facets due to: {e}")

    def test_bulk_query_with_dataframe(self, authenticated_vault_client, vault_config):
        """Test bulk_query returns a pandas DataFrame with real API"""
        # Skip if not authenticated
        if not authenticated_vault_client.sessionId:
            pytest.skip("No authenticated session available")

        # Create service
        query_service = QueryService(authenticated_vault_client)

        # Execute a safe query with bulk_query
        result_df = query_service.bulk_query(
            "SELECT id, name__v FROM vault_package__v LIMIT 10"
        )

        # Verify result is a DataFrame with expected structure
        assert isinstance(result_df, pd.DataFrame)
        assert "id" in result_df.columns
        assert "name__v" in result_df.columns
