import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import MagicMock

from veevavault.services.security_policies import SecurityPoliciesService


@pytest.mark.unit
@pytest.mark.veevavault
class TestSecurityPoliciesServiceUnit:
    """
    Unit tests for SecurityPoliciesService using mocks
    """

    def setup_method(self):
        # Create a fake client with a mockable api_call and version attr
        self.client = MagicMock()
        self.client.LatestAPIversion = "v99.9"
        self.service = SecurityPoliciesService(self.client)

    def test_retrieve_security_policy_metadata_calls_api_with_correct_url(self):
        expected = {"responseStatus": "SUCCESS", "meta": {}}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_security_policy_metadata()

        url = f"api/{self.client.LatestAPIversion}/metadata/objects/securitypolicies"
        self.client.api_call.assert_called_once_with(url)
        assert result == expected

    def test_retrieve_all_security_policies_calls_api_with_correct_url(self):
        expected = {"responseStatus": "SUCCESS", "security_policies__v": []}
        self.client.api_call.return_value = expected

        result = self.service.retrieve_all_security_policies()

        url = f"api/{self.client.LatestAPIversion}/objects/securitypolicies"
        self.client.api_call.assert_called_once_with(url)
        assert result == expected

    def test_retrieve_security_policy_calls_api_with_correct_url(self):
        expected = {"responseStatus": "SUCCESS", "policy": {}}
        name = "12345"
        self.client.api_call.return_value = expected

        result = self.service.retrieve_security_policy(name)

        url = f"api/{self.client.LatestAPIversion}/objects/securitypolicies/{name}"
        self.client.api_call.assert_called_once_with(url)
        assert result == expected

    def test_get_security_policy_dataframe_with_data(self):
        # Mock the underlying retrieve_all_security_policies
        policies = [
            {"name__v": "1", "label__v": "L1", "value__v": "/v1"},
            {"name__v": "2", "label__v": "L2", "value__v": "/v2"},
        ]
        self.service.retrieve_all_security_policies = MagicMock(
            return_value={"responseStatus": "SUCCESS", "security_policies__v": policies}
        )

        df = self.service.get_security_policy_dataframe()

        expected_df = pd.DataFrame(policies)
        assert_frame_equal(df.reset_index(drop=True), expected_df)

    def test_get_security_policy_dataframe_no_policies_returns_empty(self):
        self.service.retrieve_all_security_policies = MagicMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        df = self.service.get_security_policy_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["name__v", "label__v", "value__v"]
        assert df.empty

    def test_get_security_policy_dataframe_failure_raises(self):
        self.service.retrieve_all_security_policies = MagicMock(
            return_value={"responseStatus": "FAIL", "error": "oops"}
        )
        with pytest.raises(Exception) as exc:
            self.service.get_security_policy_dataframe()
        assert "Failed to retrieve security policies" in str(exc.value)


@pytest.mark.integration
@pytest.mark.veevavault
class TestSecurityPoliciesServiceIntegration:
    """
    Integration tests for SecurityPoliciesService using real API calls.
    These tests will be skipped if no Vault credentials are available.
    """

    def test_retrieve_security_policy_metadata(
        self, security_policies_service, vault_config
    ):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        resp = security_policies_service.retrieve_security_policy_metadata()
        assert resp["responseStatus"] == "SUCCESS"
        # should contain object metadata description
        assert "properties" in resp or "description" in resp

    def test_retrieve_all_security_policies(
        self, security_policies_service, vault_config
    ):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        resp = security_policies_service.retrieve_all_security_policies()
        assert resp["responseStatus"] == "SUCCESS"
        assert "security_policies__v" in resp
        # expect at least one policy in a typical Vault
        assert isinstance(resp["security_policies__v"], list)

    def test_retrieve_specific_policy(self, security_policies_service, vault_config):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        all_resp = security_policies_service.retrieve_all_security_policies()
        policies = all_resp.get("security_policies__v", [])
        if not policies:
            pytest.skip("No security policies found to test retrieval")
        name = policies[0]["name__v"]
        resp = security_policies_service.retrieve_security_policy(name)
        assert resp["responseStatus"] == "SUCCESS"
        assert "policy_details__v" in resp
        # security settings should appear if active
        assert isinstance(resp.get("policy_security_settings__v", {}), dict)

    def test_get_dataframe_integration(self, security_policies_service, vault_config):
        if not vault_config.username or not vault_config.password:
            pytest.skip("Vault credentials not available")
        df = security_policies_service.get_security_policy_dataframe()
        assert isinstance(df, pd.DataFrame)
        # if policies exist, DataFrame should have rows; if not, empty is acceptable
        assert set(df.columns) == {"name__v", "label__v", "value__v"}
