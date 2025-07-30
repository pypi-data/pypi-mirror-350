from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.safety import SafetyService
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.safety
class TestSafetyServiceUnit:
    """
    Unit tests for SafetyService class using mocks (no real API calls)
    """

    @fixture
    def safety_service(self):
        """Fixture for creating a SafetyService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return SafetyService(client)

    @patch("requests.request")
    def test_intake_inbox_item(self, mock_request, safety_service):
        """Test intake_inbox_item method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "intake_id": "intake123",
            "url": "https://test.veevavault.com/api/v25.1/app/safety/intake/status?inbound_id=intake123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data - we'll mock the file open
        with patch("builtins.open", mock_open(read_data="dummy e2b file content")):
            # Call method
            result = safety_service.intake_inbox_item(
                file_path="test.xml",
                format="e2b_r3__v",
                origin_organization="sponsor_org__v",
                organization="vault_customer__v",
                transmission_profile="general_api_profile__v",
            )

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/intake/inbox-item"
        assert kwargs["method"] == "POST"
        assert isinstance(kwargs["files"], dict)
        assert "file" in kwargs["files"]
        assert kwargs["data"] == {
            "format": "e2b_r3__v",
            "origin-organization": "sponsor_org__v",
            "organization": "vault_customer__v",
            "transmission-profile": "general_api_profile__v",
        }

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["intake_id"] == "intake123"

    @patch("requests.request")
    def test_intake_imported_case(self, mock_request, safety_service):
        """Test intake_imported_case method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "intake_id": "intake123",
            "url": "https://test.veevavault.com/api/v25.1/app/safety/intake/status?inbound_id=intake123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data - we'll mock the file open
        with patch("builtins.open", mock_open(read_data="dummy e2b file content")):
            # Call method
            result = safety_service.intake_imported_case(
                file_path="test.xml",
                format="e2b_r3__v",
                organization="vault_customer__v",
                origin_organization="sponsor_org__v",
            )

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/intake/imported-case"
        assert kwargs["method"] == "POST"
        assert isinstance(kwargs["files"], dict)
        assert "file" in kwargs["files"]
        assert kwargs["data"] == {
            "format": "e2b_r3__v",
            "organization": "vault_customer__v",
            "origin-organization": "sponsor_org__v",
        }

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["intake_id"] == "intake123"

    @patch("requests.request")
    def test_retrieve_intake_status(self, mock_request, safety_service):
        """Test retrieve_intake_status method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "status": "COMPLETE",
            "inbound-transmission": "trans123",
            "number-cases": 1,
            "number-successes": 1,
            "number-failures": 0,
            "icsr-details": [
                {"status": "SUCCESS", "case-id": "case123", "inbox-item-id": "inbox123"}
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data
        inbound_id = "intake123"

        # Call method
        result = safety_service.retrieve_intake_status(inbound_id)

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/intake/status"
        assert kwargs["method"] == "GET"
        assert kwargs["params"] == {"inbound_id": "intake123"}
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["status"] == "COMPLETE"
        assert result["number-cases"] == 1
        assert len(result["icsr-details"]) == 1

    @patch("requests.request")
    def test_retrieve_ack(self, mock_request, safety_service):
        """Test retrieve_ack method"""
        # Set up mock response
        mock_response = MagicMock()
        # This would typically return XML
        mock_response.text = "<ACKNOWLEDGEMENT>test ack</ACKNOWLEDGEMENT>"
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response

        # Test data
        inbound_id = "intake123"

        # Call method
        result = safety_service.retrieve_ack(inbound_id)

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/intake/ack"
        assert kwargs["method"] == "GET"
        assert kwargs["params"] == {"inbound_id": "intake123"}
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["raw_response"] is True

        # Verify raw response is returned
        assert result == mock_response

    @patch("requests.request")
    def test_intake_json(self, mock_request, safety_service):
        """Test intake_json method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "jobID": "job123",
            "transmissionRecordId": "trans123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data - for file-like objects
        with patch("builtins.open", mock_open(read_data='{"json_data": "test"}')):
            # Call method
            result = safety_service.intake_json(
                api_name="vault_customer",
                intake_json="test.json",
                intake_form="source_doc.pdf",
            )

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/safety/ai/intake?API_Name=vault_customer"
        )
        assert kwargs["method"] == "POST"
        assert isinstance(kwargs["files"], dict)
        assert "intake_json" in kwargs["files"]
        assert "intake_form" in kwargs["files"]
        assert kwargs["headers"]["Content-Type"] == "multipart/form-data"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["jobID"] == "job123"
        assert result["transmissionRecordId"] == "trans123"

    @patch("requests.request")
    def test_import_narrative(self, mock_request, safety_service):
        """Test import_narrative method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Narrative imported successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data
        case_id = "case123"
        narrative_type = "primary"
        narrative_language = "eng"
        narrative_text = "This is a test narrative for case 123."

        # Call method
        result = safety_service.import_narrative(
            case_id, narrative_type, narrative_language, narrative_text
        )

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/import-narrative"
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["caseId"] == "case123"
        assert kwargs["headers"]["narrativeType"] == "primary"
        assert kwargs["headers"]["narrativeLanguage"] == "eng"
        assert kwargs["data"] == narrative_text

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["message"] == "Narrative imported successfully"

    @patch("requests.request")
    def test_bulk_import_narrative(self, mock_request, safety_service):
        """Test bulk_import_narrative method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "import_id": "import123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data - we'll mock the file open
        with patch(
            "builtins.open",
            mock_open(
                read_data="caseId,narrativeType,narrativeLanguage,narrative\ncase123,primary,eng,test narrative"
            ),
        ):
            # Call method
            result = safety_service.bulk_import_narrative(
                narratives_file="narratives.csv",
                integrity_check=True,
                migration_mode=True,
                archive_document=False,
            )

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert kwargs["endpoint"] == "api/v25.1/app/safety/import-narrative/batch"
        assert kwargs["method"] == "POST"
        assert isinstance(kwargs["files"], dict)
        assert "narratives" in kwargs["files"]
        assert kwargs["headers"]["Content-Type"] == "multipart/form-data"
        assert kwargs["headers"]["X-VaultAPI-IntegrityCheck"] == "true"
        assert kwargs["headers"]["X-VaultAPI-MigrationMode"] == "true"
        assert kwargs["headers"]["X-VaultAPI-ArchiveDocument"] == "false"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["import_id"] == "import123"

    @patch("requests.request")
    def test_retrieve_bulk_import_status(self, mock_request, safety_service):
        """Test retrieve_bulk_import_status method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "status": "COMPLETE",
            "total": 2,
            "successful": 2,
            "failed": 0,
            "narratives": [
                {"status": "SUCCESS", "caseId": "case123", "documentId": "doc123"},
                {"status": "SUCCESS", "caseId": "case456", "documentId": "doc456"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        safety_service.client.api_call.return_value = mock_response.json.return_value

        # Test data
        import_id = "import123"

        # Call method
        result = safety_service.retrieve_bulk_import_status(import_id)

        # Verify client.api_call was called with correct parameters
        safety_service.client.api_call.assert_called_once()
        args, kwargs = safety_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/safety/import-narrative/batch/import123"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["status"] == "COMPLETE"
        assert result["total"] == 2
        assert len(result["narratives"]) == 2


@mark.integration
@mark.veevavault
@mark.safety
class TestSafetyServiceIntegration:
    """
    Integration tests for SafetyService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def safety_service(self, authenticated_vault_client):
        """Fixture for creating a SafetyService instance with a real client"""
        return SafetyService(authenticated_vault_client)

    def test_retrieve_intake_status(self, safety_service, vault_config):
        """Test retrieve_intake_status with real API"""
        # Skip if not authenticated
        if not safety_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need a real intake ID
        pytest.skip("This test requires a real intake ID and appropriate permissions")

    def test_import_narrative(self, safety_service, vault_config):
        """Test import_narrative with real API"""
        # Skip if not authenticated
        if not safety_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need a real case ID
        pytest.skip("This test requires a real case ID and appropriate permissions")
