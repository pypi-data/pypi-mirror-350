from urllib.parse import urlparse
import requests
from typing import Dict, Any, Optional, Union


class VaultClient:
    """
    Core client for interacting with the Veeva Vault API.
    This class handles basic API communication while delegating authentication to AuthenticationService.
    """

    def __init__(self):
        self.vaultURL = None
        self.vaultUserName = None
        self.vaultPassword = None
        self.vaultConnection = None
        self.sessionId = None
        self.vaultId = None
        self.vaultDNS = None
        self.APIheaders = None
        self.APIversionList = []
        self.LatestAPIversion = "v25.1"

        # Property alias for service classes that expect session_id vs sessionId
        self._session_id = None

    @property
    def session_id(self):
        """
        Getter for session_id property that returns sessionId
        """
        return self.sessionId

    @session_id.setter
    def session_id(self, value):
        """
        Setter for session_id property that updates both sessionId and _session_id
        """
        self.sessionId = value
        self._session_id = value

    def api_call(
        self,
        endpoint: str,
        method: str = "GET",
        data: Any = None,
        params: Dict = None,
        headers: Dict = None,
        files: Dict = None,
        json: Any = None,
        raw_response: bool = False,
        **kwargs,
    ) -> Union[Dict[str, Any], requests.Response]:
        """
        This function is used to make API calls to the Veeva Vault API. It is a wrapper around the requests library.

        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Dictionary, list of tuples, bytes, or file-like object to send in the body
            params: Dictionary or bytes to be sent in the query string
            headers: Dictionary of HTTP headers to send with the request
            files: Dictionary of file-like objects for multipart encoding upload
            json: JSON data to send in the body
            raw_response: Whether to return the raw response object instead of parsed JSON
            kwargs: Additional arguments for requests.request

        Returns:
            Either a JSON parsed dictionary or the raw response object if raw_response is True
        """
        if headers is None:
            headers = {}

        # Add default headers if not already provided
        if "Accept" not in headers:
            headers["Accept"] = "application/json"
        if "Authorization" not in headers and self.sessionId:
            headers["Authorization"] = f"{self.sessionId}"

        # Construct the full URL - handle both absolute and relative paths
        if endpoint.startswith(("http://", "https://")):
            api_url = endpoint
        else:
            baseUrl = self.vaultURL.rstrip("/")
            # Make sure we don't have double slashes
            clean_endpoint = endpoint.lstrip("/")
            api_url = f"{baseUrl}/{clean_endpoint}"

        try:
            response = requests.request(
                method=method,
                url=api_url,
                headers=headers,
                params=params,
                data=data,
                files=files,
                json=json,
                **kwargs,
            )
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            if raw_response:
                return response
            return response.json()  # Return JSON response
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

    def authenticate(
        self,
        vaultURL=None,
        vaultUserName=None,
        vaultPassword=None,
        sessionId=None,
        vaultId=None,
        if_return=False,
        *args,
        **kwargs,
    ):
        """
        Authenticate with the Veeva Vault API.
        This method is a stub that delegates to AuthenticationService.
        It's maintained here for backward compatibility.

        Args:
            vaultURL: URL of the Vault instance
            vaultUserName: User name for authentication
            vaultPassword: Password for authentication
            sessionId: Existing session ID (optional)
            vaultId: Vault ID (optional)
            if_return: Whether to return authentication details

        Returns:
            dict: Authentication details if if_return is True, otherwise None
        """
        # This is a stub that will be implemented by the AuthenticationService
        # We have to import inline to avoid circular imports
        from veevavault.services.authentication import AuthenticationService

        auth_service = AuthenticationService(self)
        return auth_service.authenticate(
            vaultURL=vaultURL,
            vaultUserName=vaultUserName,
            vaultPassword=vaultPassword,
            sessionId=sessionId,
            vaultId=vaultId,
            if_return=if_return,
            *args,
            **kwargs,
        )

    def validate_session_user(
        self,
        exclude_vault_membership: bool = False,
        exclude_app_licensing: bool = False,
    ) -> Dict[str, Any]:
        """
        Given a valid session ID, this request returns information for the currently authenticated user.
        In case of an invalid session ID, it returns an INVALID_SESSION_ID error.

        Args:
            exclude_vault_membership: If set to true, vault_membership fields are omitted from the response
            exclude_app_licensing: If set to true, app_licensing fields are omitted from the response

        Returns:
            Information of the currently authenticated user or an error message for invalid session ID
        """
        url = f"{self.vaultURL}/api/{self.LatestAPIversion}/objects/users/me"

        headers = {"Accept": "application/json", "Authorization": self.sessionId}

        params = {
            "exclude_vault_membership": str(exclude_vault_membership).lower(),
            "exclude_app_licensing": str(exclude_app_licensing).lower(),
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def session_keep_alive(self) -> Dict[str, Any]:
        """
        Given an active sessionId, keep the session active by refreshing the session duration.
        This is a stub method that delegates to AuthenticationService.keep_alive().

        Returns:
            dict: Response from the API call indicating the success status.
        """
        # Import inline to avoid circular imports
        from veevavault.services.authentication import AuthenticationService

        auth_service = AuthenticationService(self)
        return auth_service.keep_alive()
