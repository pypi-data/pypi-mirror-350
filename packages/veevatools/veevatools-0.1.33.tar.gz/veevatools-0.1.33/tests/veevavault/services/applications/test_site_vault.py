from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.site_vault import SiteVaultService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.site_vault
class TestSiteVaultServiceUnit:
    """
    Unit tests for SiteVaultService class using mocks (no real API calls)
    """

    @fixture
    def site_vault_service(self):
        """Fixture for creating a SiteVaultService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return SiteVaultService(client)

    @patch("requests.request")
    def test_create_user(self, mock_request, site_vault_service):
        """Test create_user method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "person_id": "person123",
            "message": "User created successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        site_vault_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        user_data = [
            {
                "user": {
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "security_policy_id": "policy123",
                    "person_type": "staff__v",
                    "language": "en",
                },
                "person_type": "staff__v",
                "is_investigator": False,
                "assignments": {
                    "org_assignment": {
                        "org_id": "org123",
                        "application_role": "site_staff__v",
                    },
                    "site_assignments": [
                        {"site_id": "site123", "application_role": "site_staff__v"}
                    ],
                },
            }
        ]

        # Call method
        result = site_vault_service.create_user(user_data)

        # Verify client.api_call was called with correct parameters
        site_vault_service.client.api_call.assert_called_once()
        args, kwargs = site_vault_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/sitevault/useradmin/persons"
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == user_data
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["person_id"] == "person123"

    @patch("requests.request")
    def test_edit_user(self, mock_request, site_vault_service):
        """Test edit_user method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "person_id": "person123",
            "message": "User updated successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        site_vault_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        person_id = "person123"
        user_data = {
            "username": "test.user",
            "is_investigator": True,
            "assignments": {
                "org_assignment": {
                    "org_id": "org123",
                    "application_role": "site_investigator__v",
                },
                "site_assignments": [
                    {"site_id": "site123", "application_role": "site_investigator__v"}
                ],
            },
        }

        # Call method
        result = site_vault_service.edit_user(person_id, user_data)

        # Verify client.api_call was called with correct parameters
        site_vault_service.client.api_call.assert_called_once()
        args, kwargs = site_vault_service.client.api_call.call_args

        assert (
            kwargs["endpoint"] == "api/v25.1/app/sitevault/useradmin/persons/person123"
        )
        assert kwargs["method"] == "PUT"
        assert kwargs["json"] == user_data
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["person_id"] == "person123"

    @patch("requests.request")
    def test_retrieve_documents_and_signatories(self, mock_request, site_vault_service):
        """Test retrieve_documents_and_signatories method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "documents": [
                {"id": "doc123", "name": "Informed Consent Form", "version": "1.0"}
            ],
            "signatories": [{"id": "sig123", "name": "John Doe", "role": "subject__v"}],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        site_vault_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        participant_id = "participant123"

        # Call method
        result = site_vault_service.retrieve_documents_and_signatories(participant_id)

        # Verify client.api_call was called with correct parameters
        site_vault_service.client.api_call.assert_called_once()
        args, kwargs = site_vault_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/sitevault/econsent/participant/participant123"
        )
        assert kwargs["method"] == "GET"

        # Verify response
        assert isinstance(result, list)  # The method should return the result directly

    @patch("requests.request")
    def test_send_documents_to_signatories(self, mock_request, site_vault_service):
        """Test send_documents_to_signatories method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "message": "Documents sent for signature",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        site_vault_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        documents_version_id = "doc_ver123"
        signatory_id = "sig123"
        signatory_role = "subject__v"
        subject_id = "subject123"

        # Call method
        result = site_vault_service.send_documents_to_signatories(
            documents_version_id, signatory_id, signatory_role, subject_id
        )

        # Verify client.api_call was called with correct parameters
        site_vault_service.client.api_call.assert_called_once()
        args, kwargs = site_vault_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/sitevault/econsent/send"
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == {
            "documents.version_id__v": "doc_ver123",
            "signatory__v.id": "sig123",
            "signatory__v.role__v": "subject__v",
            "subject__v.id": "subject123",
        }
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"


@mark.integration
@mark.veevavault
@mark.site_vault
class TestSiteVaultServiceIntegration:
    """
    Integration tests for SiteVaultService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def site_vault_service(self, authenticated_vault_client):
        """Fixture for creating a SiteVaultService instance with a real client"""
        return SiteVaultService(authenticated_vault_client)

    def test_create_user(self, site_vault_service, vault_config):
        """Test create_user with real API"""
        # Skip if not authenticated
        if not site_vault_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real user data
        pytest.skip("This test requires real user data and appropriate permissions")

    def test_retrieve_documents_and_signatories(self, site_vault_service, vault_config):
        """Test retrieve_documents_and_signatories with real API"""
        # Skip if not authenticated
        if not site_vault_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need a real participant ID
        pytest.skip(
            "This test requires a real participant ID and appropriate permissions"
        )
