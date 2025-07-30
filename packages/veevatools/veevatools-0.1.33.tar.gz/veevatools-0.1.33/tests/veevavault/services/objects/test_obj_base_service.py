from pytest import mark, fixture
import pytest
import requests
from unittest.mock import patch, MagicMock

from veevavault.client import VaultClient
from veevavault.services.objects.base_service import BaseObjectService


@mark.unit
@mark.veevavault
class TestBaseObjectServiceUnit:
    """
    Unit tests for BaseObjectService
    """

    def test_initialization(self):
        """Test initialization of BaseObjectService"""
        client = VaultClient()
        service = BaseObjectService(client)

        # Verify the client is correctly stored
        assert service.client == client

    def test_inherited_services(self):
        """Test that other services properly inherit from BaseObjectService"""
        from veevavault.services.objects.crud_service import ObjectCRUDService
        from veevavault.services.objects.metadata_service import ObjectMetadataService

        client = VaultClient()

        # Create instances of services
        crud_service = ObjectCRUDService(client)
        metadata_service = ObjectMetadataService(client)

        # Verify they inherit from BaseObjectService
        assert isinstance(crud_service, BaseObjectService)
        assert isinstance(metadata_service, BaseObjectService)

        # Verify they have the client attribute
        assert crud_service.client == client
        assert metadata_service.client == client
