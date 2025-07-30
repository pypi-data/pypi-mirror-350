from pytest import mark, fixture, skip
import pytest
import json
import requests
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.applications.clinical_operations import (
    ClinicalOperationsService,
)
from veevavault.client import VaultClient


@mark.unit
@mark.veevavault
@mark.clinical_operations
class TestClinicalOperationsServiceUnit:
    """
    Unit tests for ClinicalOperationsService class using mocks (no real API calls)
    """

    @fixture
    def clinical_operations_service(self):
        """Fixture for creating a ClinicalOperationsService instance with a mocked client"""
        client = MagicMock(spec=VaultClient)
        client.LatestAPIversion = "v25.1"
        return ClinicalOperationsService(client)

    @patch("requests.request")
    def test_create_edls(self, mock_request, clinical_operations_service):
        """Test create_edls method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        study_id = "study123"
        data = "id,name\n001,Test Document"

        # Call method
        result = clinical_operations_service.create_edls(study_id, data)

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        # Check the endpoint contains the study_id
        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/study__v/study123/actions/etmfcreateedl"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_recalculate_milestone_document_field(
        self, mock_request, clinical_operations_service
    ):
        """Test recalculate_milestone_document_field method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Recalculation job started",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        data = "id\ndoc001\ndoc002"

        # Call method
        result = clinical_operations_service.recalculate_milestone_document_field(data)

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/objects/documents/milestones/actions/recalculate"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["message"] == "Recalculation job started"

    @patch("requests.request")
    def test_apply_edl_template_to_milestone(
        self, mock_request, clinical_operations_service
    ):
        """Test apply_edl_template_to_milestone method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        milestone_id = "milestone123"
        edl_id = "edl123"

        # Call method
        result = clinical_operations_service.apply_edl_template_to_milestone(
            milestone_id, edl_id
        )

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/milestone__v/milestone123/actions/etmfcreateedl"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == {"edl_id": "edl123"}
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_create_milestones_from_template(
        self, mock_request, clinical_operations_service
    ):
        """Test create_milestones_from_template method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "url": "https://test.veevavault.com/api/v25.1/jobs/job123",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        object_name = "study__v"
        object_record_id = "study123"

        # Call method
        result = clinical_operations_service.create_milestones_from_template(
            object_name, object_record_id
        )

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/vobjects/study__v/study123/actions/createmilestones"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_execute_milestone_story_events(
        self, mock_request, clinical_operations_service
    ):
        """Test execute_milestone_story_events method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "total": 2,
            "successful": 2,
            "failed": 0,
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        object_name = "study__v"
        data = "id,story_event__v\nstudy123,event1\nstudy456,event2"
        id_param = "name__v"

        # Call method
        result = clinical_operations_service.execute_milestone_story_events(
            object_name, data, id_param
        )

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/clinical/milestone/study__v/actions/applytemplate?idParam=name__v"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["total"] == 2
        assert result["successful"] == 2

    @patch("requests.request")
    def test_generate_milestone_documents(
        self, mock_request, clinical_operations_service
    ):
        """Test generate_milestone_documents method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Milestone documents generated successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        data = "id\nmilestone123\nmilestone456"

        # Call method
        result = clinical_operations_service.generate_milestone_documents(data)

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/clinical/milestone/actions/generatemilestonedocuments"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "text/csv"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_distribute_to_sites(self, mock_request, clinical_operations_service):
        """Test distribute_to_sites method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "job_id": "job123",
            "message": "Distribution job started",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        safety_distribution_id = "dist123"

        # Call method
        result = clinical_operations_service.distribute_to_sites(safety_distribution_id)

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/clinical/safety_distributions/dist123/actions/send"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["headers"]["Accept"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "job123"

    @patch("requests.request")
    def test_populate_site_fee_definitions(
        self, mock_request, clinical_operations_service
    ):
        """Test populate_site_fee_definitions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Site fee definitions populated successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        target_study = "study123"
        source_study = ["study456", "study789"]

        # Call method
        result = clinical_operations_service.populate_site_fee_definitions(
            target_study, source_study
        )

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/clinical/payments/populate-site-fee-definitions"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == {
            "target_study": "study123",
            "source_study": ["study456", "study789"],
        }
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"

    @patch("requests.request")
    def test_populate_procedure_definitions(
        self, mock_request, clinical_operations_service
    ):
        """Test populate_procedure_definitions method"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "responseStatus": "SUCCESS",
            "message": "Procedure definitions populated successfully",
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Set up client mock to return our mock response
        clinical_operations_service.client.api_call.return_value = (
            mock_response.json.return_value
        )

        # Test data
        data = [
            {
                "source_holder_object_name": "study__v",
                "source_holder_object_ids": ["study456"],
                "destination_holder_object_name": "study__v",
                "destination_holder_object_id": "study123",
            }
        ]

        # Call method
        result = clinical_operations_service.populate_procedure_definitions(data)

        # Verify client.api_call was called with correct parameters
        clinical_operations_service.client.api_call.assert_called_once()
        args, kwargs = clinical_operations_service.client.api_call.call_args

        assert (
            kwargs["endpoint"]
            == "api/v25.1/app/clinical/ctms/populate-procedure-definitions"
        )
        assert kwargs["method"] == "POST"
        assert kwargs["json"] == data
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # Verify response
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
@mark.clinical_operations
class TestClinicalOperationsServiceIntegration:
    """
    Integration tests for ClinicalOperationsService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def clinical_operations_service(self, authenticated_vault_client):
        """Fixture for creating a ClinicalOperationsService instance with a real client"""
        return ClinicalOperationsService(authenticated_vault_client)

    def test_create_edls(self, clinical_operations_service, vault_config):
        """Test create_edls with real API"""
        # Skip if not authenticated or if in mock mode
        if not clinical_operations_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need a real study ID and EDL data
        # For now, we'll skip it as it requires specific test data
        pytest.skip("This test requires a real study ID and EDL data")

    def test_apply_edl_template_to_milestone(self, clinical_operations_service):
        """Test apply_edl_template_to_milestone with real API"""
        # Skip if not authenticated
        if not clinical_operations_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # This test would need real milestone and EDL IDs
        pytest.skip("This test requires real milestone and EDL IDs")
