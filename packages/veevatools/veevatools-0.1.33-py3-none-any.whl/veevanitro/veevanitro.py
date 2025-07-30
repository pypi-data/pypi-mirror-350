from sys import platform
import requests
import pandas as pd
import os
import json
from urllib.parse import urlparse
from typing import List, Optional
import asyncio
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from urllib.parse import quote_plus

try:
    from nitro_utils.s3_utils import display_progress
except:
    from veevanitro.nitro_utils.s3_utils import display_progress

# Async
from veevanitro.nitro_utils.async_utils import async_wrap



class Vnitro:
    
    def __init__(self):
        self.serverUrl: str = None # from authenticate
        self.nitroUserName: str = None # from authenticate
        self.nitroPassword: str = None # from authenticate
        self.accessToken: str = None # from authenticate
        self.refreshToken: str = None # from authenticate
        self.appServerUrl: str = None # from authenticate
        self.tenantName: str = None # from authenticate
        self.workingRedshiftPwd: str = None # from initialize_cdw_config
        self.cdw_config: dict = None # from initialize_cdw_config
        self.instances: List[Optional(dict)] = None # from authenticate
        self.tenantRoles: List[Optional(dict)] = None # from authenticate
        self.instanceRoles: List[Optional(dict)] = None # from authenticate
        self.instancePermissions: dict = None # from authenticate
        self.cdwAPItoken: str = None # from get_cdw_api_token
        self.tenant: dict = None # from get_tenant
        self.configuration: dict = None # from get_configuration
        self.users: List[Optional(dict)] = None # from get_users
        self.applicationRoles: List[Optional(dict)] = None # from get_application_roles
        self.rules: dict = {} # from get_rules
        self.groups: dict = {} # from get_groups
        self.jobs: dict = {} # from get_jobs
        self.connectors: dict = {} # from get_connectors
        self.clusterDetails: dict = {} # from get_cluster_details
        self.jobResults: dict = {} # from get_results
        self.workingInstance: str = None # Set by any method that requires an instance name, last used instance name is stored here
                                         # Upon authentication, the first instance in the list of instances is set as the working instance
        
        # Redshift
        self.workingRedshiftUser: str = None # from set_redshift_user
        self.workspaces: dict = {} # from get_workspaces
        self.workingWorkspaceName: dict = {} # from connect_to_user_workspace
        self.workingWorkspaceConnection: dict = {} # from connect_to_user_workspace
        self.redshiftDBdetails: dict = {} # from get_redshift_dbs
        self.workingDB: str = None # from get_redshift_dbs
        self.workingDBConnection: psycopg2.extensions.connection = None # from from get_db_connection
        self.workspaceConnections: dict = {} # from connect_to_user_workspace
        self.redshiftPort: str = '5439'
        self.workingDBConnection: psycopg2.extensions.connection = None # from from get_db_connection
        self.workingDBCursor: psycopg2.extensions.cursor = None # from from get_db_connection
        self.workingSQLalchemyEngine: sqlalchemy.engine.base.Engine = None # from get_sqlalchemy_engine
        
        # S3 Client
        self.s3_clients: boto3.client = {} # from get_s3_client
        self.workingS3Client: boto3.client = None # from get_s3_client
        self.workingS3Bucket: str = None # from get_s3_client
        self.workingS3PathPrefix: str = None # from get_s3_client
        
        
    def _handle_response(self, response):
        """
        A helper method to handle API responses.
        
        Args:
            response (Response): The response object from the requests library.
            
        Returns:
            dict: The response JSON content.
            
        Raises:
            Exception: If the response indicates an error.
        """
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 401:
            if 'error' in response.json().keys():
                raise Exception(f"Unauthorized: {response.json()['error']}")
                
            else:
                raise Exception(f"Request failed. Response from server: {response.json()}")
        else:
            raise Exception(f"Request failed. Response from server: {response.json()}")
    
    def authenticate(
        self,
        serverUrl: str = None,
        nitroUserName: str = None,
        nitroPassword: str = None,
        accessToken: str = None
    ):
        """
        Authenticates the user with the Veeva Nitro API. If the accessToken is provided, the username and password are not required.
        The authentication also retrieves the tenant information and sets the attributes of the class to the response JSON.
        It loads the following attributes:
            self.accessToken, self.refreshToken, self.serverUrl, self.appServerUrl, self.tenantName,
            self.instances, self.tenantRoles, self.instanceRoles, self.instancePermissions
        
        Args:
            serverUrl (str): Required. The base URL for the Veeva Nitro API. Example: https://mycompany.veevanitro.com
            nitroUserName (str, optional): The username for authentication. Defaults to None. Must be provided if accessToken is not provided.
            nitroPassword (str, optional): The password for authentication. Defaults to None. Must be provided if accessToken is not provided.
            accessToken (str, optional): The session ID for authentication. Defaults to None. Must be provided if nitroUserName and nitroPassword are not provided.
            
        Raises:
            Exception: If the necessary parameters for authentication are not provided.
            Exception: If the authentication fails.
        """
        self.serverUrl = serverUrl if serverUrl is not None else self.serverUrl
        self.nitroUserName = nitroUserName if nitroUserName is not None else self.nitroUserName
        self.nitroPassword = nitroPassword if nitroPassword is not None else self.nitroPassword
        self.accessToken = accessToken if accessToken is not None else self.accessToken
        
        url = f"{self.serverUrl}/api/v1/auth/login"
        
        # Ensure at least serverUrl and accessToken are provided or serverUrl and nitroUserName and nitroPassword are provided
        if (self.serverUrl is None) or (self.accessToken is None and (self.nitroUserName is None or self.nitroPassword is None)):
            raise Exception("serverUrl and accessToken are required or serverUrl and nitroUserName and nitroPassword are required")
        
        # If authenticating with username and password:
        if self.accessToken is None:
            # Get the session ID
            payload = {
                "username": self.nitroUserName,
                "password": self.nitroPassword
            }

            response = requests.post(url, json=payload)
            
        # If authenticating with session ID
        else:
            # There is not a clear way to authenticate using accessToken, so we will just make a request to the tenant endpoint to test the validity of the session ID
            url = f"{self.serverUrl}/api/v1/admin/tenant"
            payload = {
                "Authorization": self.accessToken
            }

            response = requests.get(url, headers=payload)
            
        response_json = self._handle_response(response)
            

        attributes = [
            'accessToken', 'refreshToken', 'serverUrl', 'appServerUrl', 'tenantName',
            'instances', 'tenantRoles', 'instanceRoles', 'instancePermissions'
        ]

        # Decision was made here to raise an exception if
        # the response does not contain the expected attributes
        # This is to ensure that the attributes of the class are set correctly
        # and that future methods can rely on the attributes being set
        # MPay 2023-08-18
        try:
            # Set the attributes of the class to the response JSON
            for attr in attributes:
                setattr(self, attr, response_json[attr])
        except:
            raise Exception(f"""API response did not contain the expected attributes.
            Expected attributes: {attributes}
            Response JSON: {response_json}
            Please contact the developer or system administrator for assistance.
            Has the API changed due to latest release?""")
        
        # Set working instance
        try:
            self.workingInstance = self.instances[0]['instanceName']
        except:
            self.workingInstance = None
        
        return response_json
    
    def initialize_cdw_config(self, redshiftPassword: str = None):
        self.get_cdw_api_token()
        self.workingRedshiftPwd = self.nitroPassword if redshiftPassword is None else redshiftPassword
        
        self.cdw_config = {
                        'serverUrl' : self.serverUrl,
                        'apiKey': self.cdwAPItoken,
                        'tenantName': self.tenantName,
                        'dwInstanceName': self.workingInstance,
                        'redshiftUser': self.workingRedshiftUser,
                        'redshiftPwd': self.workingRedshiftPwd,
                        'connectorName':'global__v'
                        }
    
    def refreshAuthToken(self):
        
        # https://cdw-us2-app-us.veevanitro.com/api/v1/users/tokens/renew

        if self.accessToken is None or self.refreshToken is None:
            raise Exception("You must authenticate first before executing this method")

        url = f"{self.serverUrl}/api/v1/users/tokens/renew"
        
        headers = {
            "refreshToken": self.refreshToken,
        }
        response = requests.post(url, headers=headers)
        
        # response_json = self._handle_response(response)
        
        # if 'content' in response_json and 'token' in response_json['content']:
        #     self.accessToken = response_json['content']['token']
            
        return response
    
    def download_cli(self) -> bytes:
        """
        Downloads the Command-Line Interface (CLI) zip file from the server.

        Raises:
            Exception: If the user is not authenticated.
            Exception: If the server returns an unauthorized error.
            Exception: If any other server-side error occurs.

        Returns:
            bytes: The raw content of the downloaded ZIP file.
        """

        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")

        url = f"{self.serverUrl}/api/v1/download/cli"
        
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # get the zip file content from the response
            data = getattr(response,'content', '')

            # define the filename
            filename = "cdw-cli"

            # save the data to the file
            with open(filename, "wb") as f:
                f.write(data)

            print(f"ZIP file saved as {filename} in {os.getcwd()}")
            return data
        
        elif response.status_code == 401:
            if 'error' in response.json().keys():
                raise Exception(f"Unauthorized: {response.json()['error']}")
            else:
                raise Exception(f"Request failed. Response from server: {response.json()}")
        else:
            raise Exception(f"Request failed. Response from server: {response.json()}")

    def download_sdk(self) -> bytes:
        """
        Downloads the Software Development Kit (SDK) zip file from the server.

        Raises:
            Exception: If the user is not authenticated.
            Exception: If the server returns an unauthorized error.
            Exception: If any other server-side error occurs.

        Returns:
            bytes: The raw content of the downloaded ZIP file.
        """

        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")

        url = f"{self.serverUrl}/api/v1/download/sdk"
        
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # get the zip file content from the response
            data = getattr(response, 'content', '')

            # define the filename
            filename = "nitro_sdk_latest.whl"

            # save the data to the file
            with open(filename, "wb") as f:
                f.write(data)

            print(f"ZIP file saved as {filename} in {os.getcwd()}")
            return data
        
        elif response.status_code == 401:
            if 'error' in response.json().keys():
                raise Exception(f"Unauthorized: {response.json()['error']}")
            else:
                raise Exception(f"Request failed. Response from server: {response.json()}")
        else:
            raise Exception(f"Request failed. Response from server: {response.json()}")


        return response
    
    def get_cdw_api_token(self):
        """
        Retrieves the CDW API token using the authenticated session.
        
        Returns:
            dict: The response JSON containing the CDW API token.
            
        Raises:
            Exception: If the request for the CDW API token fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/users/tokens/issue"
        
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.post(url, headers=headers)
        
        respone_json = self._handle_response(response)
        
        if 'content' in respone_json and 'token' in respone_json['content']:
            self.cdwAPItoken = respone_json['content']['token']
        
        return respone_json
            
    def get_tenant(self) -> dict:
        """
        Retrieves tenant information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing tenant details.
            
        Raises:
            Exception: If the request for tenant information fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/tenant"
        headers = {
            "Authorization": self.accessToken,
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.tenant = response_json['content']
        
        return response_json

    def get_configuration(self) -> dict:
        """
        Retrieves cluster configuration from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing cluster configuration details.
            
        Raises:
            Exception: If the request for cluster configuration fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/cluster/configuration"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.configuration = response_json['content']
        
        return response_json

    def get_redshift_dbs(self, Dwinstancename = None) -> dict:
        """
        Retrieves Redshift database configuration from the Veeva Nitro API.

        Args:
            Dwinstancename (str, optional): The name of the instance you're working with. Defaults to the currently set working instance.

        Returns:
            dict: The response JSON containing Redshift database configuration.

        Raises:
            Exception: If the request for Redshift database configuration fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance

        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")

        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        # Building the request
        url = f"{self.serverUrl}/mds/api/v1/configuration?view=condensed"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        # Making the GET request
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        # Save the response content under the Dwinstancename key
        if 'content' in response_json:
            self.redshiftDBdetails[self.workingInstance] = response_json['content']
        
        if 'content' in response_json and 'instanceDatabase' in response_json['content'] and 'database' in response_json['content']['instanceDatabase']:
            self.workingDB = response_json['content']['instanceDatabase']['database']

        # Return the response JSON containing Redshift database configuration
        return response_json
    
    def get_users(self) -> dict:
        """
        Retrieves user information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing user details.
            
        Raises:
            Exception: If the request for user information fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/users"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.users = response_json['content']
        
        return response_json

    # Question: Where can I find the app parameter values?
    def get_application_roles(self, app: str = "APP_SERVER") -> dict:
        """
        Retrieves application roles from the Veeva Nitro API.
        
        Args:
            app (str, optional): The application type. Defaults to "APP_SERVER".
            
        Returns:
            dict: The response JSON containing application roles.
            
        Raises:
            Exception: If the request for application roles fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/users/application-roles?app={app}"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.applicationRoles = response_json['content']
        
        return response_json


    def get_rules(self, Dwinstancename = None) -> dict:
        """
        Retrieves rule information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing rule details.
            
        Raises:
            Exception: If the request for rule information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/rules"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        # Save the response content under the Dwinstancename key
        if 'content' in response_json:
            self.rules[self.workingInstance] = response_json['content']
        
        return response_json

    def get_groups(self, Dwinstancename = None) -> dict:
        """
        Retrieves rule group information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing rule group details.
            
        Raises:
            Exception: If the request for rule group information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/rule/groups"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.groups[self.workingInstance] = response_json['content']
        
        return response_json

    def get_jobs(self, Dwinstancename = None, view: str = "condensed") -> dict:
        """
        Retrieves job information from the Veeva Nitro API.
        
        Args:
            view (str, optional): The view type for the jobs. Defaults to "condensed".
            
        Returns:
            dict: The response JSON containing job details.
            
        Raises:
            Exception: If the request for job information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/jobs?view={view}"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.jobs[self.workingInstance] = response_json['content']
        
        return response_json

    def get_connectors(self, Dwinstancename = None, internalOnly: bool = False, ) -> dict:
        """
        Retrieves connector information from the Veeva Nitro API.
        
        Args:
            internalOnly (bool, optional): Filter for internal connectors. Defaults to False.
            
        Returns:
            dict: The response JSON containing connector details.
            
        Raises:
            Exception: If the request for connectors fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/connectors?internalOnly={internalOnly}"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.connectors[self.workingInstance] = response_json['content']
        
        return response_json

    def get_cluster_details(self, Dwinstancename = None) -> dict:
        """
        Retrieves cluster details from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing cluster details.
            
        Raises:
            Exception: If the request for cluster details fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/cluster-details"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.clusterDetails[self.workingInstance] = response_json['content']
        
        return response_json

    def get_job_results(self, Dwinstancename: str = None, size: int = 1000, jobId: str = None) -> dict:
        """
        Retrieves job results from the Veeva Nitro API.
        
        Args:
            instanceName (str): The name of the instance.
            size (int, optional): The number of results to retrieve. Defaults to 1000.
            jobId (str, optional): The ID of the job. Defaults to None.
            
        Returns:
            dict: The response JSON containing job results.
            
        Raises:
            Exception: If the request for job results fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/jobs/results?instanceName={self.workingInstance}&size={size}&jobId={jobId}"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.jobResults[self.workingInstance] = response_json['content']
        
        return response_json
    

    ##############################################################################################################
    # Workspace methods
    ##############################################################################################################
    def set_redshift_user(self, nitroUserName: str = None, redshiftUserName: str = None):
        """
        Sets the current Redshift user based on either nitroUserName, redshiftUserName or self.nitroUserName.
        
        Args:
            nitroUserName (str, optional): Nitro username to search for and set the corresponding Redshift user.
            redshiftUserName (str, optional): Directly provide the Redshift username to set.
            
        Raises:
            ValueError: If both nitroUserName and redshiftUserName are provided.
            Exception: If the Redshift username cannot be found.
        """
        
        # If both parameters are provided, raise a value error.
        if nitroUserName and redshiftUserName:
            raise ValueError("Provide either nitroUserName or redshiftUserName, not both.")

        # If self.users is None, attempt to populate it using the get_users method.
        if self.users is None:
            self.get_users()

        # Check if self.users is still None after trying to populate it.
        if self.users is None:
            raise Exception("Unable to fetch users. Ensure self.get_users() is properly implemented and data source is available.")
        
        # Use self.nitroUserName if no parameters are provided
        if not nitroUserName and not redshiftUserName:
            nitroUserName = self.nitroUserName

        if nitroUserName:
            for user in self.users:
                if user['username'] == nitroUserName and 'redshiftUserName' in user:
                    self.workingRedshiftUser = user['redshiftUserName']
                    return
            raise Exception(f"Redshift user not found for Nitro username {nitroUserName}")
        
        if redshiftUserName:
            for user in self.users:
                if user.get('redshiftUserName') == redshiftUserName:
                    self.workingRedshiftUser = redshiftUserName
                    return
            raise Exception("RedshiftUserName not found.")
      
    def get_workspaces(self, redshiftUserName: str = None, Dwinstancename: str = None):
        """
        Fetches a list of user workspaces for a given Redshift user.

        This function attempts to get workspaces for a specified Redshift user. If no Redshift user is provided, 
        it checks and uses the workingRedshiftUser attribute. If the attribute is also not set, it attempts to set it 
        using the set_redshift_user() method. In addition, if a data warehouse instance name (Dwinstancename) is provided, 
        it updates the working instance to the given name. If not, it uses the currently set working instance.
        
        Args:
            redshiftUserName (str, optional): Redshift username for which workspaces are to be fetched. Defaults to None.
            Dwinstancename (str, optional): Data warehouse instance name to set as the working instance. Defaults to the currently set instance.
        
        Returns:
            dict: JSON response from the server containing user workspace information.
            
        Raises:
            Exception: 
                - If there's an issue fetching the workspaces.
                - If RedshiftUserName isn't provided and cannot be set via set_redshift_user method.
                - If instance name isn't provided and hasn't been set via authenticate method.
        """

        # Update self.workingRedshiftUser if redshiftUserName is provided
        if redshiftUserName:
            self.workingRedshiftUser = redshiftUserName
        elif self.workingRedshiftUser is None:
            self.set_redshift_user()
            
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance


        # Check if self.workingRedshiftUser is set after all checks and assignments
        if self.workingRedshiftUser is None:
            raise Exception("RedshiftUserName must be provided or set via set_redshift_user method.")
    
        # Check if self.workingInstance is set after all checks and assignments
        if self.workingInstance is None:
            raise Exception("Instance name must be provided or set via authenticate method.")

        
        headers = {
            'Tenantname': self.tenantName,
            'Dwinstancename': self.workingInstance,
            'Connectorname': 'global__v', # Currently hard-coded
            "Authorization": self.accessToken
        }
        
        
        url = f"{self.serverUrl}/mds/api/v1/workspaces"
        
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        # Save the response in self.workspaces using the workingInstance as the key
        if 'content' in response_json:
            self.workspaces[self.workingInstance] = response_json['content']
    
        # Filter the content if redshiftUserName is provided
        if redshiftUserName and 'content' in response_json:
            filtered_content = [entry for entry in response_json['content'] if entry.get('owner') == redshiftUserName]
            response_json['content'] = filtered_content

        return response_json

    def connect_to_user_workspace(self, workspaceName: str = None, Dwinstancename: str = None, redshiftUserName: str = None):
        """
        Connects to a specified user workspace.
        
        Args:
            workspaceName (str): The name of the workspace to connect to.
            
        Returns:
            dict: The workspace details.
            
        Raises:
            Exception: If there's an issue connecting to the workspace.
        """
        
        
        if self.workspaces is None:
            self.get_workspaces(Dwinstancename = Dwinstancename, redshiftUserName = redshiftUserName)
            
        if redshiftUserName:
            self.workingRedshiftUser = redshiftUserName
        elif self.workingRedshiftUser is None:
            self.set_redshift_user()
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if workspaceName is None and self.workingWorkspaceName is None:
            raise Exception("You must provide a workspace name or set the working workspace before executing this method")
        
        if workspaceName is not None:
            self.workingWorkspaceName = workspaceName
        else:
            workspaceName = self.workingWorkspaceName
        
        
        print(f"Connecting to workspace {workspaceName} for Redshift user {self.workingRedshiftUser} on instance {self.workingInstance}")
        headers = {
            'tenantName': self.tenantName,
            'dwInstanceName': self.workingInstance,
            'connectorName': 'global__v',
            "Authorization": self.accessToken
        }
        
        params = {'redshiftUser': self.workingRedshiftUser}
        url = f"{self.serverUrl}/api/v1/admin/workspaces/{workspaceName}/session-token"
        
        response = requests.get(url, headers=headers, params=params)
        response_json = self._handle_response(response)
        
        
        # Save the response in self.workspaceConnections using the { self.workingInstance: { workspaceName: { self.workingRedshiftUser: response_json } } } as the key
        if 'content' in response_json:
            if self.workingInstance not in self.workspaceConnections:
                self.workspaceConnections[self.workingInstance] = {}
                
            if workspaceName not in self.workspaceConnections[self.workingInstance]:
                self.workspaceConnections[self.workingInstance][workspaceName] = {}
                
            self.workspaceConnections[self.workingInstance][workspaceName][self.workingRedshiftUser] = response_json['content']
            
        self.workingWorkspaceConnection = response_json['content']
        
        return response_json
    
    ##############################################################################################################
    # S3 client methods
    ##############################################################################################################
    
    def get_s3_client(self, workspaceName: str = None, Dwinstancename: str = None, redshiftUserName: str = None):
        # Check or instantiate necessary instance variables same as connect_to_user_workspace
        if self.workspaces is None:
            self.get_workspaces(Dwinstancename=Dwinstancename, redshiftUserName=redshiftUserName)

        if redshiftUserName:
            self.workingRedshiftUser = redshiftUserName
        elif self.workingRedshiftUser is None:
            self.set_redshift_user()

        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance

        if workspaceName is None and self.workingWorkspaceName is None:
            raise Exception("You must provide a workspace name or set the working workspace before executing this method")

        if workspaceName is not None:
            self.workingWorkspaceName = workspaceName

        # Check if workspaceConnections exists. If not, connect to user workspace and reattempt
        if not hasattr(self, 'workspaceConnections') or self.workingInstance not in self.workspaceConnections or \
                self.workingWorkspaceName not in self.workspaceConnections[self.workingInstance] or \
                self.workingRedshiftUser not in self.workspaceConnections[self.workingInstance][self.workingWorkspaceName]:
            print(f"Credentials not found. Connecting to workspace...")
            self.connect_to_user_workspace(workspaceName=self.workingWorkspaceName, Dwinstancename=self.workingInstance,
                                        redshiftUserName=self.workingRedshiftUser)

        # Try to get credentials again after connecting
        try:
            credentials = self.workspaceConnections[self.workingInstance][self.workingWorkspaceName][self.workingRedshiftUser]['credentials']
        except KeyError:
            raise Exception("Credentials not found for the provided combination of Dwinstancename, workspaceName, and redshiftUserName")

        # Check expiration
        expiration_datetime = datetime.strptime(credentials['expiration'], '%Y-%m-%dT%H:%M:%S.%f+00:00').replace(tzinfo=timezone.utc)
        if expiration_datetime <= datetime.now(timezone.utc):
            raise Exception("The token has expired!")

        # Create and save the S3 client
        session = boto3.Session(
            aws_access_key_id=credentials['accessKeyId'],
            aws_secret_access_key=credentials['secretAccessKey'],
            aws_session_token=credentials['sessionToken']
        )
        s3_client = session.client('s3')

        # Saving s3 client in the desired format
        if not hasattr(self, 's3_clients'):
            self.s3_clients = {}

        if self.workingInstance not in self.s3_clients:
            self.s3_clients[self.workingInstance] = {}

        if self.workingWorkspaceName not in self.s3_clients[self.workingInstance]:
            self.s3_clients[self.workingInstance][self.workingWorkspaceName] = {}

        self.s3_clients[self.workingInstance][self.workingWorkspaceName][self.workingRedshiftUser] = s3_client

        self.workingS3Client = s3_client
        
        self.workingWorkspaceConnection = self.workspaceConnections[self.workingInstance][self.workingWorkspaceName][self.workingRedshiftUser]
        
        s3_url = urlparse(self.workspaceConnections[self.workingInstance][self.workingWorkspaceName][self.workingRedshiftUser]['s3ObjectKey'], allow_fragments=False)
        
        self.workingS3Bucket = s3_url.netloc
        self.workingS3PathPrefix = s3_url.path.lstrip('/')
        
        return s3_client

    def list_user_workspace(self):
        """
        Lists the files in the user's workspace on S3 based on the specified prefix.
        
        Args:
            parameters (dict, optional): Additional parameters for filtering the files. Defaults to None.

        Returns:
            dict: A dictionary mapping the file keys to their respective sizes.
        """
        objects = dict()
        try:
            paginator = self.workingS3Client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.workingS3Bucket, Prefix=self.workingS3PathPrefix)

            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        objKey = obj['Key']
                        objSize = obj['Size']
                        if objKey:
                            temp = objKey.replace(self.workingS3PathPrefix, '')
                            objects[temp] = objSize
                                
        except Exception as ex:
            print('list-user-workspace error :', str(ex))

        return objects


    def get_file_from_workspace(self, key, filePath, callback=None):
        """
        Downloads a file from the user's workspace on S3.

        Args:
            key (str): The key of the file to download.
            filePath (str): The local path to save the downloaded file.
            callback (function, optional): A function to track download progress. Defaults to `display_progress`.

        Returns:
            File: The downloaded file object.

        Raises:
            Exception: If there's any error during the file download process.
        """
        s3Key = self.workingS3PathPrefix + key
        meta_data = self.workingS3Client.head_object(Bucket=self.workingS3Bucket, Key=s3Key)
        total_length = int(meta_data.get('ContentLength', 0))

        if callback is None:
            callback = display_progress(total_length)

        with open(filePath, 'wb') as localFile:
            self.workingS3Client.download_fileobj(Bucket=self.workingS3Bucket, Key=s3Key, Fileobj=localFile, Callback=callback)
            sys.stdout.write("\n")
            sys.stdout.flush()
        
        print(f"Downloaded {s3Key} to {filePath}")
        return None

    def upload_file_to_workspace(self, filePath, key, callback=None):
        """
        Uploads a file to the user's workspace on S3.

        Args:
            filePath (str): The local path of the file to be uploaded.
            key (str): The key to save the file under in S3.
            callback (function, optional): A function to track upload progress. Defaults to `display_progress`.

        Returns:
            str: "Success" if the upload completes without errors, "Failed" otherwise.

        Raises:
            Exception: If there's any error during the file upload process.
        """
        total = os.stat(filePath).st_size
        s3Key = self.workingS3PathPrefix + key
        
        if callback is None:
            callback = display_progress(total)

        with open(filePath, 'rb') as localFile:
            self.workingS3Client.upload_fileobj(
                Bucket=self.workingS3Bucket, 
                Key=s3Key, 
                Fileobj=localFile, 
                Callback=callback
            )
            sys.stdout.write("\n")
            sys.stdout.flush()
            print(f"Uploaded {filePath} to {s3Key}")
            return None
        # Catching an exception and re-raising it will allow the caller to handle the exception as needed.
        raise Exception("Error uploading file to workspace.")

    def delete_file_from_workspace(self, *keys) -> dict:
        """
        Deletes one or more files from the user's workspace on S3.
        
        Args:
            *keys (str): The keys of the files to delete.
        """
        try:
            for key in keys:
                s3Key = self.workingS3PathPrefix + key
                return self.workingS3Client.delete_object(Bucket=self.workingS3Bucket, Key=s3Key)
        except Exception as ex:
            raise Exception(f"Error deleting {key} from workspace: {str(ex)}")


    def check_key_file_exists(self, key) -> bool:
        """
        Checks if a file exists in the user's workspace on S3.
        
        Args:
            key (str): The key of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            self.workingS3Client.head_object(Bucket=self.workingS3Bucket, Key=self.workingS3PathPrefix + key)
        except ClientError as e:
            print("Key file " + key + " does not exist on s3: ", str(e))
            return False

        return True

    ##############################################################################################################
    # Redshift Methods
    ##############################################################################################################
    def get_db_connection(self):
        """
        Establishes and returns a database connection using the psycopg2 library.

        This method checks the necessary attributes of the instance to form a connection string. 
        The attributes checked are:
        - workingDB: The name of the working database.
        - configuration: A dictionary containing the cluster's endpoint. The key to check is 'clusterEndpoint'.
        - redshiftPort: The port to connect to on the Redshift cluster.
        - workingRedshiftUser: The Redshift username.
        - workingRedshiftPwd: The Redshift password.

        If any of the above attributes are empty or None, a ValueError is raised.

        :return: A psycopg2 connection object established using the attributes provided.
        :raises ValueError: If any necessary attributes are empty or None.
        """
    
        if not self.workingDB:
            raise ValueError("workingDB attribute is empty or None!")

        if not self.configuration or 'clusterEndpoint' not in self.configuration or not self.configuration['clusterEndpoint']:
            raise ValueError("clusterEndpoint in configuration is empty or None!")

        if not self.redshiftPort:
            raise ValueError("redshiftPort attribute is empty or None!")

        if not self.workingRedshiftUser:
            raise ValueError("workingRedshiftUser attribute is empty or None!")

        if not self.workingRedshiftPwd:
            raise ValueError("workingRedshiftPwd attribute is empty or None!")
        
        connectionString = ("dbname={dbname} host={host} port={port} "
                        "user={userid} password={password}").format(
                            dbname=self.workingDB,
                            host=self.configuration['clusterEndpoint'],
                            port=self.redshiftPort,
                            userid=self.workingRedshiftUser,
                            password=self.workingRedshiftPwd
                        )
        
        connection = psycopg2.connect(connectionString)
        connection.autocommit = True
        
        self.workingDBConnection = connection
        
        return connection
    
    def get_db_cursor(self, connection: psycopg2.extensions.connection = None):
        """
        Creates a database cursor using the given connection.

        :param connection: A psycopg2 connection object to be used for creating the cursor.
        :return: A psycopg2 cursor object.
        :raises ValueError: If no connection is provided and workingDBConnection attribute is empty or None.
        """
        if connection is None and self.workingDBConnection is None:
            raise ValueError("No connection provided and workingDBConnection attribute is empty or None!")
        elif connection is None:
            connection = self.workingDBConnection
        
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        self.workingDBCursor = cursor
        
        return cursor
    
    def close_db_connection(self, connection: psycopg2.extensions.connection = None):
        """
        Closes the given database connection.

        :param connection: A psycopg2 connection object to be closed.
        """
        if connection is None and self.workingDBConnection is None:
            raise ValueError("No connection provided and workingDBConnection attribute is empty or None!")
        elif connection is None:
            connection = self.workingDBConnection
        
        connection.close()
    

    def get_sqlalchemy_engine(self):
        """
        Establishes and returns a database connection using SQLAlchemy with the psycopg2 driver.

        This method checks the necessary attributes of the instance to form a connection string. 
        The attributes checked are:
        - workingDB: The name of the working database.
        - configuration: A dictionary containing the cluster's endpoint. The key to check is 'clusterEndpoint'.
        - redshiftPort: The port to connect to on the Redshift cluster.
        - workingRedshiftUser: The Redshift username.
        - workingRedshiftPwd: The Redshift password.

        If any of the above attributes are empty or None, a ValueError is raised.

        :return: A SQLAlchemy engine object established using the attributes provided.
        :raises ValueError: If any necessary attributes are empty or None.
        """

        if not self.workingDB:
            raise ValueError("workingDB attribute is empty or None!")

        if not self.configuration or 'clusterEndpoint' not in self.configuration or not self.configuration['clusterEndpoint']:
            raise ValueError("clusterEndpoint in configuration is empty or None!")

        if not self.redshiftPort:
            raise ValueError("redshiftPort attribute is empty or None!")

        if not self.workingRedshiftUser:
            raise ValueError("workingRedshiftUser attribute is empty or None!")

        if not self.workingRedshiftPwd:
            raise ValueError("workingRedshiftPwd attribute is empty or None!")

        connection_string = ("postgresql+psycopg2://{userid}:{password}@{host}:{port}/{dbname}").format(
            userid=quote_plus(self.workingRedshiftUser),
            password=quote_plus(self.workingRedshiftPwd),
            host=self.configuration['clusterEndpoint'],
            port=self.redshiftPort,
            dbname=self.workingDB
        )

        engine = create_engine(connection_string, echo=False)  # echo=False disables logging of SQL statements

        # Store the engine for later use (optional)
        self.workingSQLalchemyEngine = engine
        
        return engine
    
    ##############################################################################################################
    # Async methods
    ##############################################################################################################
    
    async def get_rules_from_instances(self, instances: List[str] = None):
        """
        Retrieves rule information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing rule details.
            
        Raises:
            Exception: If the request for rule information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """

        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_rules = async_wrap(self.get_rules)
        
        rules_dict = {}
        
        for instance in instances:
            tasks.append(async_get_rules(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            rules_dict[instance] = responses[i]['content']
        
        self.rules = rules_dict
        
        return rules_dict
    
    async def get_groups_from_instances(self, instances: List[str] = None):
        """
        Retrieves rule group information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing rule group details.
            
        Raises:
            Exception: If the request for rule group information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_groups = async_wrap(self.get_groups)
        
        groups_dict = {}
        
        for instance in instances:
            tasks.append(async_get_groups(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            groups_dict[instance] = responses[i]['content']
        
        self.groups = groups_dict
        
        return groups_dict

    async def get_jobs_from_instances(self, instances: List[str] = None, view: str = "condensed"):
        """
        Retrieves job information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            view (str, optional): The view type for the jobs. Defaults to "condensed".
            
        Returns:
            dict: The response JSON containing job details.
            
        Raises:
            Exception: If the request for job information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_jobs = async_wrap(self.get_jobs)
        
        jobs_dict = {}
        
        for instance in instances:
            tasks.append(async_get_jobs(Dwinstancename=instance, view=view))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            jobs_dict[instance] = responses[i]['content']
        
        self.jobs = jobs_dict
        
        return jobs_dict
    
    async def get_connectors_from_instances(self, instances: List[str] = None, internalOnly: bool = False):
        """
        Retrieves connector information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            internalOnly (bool, optional): Filter for internal connectors. Defaults to False.
            
        Returns:
            dict: The response JSON containing connector details.
            
        Raises:
            Exception: If the request for connectors fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_connectors = async_wrap(self.get_connectors)
        
        connectors_dict = {}
        
        for instance in instances:
            tasks.append(async_get_connectors(Dwinstancename=instance, internalOnly=internalOnly))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            connectors_dict[instance] = responses[i]['content']
        
        self.connectors = connectors_dict
        
        return connectors_dict
    
    async def get_cluster_details_from_instances(self, instances: List[str] = None):
        """
        Retrieves cluster details from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing cluster details.
            
        Raises:
            Exception: If the request for cluster details fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_cluster_details = async_wrap(self.get_cluster_details)
        
        cluster_details_dict = {}
        
        for instance in instances:
            tasks.append(async_get_cluster_details(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            cluster_details_dict[instance] = responses[i]['content']
        
        self.clusterDetails = cluster_details_dict
        
        return cluster_details_dict
    
    async def get_job_results_from_instances(self, instances: List[str] = None, size: int = 1000, jobId: str = None):
        """
        Retrieves job results from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            size (int, optional): The number of results to retrieve. Defaults to 1000.
            jobId (str, optional): The ID of the job. Defaults to None.
            
        Returns:
            dict: The response JSON containing job results.
            
        Raises:
            Exception: If the request for job results fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_job_results = async_wrap(self.get_job_results)
        
        job_results_dict = {}
        
        for instance in instances:
            tasks.append(async_get_job_results(Dwinstancename=instance, size=size, jobId=jobId))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            job_results_dict[instance] = responses[i]['content']
        
        self.jobResults = job_results_dict
        
        return job_results_dict

    async def get_workspaces_from_instances(self, instances: List[str] = None):
        """
        Retrieves workspace information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing workspace details.
            
        Raises:
            Exception: If the request for workspaces fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []

        async_get_workspaces = async_wrap(self.get_workspaces)
        
        for instance in instances:
            tasks.append(async_get_workspaces(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        workspaces_dict = {}
        for i, instance in enumerate(instances):
            workspaces_dict[instance] = responses[i]['content']
        
        self.workspaces = workspaces_dict
        
        return workspaces_dict
    
    async def get_all_tenant_details(self):
        
        tasks = [
            self.get_rules_from_instances(),
            self.get_groups_from_instances(),
            self.get_jobs_from_instances(),
            self.get_connectors_from_instances(),
            self.get_cluster_details_from_instances(),
            self.get_job_results_from_instances(),
            self.get_workspaces_from_instances()
        ]
        
        result_dict = {}
        
        result = await asyncio.gather(*tasks)
        
        for i, instance in enumerate(self.instances):
            result_dict[instance['instanceName']] = {
                'rules': result[0][instance['instanceName']],
                'groups': result[1][instance['instanceName']],
                'jobs': result[2][instance['instanceName']],
                'connectors': result[3][instance['instanceName']],
                'clusterDetails': result[4][instance['instanceName']],
                'jobResults': result[5][instance['instanceName']],
                'workspaces': result[6][instance['instanceName']]
            }
        
        return result_dict