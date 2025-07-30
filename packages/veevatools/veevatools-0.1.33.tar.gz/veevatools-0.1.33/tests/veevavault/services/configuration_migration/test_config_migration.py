import os
import pytest
from pytest import mark, fixture
import io
import json
from unittest.mock import patch, MagicMock, mock_open

from veevavault.services.configuration_migration import ConfigurationMigrationService


@mark.unit
@mark.veevavault
class TestConfigMigrationServiceUnit:
    """
    Unit tests for ConfigurationMigrationService class using mocks (no real API calls)
    """

    @fixture
    def migration_service(self):
        """Create a ConfigurationMigrationService with a mock client"""
        mock_client = MagicMock()
        mock_client.LatestAPIversion = "v25.1"
        return ConfigurationMigrationService(mock_client)

    def test_init(self, migration_service):
        """Test service initialization"""
        assert migration_service.client is not None
        assert migration_service.client.LatestAPIversion == "v25.1"

    def test_export_package(self, migration_service):
        """Test export_package method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB123",
            "job_id": "JB123",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        result = migration_service.export_package("Test_Package")

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            "api/v25.1/services/package",
            method="POST",
            data={"packageName": "Test_Package"},
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB123"

    def test_import_package_with_string_path(self, migration_service):
        """Test import_package method with a string file path"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB456",
            "job_id": "JB456",
        }
        migration_service.client.api_call.return_value = mock_response

        # Mock the open function
        m = mock_open(read_data=b"mock file content")

        # Use patch to mock built-in open function
        with patch("builtins.open", m):
            result = migration_service.import_package("test_package.vpk")

        # Verify the API call - we can't check the files argument directly
        # since it contains a file object, but we can check other parts
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "PUT"
        assert "file" in kwargs["files"]

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB456"

    def test_import_package_with_file_object(self, migration_service):
        """Test import_package method with a file-like object"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB456",
            "job_id": "JB456",
        }
        migration_service.client.api_call.return_value = mock_response

        # Create a file-like object
        file_obj = io.BytesIO(b"mock file content")

        # Call the method
        result = migration_service.import_package(file_obj)

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "PUT"
        assert "file" in kwargs["files"]

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB456"

    def test_deploy_package(self, migration_service):
        """Test deploy_package method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB789",
            "job_id": "JB789",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        package_id = "VP123"
        result = migration_service.deploy_package(package_id)

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            f"api/v25.1/vobject/vault_package__v/{package_id}/actions/deploy",
            method="POST",
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB789"

    def test_retrieve_package_deploy_results(self, migration_service):
        """Test retrieve_package_deploy_results method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "summary": {"total": 10, "success": 10, "error": 0},
            "deployment_log": "https://test.veevavault.com/api/v25.1/objects/jobs/JB789/outputs/deployment_log",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        package_id = "VP123"
        result = migration_service.retrieve_package_deploy_results(package_id)

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            f"api/v25.1/vobject/vault_package__v/{package_id}/actions/deploy/results",
            method="GET",
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["summary"]["total"] == 10
        assert "deployment_log" in result

    def test_retrieve_outbound_package_dependencies(self, migration_service):
        """Test retrieve_outbound_package_dependencies method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "total_dependencies": 2,
            "target_vault_id": "1234",
            "package_name": "Test_Package",
            "package_id": "OP123",
            "url": "https://test.veevavault.com/api/v25.1/vobjects/outbound_package__v/OP123/actions/add",
            "package_dependencies": [
                {
                    "id": "comp1",
                    "component_type__v": "Doctype",
                    "name__v": "Test_Doctype",
                },
                {
                    "id": "comp2",
                    "component_type__v": "Workflow",
                    "name__v": "Test_Workflow",
                },
            ],
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        package_id = "OP123"
        result = migration_service.retrieve_outbound_package_dependencies(package_id)

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            f"api/v25.1/vobjects/outbound_package__v/{package_id}/dependencies",
            method="GET",
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["total_dependencies"] == 2
        assert len(result["package_dependencies"]) == 2

    def test_query_component_definitions(self, migration_service):
        """Test query_component_definitions method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "data": [
                {
                    "id": "comp1",
                    "mdl_definition__v": "component doctype Test_Doctype { /* definition */ }",
                },
                {
                    "id": "comp2",
                    "mdl_definition__v": "component workflow Test_Workflow { /* definition */ }",
                },
            ],
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        query = "SELECT id, mdl_definition__v FROM vault_component__v WHERE component_type__v = 'Doctype'"
        result = migration_service.query_component_definitions(query)

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            "api/v25.1/query/components", method="POST", data={"q": query}
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert len(result["data"]) == 2

    def test_compare_vaults(self, migration_service):
        """Test compare_vaults method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB101",
            "job_id": "JB101",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method with default parameters
        target_vault_id = "V456"
        result = migration_service.compare_vaults(target_vault_id)

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["vault_id"] == target_vault_id
        assert kwargs["data"]["results_type"] == "differences"
        assert kwargs["data"]["details_type"] == "simple"
        assert kwargs["data"]["include_doc_binder_templates"] is True
        assert kwargs["data"]["include_vault_settings"] is True
        assert kwargs["data"]["generate_outbound_packages"] is False

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB101"

    def test_compare_vaults_with_custom_params(self, migration_service):
        """Test compare_vaults method with custom parameters"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB102",
            "job_id": "JB102",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method with custom parameters
        target_vault_id = "V456"
        result = migration_service.compare_vaults(
            target_vault_id,
            results_type="complete",
            details_type="complex",
            include_doc_binder_templates=False,
            include_vault_settings=False,
            component_types="Doclifecycle,Doctype,Workflow",
            generate_outbound_packages=True,
        )

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["vault_id"] == target_vault_id
        assert kwargs["data"]["results_type"] == "complete"
        assert kwargs["data"]["details_type"] == "complex"
        assert kwargs["data"]["include_doc_binder_templates"] is False
        assert kwargs["data"]["include_vault_settings"] is False
        assert kwargs["data"]["component_types"] == "Doclifecycle,Doctype,Workflow"
        assert kwargs["data"]["generate_outbound_packages"] is True

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB102"

    def test_generate_configuration_report(self, migration_service):
        """Test generate_configuration_report method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB103",
            "job_id": "JB103",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method with default parameters
        result = migration_service.generate_configuration_report()

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["include_vault_settings"] is True
        assert kwargs["data"]["include_inactive_components"] is False
        assert kwargs["data"]["include_doc_binder_templates"] is True
        assert kwargs["data"]["suppress_empty_results"] is False
        assert kwargs["data"]["output_format"] == "Excel_Macro_Enabled"

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB103"

    def test_generate_configuration_report_with_custom_params(self, migration_service):
        """Test generate_configuration_report method with custom parameters"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "url": "https://test.veevavault.com/api/v25.1/objects/jobs/JB104",
            "job_id": "JB104",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method with custom parameters
        result = migration_service.generate_configuration_report(
            include_vault_settings=False,
            include_inactive_components=True,
            include_components_modified_since="2023-01-01",
            include_doc_binder_templates=False,
            suppress_empty_results=True,
            component_types="Doclifecycle,Doctype",
            output_format="Excel",
        )

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["data"]["include_vault_settings"] is False
        assert kwargs["data"]["include_inactive_components"] is True
        assert kwargs["data"]["include_components_modified_since"] == "2023-01-01"
        assert kwargs["data"]["include_doc_binder_templates"] is False
        assert kwargs["data"]["suppress_empty_results"] is True
        assert kwargs["data"]["component_types"] == "Doclifecycle,Doctype"
        assert kwargs["data"]["output_format"] == "Excel"

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["job_id"] == "JB104"

    def test_validate_package_with_string_path(self, migration_service):
        """Test validate_package method with a string file path"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "summary": {"total": 5, "success": 5, "error": 0},
            "validation_details": [
                {
                    "component_type": "Doctype",
                    "component_name": "Test_Doctype",
                    "status": "VALID",
                },
                {
                    "component_type": "Workflow",
                    "component_name": "Test_Workflow",
                    "status": "VALID",
                },
            ],
        }
        migration_service.client.api_call.return_value = mock_response

        # Mock the open function
        m = mock_open(read_data=b"mock file content")

        # Use patch to mock built-in open function
        with patch("builtins.open", m):
            result = migration_service.validate_package("test_package.vpk")

        # Verify the API call - we can't check the files argument directly
        # since it contains a file object, but we can check other parts
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert "file" in kwargs["files"]

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["summary"]["total"] == 5
        assert len(result["validation_details"]) == 2

    def test_validate_package_with_file_object(self, migration_service):
        """Test validate_package method with a file-like object"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "summary": {"total": 5, "success": 5, "error": 0},
            "validation_details": [
                {
                    "component_type": "Doctype",
                    "component_name": "Test_Doctype",
                    "status": "VALID",
                },
                {
                    "component_type": "Workflow",
                    "component_name": "Test_Workflow",
                    "status": "VALID",
                },
            ],
        }
        migration_service.client.api_call.return_value = mock_response

        # Create a file-like object
        file_obj = io.BytesIO(b"mock file content")

        # Call the method
        result = migration_service.validate_package(file_obj)

        # Verify the API call
        migration_service.client.api_call.assert_called_once()
        args, kwargs = migration_service.client.api_call.call_args
        assert kwargs["method"] == "POST"
        assert "file" in kwargs["files"]

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["summary"]["total"] == 5
        assert len(result["validation_details"]) == 2

    def test_validate_inbound_package(self, migration_service):
        """Test validate_inbound_package method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "summary": {"total": 5, "success": 5, "error": 0},
            "validation_details": [
                {
                    "component_type": "Doctype",
                    "component_name": "Test_Doctype",
                    "status": "VALID",
                },
                {
                    "component_type": "Workflow",
                    "component_name": "Test_Workflow",
                    "status": "VALID",
                },
            ],
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        package_id = "VP123"
        result = migration_service.validate_inbound_package(package_id)

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            f"api/v25.1/services/vobject/vault_package__v/{package_id}/actions/validate",
            method="POST",
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"
        assert result["summary"]["total"] == 5
        assert len(result["validation_details"]) == 2

    def test_enable_configuration_mode(self, migration_service):
        """Test enable_configuration_mode method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "message": "Configuration Mode enabled successfully",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        result = migration_service.enable_configuration_mode()

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            "api/v25.1/services/configuration_mode/actions/enable", method="POST"
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"

    def test_disable_configuration_mode(self, migration_service):
        """Test disable_configuration_mode method"""
        # Set up mock response
        mock_response = {
            "responseStatus": "SUCCESS",
            "message": "Configuration Mode disabled successfully",
        }
        migration_service.client.api_call.return_value = mock_response

        # Call the method
        result = migration_service.disable_configuration_mode()

        # Verify the API call
        migration_service.client.api_call.assert_called_once_with(
            "api/v25.1/services/configuration_mode/actions/disable", method="POST"
        )

        # Verify response
        assert result == mock_response
        assert result["responseStatus"] == "SUCCESS"


@mark.integration
@mark.veevavault
class TestConfigMigrationServiceIntegration:
    """
    Integration tests for ConfigurationMigrationService class using real API calls
    These tests will be skipped if no credentials are available
    """

    @fixture
    def migration_service(self, authenticated_vault_client):
        """Create a ConfigurationMigrationService with authenticated client"""
        return ConfigurationMigrationService(authenticated_vault_client)

    @mark.skip(
        reason="This test requires an existing outbound package and real credentials"
    )
    def test_export_package(self, migration_service):
        """Test export_package method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call the method with a real package name
        result = migration_service.export_package("Test_Package")

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "job_id" in result
        assert "url" in result

    @mark.skip(reason="This test requires a VPK file and real credentials")
    def test_import_package(self, migration_service):
        """Test import_package method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Path to a test VPK file
        vpk_path = "test_data/test_package.vpk"

        # Skip if test file doesn't exist
        if not os.path.exists(vpk_path):
            pytest.skip(f"Test VPK file not found: {vpk_path}")

        # Call the method
        result = migration_service.import_package(vpk_path)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "job_id" in result
        assert "url" in result

    @mark.skip(
        reason="This test requires an existing imported package and real credentials"
    )
    def test_deploy_package(self, migration_service):
        """Test deploy_package method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Use a real package ID
        package_id = "VP123"  # This would be a real ID in a real test

        # Call the method
        result = migration_service.deploy_package(package_id)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "job_id" in result
        assert "url" in result

    @mark.skip(
        reason="This test requires an existing deployed package and real credentials"
    )
    def test_retrieve_package_deploy_results(self, migration_service):
        """Test retrieve_package_deploy_results method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Use a real package ID
        package_id = "VP123"  # This would be a real ID in a real test

        # Call the method
        result = migration_service.retrieve_package_deploy_results(package_id)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "summary" in result
        assert "deployment_log" in result

    @mark.skip(
        reason="This test requires an existing outbound package and real credentials"
    )
    def test_retrieve_outbound_package_dependencies(self, migration_service):
        """Test retrieve_outbound_package_dependencies method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Use a real outbound package ID
        package_id = "OP123"  # This would be a real ID in a real test

        # Call the method
        result = migration_service.retrieve_outbound_package_dependencies(package_id)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "total_dependencies" in result
        assert "target_vault_id" in result
        assert "package_name" in result

    def test_query_component_definitions(self, migration_service):
        """Test query_component_definitions method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Construct a simple query
        query = "SELECT id, name__v, component_type__v FROM vault_component__v LIMIT 10"

        # Call the method
        result = migration_service.query_component_definitions(query)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "data" in result
        assert isinstance(result["data"], list)

    @mark.skip(reason="This test requires admin privileges and a target vault ID")
    def test_compare_vaults(self, migration_service):
        """Test compare_vaults method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Use a real target vault ID
        target_vault_id = "V456"  # This would be a real ID in a real test

        # Call the method
        result = migration_service.compare_vaults(target_vault_id)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "job_id" in result
        assert "url" in result

    @mark.skip(reason="This test requires admin privileges")
    def test_generate_configuration_report(self, migration_service):
        """Test generate_configuration_report method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Call the method
        result = migration_service.generate_configuration_report()

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "job_id" in result
        assert "url" in result

    @mark.skip(reason="This test requires a VPK file and real credentials")
    def test_validate_package(self, migration_service):
        """Test validate_package method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Path to a test VPK file
        vpk_path = "test_data/test_package.vpk"

        # Skip if test file doesn't exist
        if not os.path.exists(vpk_path):
            pytest.skip(f"Test VPK file not found: {vpk_path}")

        # Call the method
        result = migration_service.validate_package(vpk_path)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "summary" in result
        assert "validation_details" in result

    @mark.skip(
        reason="This test requires an existing imported package and real credentials"
    )
    def test_validate_inbound_package(self, migration_service):
        """Test validate_inbound_package method with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Use a real package ID
        package_id = "VP123"  # This would be a real ID in a real test

        # Call the method
        result = migration_service.validate_inbound_package(package_id)

        # Verify response structure
        assert result["responseStatus"] == "SUCCESS"
        assert "summary" in result
        assert "validation_details" in result

    @mark.skip(reason="This test requires admin privileges and affects all vault users")
    def test_enable_and_disable_configuration_mode(self, migration_service):
        """Test enable_configuration_mode and disable_configuration_mode methods with real API"""
        # Skip if not authenticated
        if not migration_service.client.sessionId:
            pytest.skip("No authenticated session available")

        # Test enable
        enable_result = migration_service.enable_configuration_mode()
        assert enable_result["responseStatus"] == "SUCCESS"

        # Add some delay to allow the change to take effect
        # import time
        # time.sleep(5)

        # Test disable
        disable_result = migration_service.disable_configuration_mode()
        assert disable_result["responseStatus"] == "SUCCESS"
