from sys import platform
import numpy as np
import pandas as pd
import os
from simple_salesforce import Salesforce
from simple_salesforce import SalesforceLogin
from salesforce_bulk import SalesforceBulk
from sfdclib import SfdcSession
from sfdclib import SfdcMetadataApi
from sfdclib import SfdcToolingApi
import re
import time
import json
from salesforce_bulk.util import IteratorBytesIO
import pandas as pd
import requests
import base64
from typing import List, Tuple, Optional, Union, Type, Callable
from collections import OrderedDict
import sys
import zeep
import datetime
import ast
sys.path.append("..")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    from custom_exceptions.salesforce_exceptions import *
    from utilities.df_utils import *
    from utilities.async_utils import *
    from utilities.sf_query_processors import *
    from decorators import *
except:
    from salesforce.custom_exceptions.salesforce_exceptions import *
    from salesforce.utilities.df_utils import *
    from salesforce.utilities.async_utils import *
    from salesforce.utilities.sf_query_processors import *
    from salesforce.decorators import *
import asyncio
from functools import wraps, partial
from pandas import json_normalize




class Sf:
    _REGEX_PARSE_SOQL_FIELDS = "(?<=select)(.*?)(?<!, )(?=from)"
    _REGEX_PARSE_SOQL_OBJECT = "(?<!, from )(?<=from )\w*"
    
    def __init__(self) -> None:
        self.filename: str = None
        self.os_platform: str = platform
        self.credentials: pd.DataFrame = pd.DataFrame()
        self.sfUsername: str = None
        self.sfPassword: str = None
        self.sfOrgId: str = ""
        self.isSandbox: bool = None
        self.session_id: str = None
        self.instance: str = None
        self.domain: str = None
        self.security_token: str = ''
        self.sf: Salesforce = None
        self.bulk: SalesforceBulk = None
        self.sfMeta: SfdcMetadataApi = None
        self.tooling: SfdcToolingApi = None
        self.api_version: str = 'v52.0'
        self.record_count: dict = {}
        self.record_count_caseinsensitive: dict = {}
        self.debug: bool = False
        self.veeva_common:dict = None
        self.org_info:dict = None
        self.sfdc_limits: dict = None
        
    @staticmethod
    def sf15to18 (id):
        if not id:
            raise ValueError('No id given.')
        if not isinstance(id, str):
            raise TypeError('The given id isn\'t a string')
        if len(id) == 18:
            return id
        if len(id) != 15:
            raise ValueError('The given id isn\'t 15 characters long.')

        # Generate three last digits of the id
        for i in range(0,3):
            f = 0

            # For every 5-digit block of the given id
            for j in range(0,5):
                # Assign the j-th chracter of the i-th 5-digit block to c
                c = id[i * 5 + j]

                # Check if c is an uppercase letter
                if c >= 'A' and c <= 'Z':
                    # Set a 1 at the character's position in the reversed segment
                    f += 1 << j

            # Add the calculated character for the current block to the id
            id += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012345'[f]

        return id
    
    def authenticate(self, sfUsername: Optional[str]=None, 
                                sfPassword: Optional[str]=None, 
                                sfOrgId: Optional[str]=None, 
                                isSandbox: Optional[bool]=None, 
                                session_id: Optional[str]=None, 
                                instance: Optional[str]=None, 
                                security_token: Optional[str] = None,
                                domain: Optional[str] = None,
                                if_return: Optional[bool] = False,
                                *args, **kwargs) -> Optional[dict]:
        """
        Authenticates Salesforce and retrieves the auth token.

        Dependencies:
            from simple_salesforce import Salesforce
            from simple_salesforce import SalesforceLogin
            from salesforce_bulk import SalesforceBulk
            from sfdclib import SfdcSession
            from sfdclib import SfdcMetadataApi
            from sfdclib import SfdcToolingApi
        """
        
        sfUsername = self.sfUsername if sfUsername is None else sfUsername
        sfPassword = self.sfPassword if sfPassword is None else sfPassword
        sfOrgId = self.sfOrgId if sfOrgId is None else sfOrgId
        isSandbox = self.isSandbox if isSandbox is None else isSandbox
        session_id = self.session_id if session_id is None else session_id
        instance = self.instance if instance is None else instance
        security_token = self.security_token if security_token is None else security_token
        domain = self.domain if domain is None else domain
        
        # If session ID already exists and instance URL is already populated,
        # reauthenticate using existing session ID
        if session_id is not None and instance is not None:
            sf = Salesforce(session_id = session_id, instance = instance)
            self.sf = sf
            self.instance = instance
            self.session_id = session_id
        
        # If username, password, org ID, and isSandbox flags are all provided,
        # authenticate using provided credentials
        elif sfUsername is not None and sfPassword is not None and sfOrgId is not None and isSandbox is not None:
            
            # SFDC Sandbox authentication
            if isSandbox:
                self.domain = 'test'
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token = self.security_token,domain='test')
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token,
                domain= self.domain)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
                self.sfUsername = sfUsername
                self.sfPassword = sfPassword
                self.load_org_info()
                self.sfOrgId = self.org_info['Id'][0]
                self.isSandbox = isSandbox
                
            else:
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token=self.security_token)
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
                self.sfUsername = sfUsername
                self.sfPassword = sfPassword
                self.load_org_info()
                self.sfOrgId = self.org_info['Id'][0]
                self.isSandbox = isSandbox
                
        else:
            raise Exception('Either sfUsername, sfPassword, sfOrgId and isSandbox must be populated, OR session_id and instance must be populated.')

        # Alternative way to authenticate using SFDC Bulk API
        # bulk = SalesforceBulk(username=sfUsername, password=sfPassword, security_token='')
        bulk = SalesforceBulk(sessionId = self.session_id, host = self.instance)
        self.bulk = bulk
        # SFDC Metadata API
        sf_meta_instance = ""
        if self.instance.__contains__("my.salesforce.com"):
            sf_meta_instance = self.instance.replace("my.salesforce.com","my")
        else:
            sf_meta_instance = ".".join(self.instance.split(".")[:2])
            
        sfMeta = SfdcSession(session_id=self.session_id, instance=sf_meta_instance)
        self.sfMeta = sfMeta
        # Alternative way to authenticate using SFDC Metadata API
        # sfMeta = SfdcSession(username=sfUsername,password=sfPassword,token='',is_sandbox=isSandbox)
        sfMeta._api_version = "54.0"
        tooling = SfdcToolingApi(sfMeta)
        self.tooling = tooling
        
        self.api_version = 'v' + self.sf_api_call('/services/data')[-1]['version']
        
        for x in self.sf_api_call('/services/data/'+self.api_version+'/limits/recordCount')['sObjects']:
            self.record_count[x['name']] = x['count']
            self.record_count_caseinsensitive[x['name'].lower()] = x['count']
        
        self.sfdc_limits = self.parse_sf_limits(self.sf_api_call('/services/data/'+self.api_version+'/limits'))
        
        
        if if_return:
            return {'sf':sf, 
                    'bulk':bulk, 
                    'sfMeta': sfMeta, 
                    'tooling':tooling, 
                    'session_id':session_id, 
                    'instance':instance, 
                    'sfMeta_is_connected':sfMeta.is_connected(), 
                    'bulk_api_sessionId':bulk.sessionId}

    ### ----------------------------------------------------------------------------------------------------
    ### Synchronous Data Functions
    ### ----------------------------------------------------------------------------------------------------

    def query(self, query: str, excludedFields: Optional[List] = [], *args) -> pd.DataFrame:
        """
        Using SFDC SOQL Syntax, and allowing for Relationships and group bys. 
        
        Arguments:
            query (str): A Standard SFDC SOQL Query allowing for relationships (Owner.Name)
                Asterisks(*) represents all queryable fields and can be used in conjunction
                with other relationship fields. 
                i.e. (Select *, Owner.Profile.Name, Owner.Name From Account)
        
        Returns:
            Pandas Dataframe Object.
        
        Raises:
            KeyError: Typically raised when 0 records exist for the object
                
            badfield: A self-correcting error that is raised when a field is unqueriable, i.e. Address Fields
            
            Exception: When relationship query contains more than 4 layers, an Exception is raised.
            i.e. Parent_Account_vod__r.Owner.Profile.LastModifiedBy.Name (<- a 5 layer deep relationship is not supported)
        
        Example of Usage:
            sf.query("Select *, Owner.Profile.Name From Account ORDER BY CreatedDate DESC LIMIT 100")
            
            return:
            A Pandas Dataframe of the last created 100 account records, with all queriable fields included in the query and a relationship field.
            
        """
        objectName = re.search(self._REGEX_PARSE_SOQL_OBJECT, query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                final_query = query.replace("*", ", ".join(results))                
                query_response = self.sf.query_all(final_query)
                # if the object has 0 records in Salesforce, return empty dataframe
                if query_response['totalSize'] == 0:
                    fields_preparsed = re.search(self._REGEX_PARSE_SOQL_FIELDS, query,  re.IGNORECASE).group(0).split(",")
                    return pd.DataFrame(columns=fields_preparsed)
                else:
                    result = pd.DataFrame(query_response)['records']
                    for _ in result:
                        del _['attributes']
                    successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
            
            result = result.apply(lambda x: pd.Series(x)).copy()

            relationship_fields_preparsed = re.search(self._REGEX_PARSE_SOQL_FIELDS, query,  re.IGNORECASE).group(0).split(",")
            # relationship_fields_prepared Example:
            # ['*',
            #  ' Parent_Account_vod__r.Owner.Profile.Name',
            #  ' Child_Account_vod__r.Owner.Profile.Name',
            #  'Parent_Account_vod__r.Owner.Profile.Id ']

            relational_fields = [{x.strip(): x.strip().split(".")} for x in relationship_fields_preparsed if "." in x]
            # relationship_fields Example:
            # [{'Parent_Account_vod__r.Owner.Profile.Name': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Child_Account_vod__r.Owner.Profile.Name': ['Child_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Parent_Account_vod__r.Owner.Profile.Id': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Id']}]

            columns_to_remove = set()
            for x in relational_fields:
                if len(list(x.values())[0]) > 4:
                    raise Exception("Too Many Relationship Levels. The Query you have entered contains more than 4 levels deep and is not supported.")
                elif len(list(x.values())[0]) == 4:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]][list(x.values())[0][3]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 3:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 2:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]])
                    columns_to_remove.add(list(x.values())[0][0])
            result.drop(columns_to_remove, axis=1, inplace=True)
            result.replace(np.nan, None, inplace=True)        

                
        return result

    def create(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function creates records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be created.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing all the required fields for a record.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the create request was successful
            created: boolean: this value should always be False in a create request
            id: object[str]: this value typically is None in a create request
            statusCode: object[str] - Optional: the error code of the create operation if failed
            message: object[str] - Optional: the error message of the create operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpdate
        """
        if (object_api is None) or (len(record_dataframe) == 0):
            raise RequiredValuesNotProvidedDuringCreate()
        else:
            result = getattr(self.sf.bulk, object_api).insert(record_dataframe.to_dict('records'), batch_size=10000, use_serial=False)
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))

    def delete(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function deletes records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be deleted from.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing at least 1 column with an Id column (case sensitive)

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the delete request was successful
            created: boolean: this value should always be False in a delete request
            id: object[str]: this value typically is None in a delete request
            statusCode: object[str] - Optional: the error code of the delete operation if failed
            message: object[str] - Optional: the error message of the delete operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringDelete
        """
        if (object_api is None) or (len(record_dataframe) == 0) or record_dataframe.columns.__contains__('Id') == False:
            raise RequiredValuesNotProvidedDuringDelete()
        else:
            result = getattr(self.sf.bulk, object_api).delete(record_dataframe['Id'].to_frame().to_dict('records'))
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))
    
    def update(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function updates records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be updated.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing at least 1 column with an Id column (case sensitive)
            and additional columns matching the Salesforce field api names.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the update request was successful
            created: boolean: this value should always be False in a update request
            id: object[str]: this value typically is None in a update request
            statusCode: object[str] - Optional: the error code of the update operation if failed
            message: object[str] - Optional: the error message of the update operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpdate
        """

        field_metadata = self.field_describe([object_api],attributes=['name','type','updateable','compoundFieldName'])

        if ((object_api is None) or 
        (len(record_dataframe) == 0)):
            raise RequiredValuesNotProvidedDuringUpdate(message="Object API and Record Dataframe are required, ensure your record dataframe has at least 1 row and 1 column with an Id column")
        elif record_dataframe.columns.__contains__('Id') == False:
            raise RequiredValuesNotProvidedDuringUpdate(message="Record Dataframe must have an Id column")
        elif ~record_dataframe.columns.isin(field_metadata[object_api]).all():
            # checks whether any of the columns in the dataframe passed in are not valid field API names
            raise RequiredValuesNotProvidedDuringUpdate(message="One of the columns in the record dataframe is not a valid field for the object")
        elif record_dataframe.columns.isin(field_metadata[(field_metadata['Updateable'] == False) & (field_metadata[object_api] != "Id")][object_api]).any():
            # checks whether any of the columns in the dataframe passed in are not updateable
            non_updatable_fields = list(set(record_dataframe.columns) - set(field_metadata[(field_metadata['Updateable'] == True) | (field_metadata[object_api] == "Id")][object_api]))
            raise RequiredValuesNotProvidedDuringUpdate(message=f"The following fields are not updatable: {', '.join(non_updatable_fields)}")
        elif record_dataframe.columns.isin(field_metadata[(~field_metadata['Compoundfieldname'].isnull()) & (field_metadata['Compoundfieldname'] != 'Name')][object_api]).any():
            # checks whether any of the columns in the dataframe passed in are compound fields
            compound_fields = list(set(record_dataframe.columns) & set(field_metadata[(~field_metadata['Compoundfieldname'].isnull()) & (field_metadata['Compoundfieldname'] != 'Name')][object_api]))
            raise RequiredValuesNotProvidedDuringUpdate(message=f"The following fields are compound fields, which are not updatable: {', '.join(compound_fields)}")
        # checks whether an reference (lookup/master-detail) field is included in the source dataframe
        #  or ~record_dataframe.columns.isin(field_metadata[field_metadata['Type'] == 'reference'][object_api]).any()
            
        else:
            record_dataframe.replace(np.nan, None, inplace=True)
            result = getattr(self.sf.bulk, object_api).update(record_dataframe.to_dict('records'), batch_size=10000, use_serial=False)
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))

    def upsert(self, object_api: str=None, external_id_field_api: str="", record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function upserts records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be upserted into.

        external_id_field_api: str: API name of the external ID field used for the upsert operation.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing the External column (case sensitive)
            and additional columns matching the Salesforce field api names.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the upsert request was successful
            created: boolean: this value should always be False in a upsert request
            id: object[str]: this value typically is None in a upsert request
            statusCode: object[str] - Optional: the error code of the upsert operation if failed
            message: object[str] - Optional: the error message of the upsert operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpsert
            SalesforceMalformedRequest
        """

        field_metadata = self.field_describe([object_api], ['name', 'type', 'length','externalId','updateable','compoundFieldName'])
            
            
        if ((object_api is None) or 
        (len(record_dataframe) == 0)):
            raise RequiredValuesNotProvidedDuringUpdate(message="Object API and Record Dataframe are required, ensure your record dataframe has at least 1 row and 1 column with an Id column")
        elif ~record_dataframe.columns.isin(field_metadata[object_api]).all():
            # checks whether any of the columns in the dataframe passed in are not valid field API names
            raise RequiredValuesNotProvidedDuringUpdate(message="One of the columns in the record dataframe is not a valid field for the object")
        elif external_id_field_api == "":
            raise RequiredValuesNotProvidedDuringUpsert(message="External ID field API is required")
        elif record_dataframe.columns.isin(field_metadata[(field_metadata['Updateable'] == False) & (field_metadata[object_api] != "Id")][object_api]).any():
            # checks whether any of the columns in the dataframe passed in are not updateable
            non_updatable_fields = list(set(record_dataframe.columns) - set(field_metadata[(field_metadata['Updateable'] == True) | (field_metadata[object_api] == "Id")][object_api]))
            raise RequiredValuesNotProvidedDuringUpdate(message=f"The following fields are not updatable: {', '.join(non_updatable_fields)}")
        elif record_dataframe.columns.isin(field_metadata[(~field_metadata['Compoundfieldname'].isnull()) & (field_metadata['Compoundfieldname'] != 'Name')][object_api]).any():
            # checks whether any of the columns in the dataframe passed in are compound fields
            compound_fields = list(set(record_dataframe.columns) & set(field_metadata[(~field_metadata['Compoundfieldname'].isnull()) & (field_metadata['Compoundfieldname'] != 'Name')][object_api]))
            raise RequiredValuesNotProvidedDuringUpdate(message=f"The following fields are compound fields, which are not updatable: {', '.join(compound_fields)}")
        else:
            record_dataframe.replace(np.nan, None, inplace=True)
            result = getattr(self.sf.bulk, object_api).upsert(record_dataframe.to_dict('records'), external_id_field_api, batch_size=10000, use_serial=False)
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result)

    def extract_bulk(self, og_query: str, 
                        excludedFields: Optional[List] = []) -> pd.DataFrame:
        """
        Uses a standard SOQL query to extract Salesforce Data and outputs a pandas dataframe
        
        Dependencies:
            import re
            import time
            import json
            from salesforce_bulk.util import IteratorBytesIO
            import pandas as pd
        
        """
        objectName = re.search(self._REGEX_PARSE_SOQL_OBJECT, og_query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                query = og_query.replace("*", ", ".join(results))
                
#                 # if the object has 0 records in Salesforce, return empty dataframe
#                 if objectName not in self.record_count_caseinsensitive.keys():
#                     return pd.DataFrame(columns=results)
                    
                job = self.bulk.create_query_job(objectName, contentType='JSON')
                batch = self.bulk.query(job, query)
                while not self.bulk.is_batch_done(batch):
                    time.sleep(1)
                sfdf = pd.DataFrame()
                for result in self.bulk.get_all_results_for_query_batch(batch):
                    result = json.load(IteratorBytesIO(result))
                    sfdf = pd.concat([sfdf, pd.DataFrame(result)])

                # drops attributes column in dataframe
                sfdf.drop(columns="attributes", inplace = True)

                # formats all datetime to the proper formatting
                for column in sfdf:
                    if schemaDict[column]['type'] == 'datetime':
                        sfdf[column] = pd.to_datetime(sfdf[column], unit='ms')
                    # if the column has a 'scale' or salesforce's decimal places, then turn the column into an int
                    elif schemaDict[column]['type'] == 'double' and schemaDict[column]['scale'] == 0:
                        sfdf[column] = pd.to_numeric(sfdf[column], downcast='integer')

            #                         pd.to_datetime(sfdf[column], unit = 's')
            #                         sfdf[column].apply(lambda x : datetime.fromtimestamp(int(x), tz).isoformat())
            #                 sfdf.convert_dtypes()
                # converts the output of the bulk query to text so that the unix timestamp displays property, and fills and empty values with the '' string.
                sfdf = sfdf.fillna('').astype(str)
                successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if og_query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
        if self.debug:
            print("Extracted " + objectName + " successfully!")
        return sfdf
    
    def entity_access_query(self, entity_type):
        # Retrieves information about which Profile or PermissionSet
        # grants permission to which Setup Entity (i.e. ApexPage, ApexClass, TabSets, etc)
        
        entity_access = transform_sf_result_set_rec(self.sf.query_all(f"""
        SELECT Id, Parent.Id, Parent.ProfileId, Parent.Profile.Name, Parent.Name,SetupEntityId,SetupEntityType FROM
        SetupEntityAccess WHERE SetupEntityType = '{entity_type}'""")['records'])
        # entity_access.drop(columns=['PermissionSet.Profile'], inplace=True)
        return {entity_type: entity_access}

    ### ----------------------------------------------------------------------------------------------------
    ### Asynchronous Data Functions
    ### ----------------------------------------------------------------------------------------------------

    async def async_query(self, query, excludedFields: Optional[List] = []) -> pd.DataFrame:
        async_query = async_wrap(self.query)
        return await async_query(query, excludedFields)
    
    async def async_queries(self, queries: List[str]):
        async_queries = async_wrap(self.sf.query_all)
        result_list = await asyncio.gather(*[async_queries(query) for query in queries])
        result_pd_list = [transform_sf_result_set_rec(result['records']) for result in result_list]
        return result_pd_list


    async def async_upsert(self, object_api, record_dataframe, external_id_field_api, batchsize=2000, *args, **kwargs):
        async_upsert = async_wrap(self.upsert)
        batches = len(record_dataframe) / batchsize
        result_list = await asyncio.gather(*[async_upsert(object_api= object_api, record_dataframe=batch, external_id_field_api=external_id_field_api) for batch in np.array_split(record_dataframe, batches)])
        return pd.concat(result_list).reset_index(drop=True)

    async def async_update(self, object_api, record_dataframe, batchsize=2000, *args, **kwargs):
        async_update = async_wrap(self.update)
        batches = len(record_dataframe) / batchsize
        result_list = await asyncio.gather(*[async_update(object_api= object_api, record_dataframe=batch) for batch in np.array_split(record_dataframe, batches)])
        return pd.concat(result_list).reset_index(drop=True)

    async def async_create(self, object_api, record_dataframe, batchsize=2000, *args, **kwargs):
        async_create = async_wrap(self.create)
        batches = len(record_dataframe) / batchsize
        result_list = await asyncio.gather(*[async_create(object_api= object_api, record_dataframe=batch) for batch in np.array_split(record_dataframe, batches)])
        return pd.concat(result_list).reset_index(drop=True)

    async def async_delete(self, object_api, record_dataframe, batchsize=2000, *args, **kwargs):
        async_delete = async_wrap(self.delete)
        batches = len(record_dataframe) / batchsize
        result_list = await asyncio.gather(*[async_delete(object_api= object_api, record_dataframe=batch) for batch in np.array_split(record_dataframe, batches)])
        return pd.concat(result_list).reset_index(drop=True)
    
    async def async_get_user_password_status(self, user_ids: list[str]) -> dict:
        async_sf_api_call = async_wrap(self.sf_api_call)
        response = await asyncio.gather(*[async_sf_api_call(f'/services/data/{self.api_version}/sobjects/User/{user_id}/password', method='GET') for user_id in user_ids])
        # Return a dict
        response = {user_id: result for user_id, result in zip(user_ids, response)}
        return response
    
    
    
    ### ----------------------------------------------------------------------------------------------------
    ### Asynchronous Metadata Functions
    ### ----------------------------------------------------------------------------------------------------
    async def async_get_non_updatable_fields(self, object_name: str):
        """
        Returns a list of fields that cannot be updated.
        """
        async_field_describe =  async_wrap(self.field_describe)
        field_metadata = await async_field_describe([object_name], attributes=['name','updateable'])
        non_updatable_fields = list(field_metadata[field_metadata['Updateable'] == False][object_name])[1:]
        return non_updatable_fields

    async def async_get_compound_field_names(self, object_name: str, include_name_compound_fields: bool=False):
        """
        Returns a list of compound fields. By default "Name" compound field names are excluded.
        To return a list of compound fields including "Name" fields, set include_name_compound_fields to True.

        Compound field names are fields that are composed of multiple fields. These fields are not updatable directly via the API
        and may cause errors if updated directly.
        """
        async_field_describe =  async_wrap(self.field_describe)
        field_metadata = await async_field_describe([object_name], attributes=['name','compoundFieldName'])

        if include_name_compound_fields:
            compound_field_names = list(field_metadata[(~field_metadata['Compoundfieldname'].isnull())][object_name])
        elif include_name_compound_fields==False:
            compound_field_names = list(field_metadata[(~field_metadata['Compoundfieldname'].isnull()) & (field_metadata['Compoundfieldname'] != 'Name')][object_name])
        else:
            raise ValueError('include_name_compound_fields must be a boolean.')
        return compound_field_names
    
    async def get_picklist_values_by_object_record_type(self, object: str):
        object_record_type_ids = self.query(f"Select Id, Name From RecordType Where SobjectType = '{object}'").apply(lambda row: {"Id": row['Id'], "Name": row['Name']}, axis=1)
        if len(object_record_type_ids) == 0:
            object_record_type_ids = pd.Series([{"Id": "012000000000000AAA", "Name": "Master"}]).to_list()
        else:
            object_record_type_ids = object_record_type_ids.to_list()
            
        object_describe = self.sf_api_call(f"/services/data/{self.api_version}/ui-api/object-info/{object}")['fields']
        controlling_fields = []
        for field, values in object_describe.items():
            controlling_fields.append({"Field": field, "Controlling Field": "" if values['controllingFields'] == [] else "; ".join(values['controllingFields'])})
        controlling_fields = pd.DataFrame(controlling_fields)

        def record_type_picklist_retriever(self, object, record_type_id, record_type_name):
            result = []
            picklist_metadata = self.sf_api_call(f"/services/data/{self.api_version}/ui-api/object-info/{object}/picklist-values/{record_type_id}")['picklistFieldValues']
            if len(picklist_metadata) == 0:
                return pd.DataFrame(columns=['attributes',
                                    'label',
                                    'validFor',
                                    'value',
                                    'Field_API',
                                    'defaultValueLabel',
                                    'defaultValueValue',
                                    'Controlling Field',
                                    'RecordTypeName',
                                    'Object'])
                
            for key, value in picklist_metadata.items():
                result.append({"Field_API": key, "controllerValues": value['controllerValues'], "defaultValue":  value['defaultValue'], "values": value['values']})
            final_result_pd = json_normalize(result, ['values'], ['defaultValue', 'controllerValues', 'Field_API'])
            ## Converts the validFor numerical codes i.e. [0,2] to it's corresponding text values by looking it up on the controllerValues column i.e. {'Web': 0, 'Phone Inquiry': 1, 'Partner Reference': 2 ... }
            ## [0,2] -> ['Web', 'Partner Reference']
            final_result_pd['validFor'] = final_result_pd.apply(lambda row: "\n".join([{v: k for k, v in row['controllerValues'].items()}[value] for value in row['validFor']]), axis=1)
            final_result_pd.drop(columns=['controllerValues'], inplace=True)
            
            try:
                final_result_pd[['defaultValueLabel', 'defaultValueValue']] = json_normalize(final_result_pd['defaultValue'])[['label','value']]
            except:
                final_result_pd[['defaultValueLabel', 'defaultValueValue']] = [np.nan, np.nan]
            
            final_result_pd.drop(columns=['defaultValue'], inplace=True)
            final_result_pd = pd.merge(final_result_pd, controlling_fields, left_on='Field_API', right_on='Field', how='left').drop(columns=['Field']).copy()
            final_result_pd['RecordTypeName'] = record_type_name
            final_result_pd['Object'] = object
            return final_result_pd

        async_picklist_rt_retrieve = async_wrap(record_type_picklist_retriever)
        results = pd.concat(await asyncio.gather(*[async_picklist_rt_retrieve(self, object, record_type_id['Id'], record_type_id['Name']) for record_type_id in object_record_type_ids]))
        results = results[['Object', 'RecordTypeName', 'Field_API', 'Controlling Field', 'defaultValueLabel', 'defaultValueValue', 'label', 'value', 'validFor']]
        return results


    async def object_permission_bulk_check(self, objects: list, permissions: list ):
        async_object_permission_check = async_wrap(self.object_permission_check)
        result_list = await asyncio.gather(*[async_object_permission_check(object, permission ) for object in objects for permission in permissions])
        # for result in result_list:
        #     data = deep_merge_dictionaries(data, result)
        result_list = [item for sublist in result_list for item in sublist]
        return result_list

    async def field_permission_bulk_check(self, objects: list, ) -> dict[str, pd.DataFrame]:
        async_field_permission_check = async_wrap(self.field_permission_check)
        result_list = await asyncio.gather(*[async_field_permission_check( object ) for object in objects])
        # for result in result_list:
        #     data = deep_merge_dictionaries(data, result)
        profile_list = [item['profilePermissions'] for item in result_list]
        permissionSet_list = [item['permissionSetPermissions'] for item in result_list]
        result_dict = {'profilePermissions': pd.concat(profile_list), 'permissionSetPermissions': pd.concat(permissionSet_list)}
        
        return result_dict
    
    async def async_set_user_passwords(self, user_id_password_list_dict: dict) -> dict:
        async_set_user_password = async_wrap(self.set_user_password)
        results = await asyncio.gather(*[async_set_user_password(user_id, password) for user_id, password in user_id_password_list_dict.items()])
        results = {result['user_id']: result['message'] for result in results}
        return results

    async def entity_access_bulk_query(self, entity_types: list):
        async_entity_access_query = async_wrap(self.entity_access_query)
        results = await asyncio.gather(*[async_entity_access_query(entity_type) for entity_type in entity_types])
        merged_dict = {}
        for result in results:
            for key, value in result.items():
                merged_dict[key] = value
        return merged_dict

    async def apex_pages_profiles_and_permission_set_access_query(self, apex_pages_to_check: list[str]):
        query_results = await self.entity_access_bulk_query(['ApexPage'])

        entity_access_apex_pages_async =  query_results['ApexPage']

        entity_permission_set_access_apex_pages_async = entity_access_apex_pages_async[entity_access_apex_pages_async['Profile.Name'].isna()]
        entity_profile_access_apex_pages_async = entity_access_apex_pages_async[entity_access_apex_pages_async['Profile.Name'].notna()]

        # filter = ['Scheduler_Administration_vod','Network_Admin_Page_vod','searchAccts_vod']
        filter_join = "','".join(apex_pages_to_check)
        where_clause = f" WHERE Name IN ('{filter_join}')"
        apex_pages_query = transform_sf_result_set_rec(self.sf.query_all(f"""
            SELECT Id, Name From ApexPage{where_clause}""")['records'])

        permission_sets_with_apex_page_access = entity_permission_set_access_apex_pages_async[entity_permission_set_access_apex_pages_async['SetupEntityAccess.SetupEntityId'].isin(apex_pages_query['ApexPage.Id'].unique())]
        profiles_with_apex_page_access = entity_profile_access_apex_pages_async[entity_profile_access_apex_pages_async['SetupEntityAccess.SetupEntityId'].isin(apex_pages_query['ApexPage.Id'].unique())]
        permission_sets_with_apex_page_access = pd.merge(permission_sets_with_apex_page_access, apex_pages_query, left_on='SetupEntityAccess.SetupEntityId', right_on='ApexPage.Id', how='inner').drop(columns=['ApexPage.Id'], axis=1)
        profiles_with_apex_page_access = pd.merge(profiles_with_apex_page_access, apex_pages_query, left_on='SetupEntityAccess.SetupEntityId', right_on='ApexPage.Id', how='inner').drop(columns=['ApexPage.Id'], axis=1)

        profiles_with_apex_page_access = profiles_with_apex_page_access[['PermissionSet.ProfileId','Profile.Name','SetupEntityAccess.SetupEntityType','ApexPage.Name']]
        profiles_with_apex_page_access.columns = ['Profile Id', 'Profile Name', 'Setup Entity Type', 'Visualforce (Apex) Name']
        
        permission_sets_with_apex_page_access = permission_sets_with_apex_page_access[['PermissionSet.Id','PermissionSet.Name','SetupEntityAccess.SetupEntityType','ApexPage.Name']]
        permission_sets_with_apex_page_access.columns = ['PermissionSet Id', 'PermissionSet Name', 'Setup Entity Type', 'Visualforce (ApexPage) Name']
        
        return {'profiles_with_apex_page_access': profiles_with_apex_page_access, 'permission_sets_with_apex_page_access': permission_sets_with_apex_page_access}

    # Retrieves the Page Layout by Profile by Record Type data for listed objects in the org
    async def retrieve_profile_layout_record_type_matrix_by_objects(self, objects_to_retrieve_profile_layout_matrix = ['Account','Address_vod__c','Child_Account_vod__c'], discard_unqueriable_objects = False, return_pivot_table = False):
        
        objects_to_retrieve = [object[:-3] if object.endswith('__c') else object for object in objects_to_retrieve_profile_layout_matrix]
        
        # Objects in the Profile Layout table's TableEnumOrId column where the value is an object name instead of an object ID
        
        ENUM_OBJECTS = {'Account', 'AccountTeamMember', 'Asset', 'AuthorizationForm', 'AuthorizationFormConsent', 'BusinessBrand', 'Campaign', 'CampaignMember', 'Case',
                            'CaseClose', 'CaseInteraction', 'CommunityMemberLayout', 'Contact', 'ContactPointAddress', 'ContactPointEmail', 'ContactPointPhone', 'ContentVersion', 'Contract', 'Customer', 'DelegatedAccount',
                            'DuplicateRecordItem', 'DuplicateRecordSet', 'EmailMessage', 'Event', 'FeedItem', 'Global', 'Idea', 'Individual', 'Lead', 'Macro', 'ObjectTerritory2AssignmentRule',
                            'Opportunity', 'OpportunityLineItem', 'Order', 'OrderItem', 'PersonAccount', 'Pricebook2', 'PricebookEntry', 'ProcessException', 'Product2',
                            'ProfileSkill', 'ProfileSkillEndorsement', 'ProfileSkillUser', 'QuickText', 'Scorecard', 'ScorecardAssociation', 'ScorecardMetric', 'Seller', 'ServiceAppointmentGroup',
                            'ServiceTerritoryRelationship', 'SignupRequest', 'SocialPersona', 'SocialPost', 'Solution', 'Task', 'Territory2', 'Territory2Model', 'Territory2Type', 'User',
                            'UserAlt', 'UserProvAccount', 'UserProvisioningLog', 'UserProvisioningRequest', 'UserTerritory2Association', 'WorkProcedure', 'WorkProcedureStep', 'WorkTypeExtension'}
        
        # Objects that returns empty results if queried via the WHERE clause using Salesforce Tooling API.
        # i.e. "Select LayoutId from ProfileLayout where TableEnumOrId = 'DelegatedAccount'" returns empty results.
        UNQUERIABLE_ENUM_OBJECTS = {'DelegatedAccount','ProfileSkill','ProfileSkillEndorsement','ProfileSkillUser','ServiceTerritoryRelationship','WorkTypeExtension'}
        
        
        
        object_dataframe = pd.DataFrame(self.tooling_query_all("Select DeveloperName from CustomObject"))
        object_dataframe['ObjectID'] = object_dataframe.apply(lambda row: row['attributes']['url'].split('/')[-1] if row['attributes']['url'] else "", axis=1)
        
        profile_layout_queries = []
        
        for object_name in objects_to_retrieve:
            if object_name in UNQUERIABLE_ENUM_OBJECTS and discard_unqueriable_objects == False:
                raise Exception("Unqueriable object: " + object_name + ". Please use retrieve_profile_layout_record_type_matrix_all() instead or set discard_unqueriable_objects parameter to True")
            elif object_name in ENUM_OBJECTS:
                profile_layout_queries.append("Select LayoutId, ProfileId, Profile.Name, RecordTypeId, RecordType.Name, Layout.Name, Layout.NamespacePrefix, Layout.TableEnumOrId, TableEnumOrId from ProfileLayout where TableEnumOrId = '" + object_name + "'")
            else:
                object_id = object_dataframe[object_dataframe['DeveloperName'] == object_name]['ObjectID'].values[0]
                profile_layout_queries.append(f"Select LayoutId, ProfileId, Profile.Name, RecordTypeId, RecordType.Name, Layout.Name, Layout.NamespacePrefix, Layout.TableEnumOrId, TableEnumOrId from ProfileLayout where TableEnumOrId = '{object_id}'")

        
        async_tooling_query_all = async_wrap(self.tooling_query_all)
        
        
        await_results = await asyncio.gather(*[async_tooling_query_all(query) for query in profile_layout_queries])
        
        await_result_dataframe = [transform_sf_result_set_rec(result) for result in await_results if len(result) > 0]
        
        account_page_layouts_bulk = pd.concat(await_result_dataframe)

        account_page_layouts_bulk['ProfileName'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Profile']['Name'] if row['ProfileLayout.Profile'] else "", axis=1)
        account_page_layouts_bulk['RecordTypeName'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.RecordType']['Name'] if row['ProfileLayout.RecordType'] else "", axis=1)
        account_page_layouts_bulk['PageLayout'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Layout']['Name'] if row['ProfileLayout.Layout'] else "", axis=1)
        account_page_layouts_bulk['NamespacePrefix'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Layout']['NamespacePrefix'] if row['ProfileLayout.Layout'] else "", axis=1)
        account_page_layouts_bulk['LayoutTableEnumOrId'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Layout']['TableEnumOrId'] if row['ProfileLayout.Layout'] else "", axis=1)

        account_page_layouts_bulk.drop(['ProfileLayout.Profile','ProfileLayout.RecordType','ProfileLayout.Layout'], axis=1, inplace=True)

        object_dataframe['ObjectID'] = object_dataframe.apply(lambda row: row['attributes']['url'].split('/')[-1] if row['attributes']['url'] else "", axis=1)

        account_page_layouts_bulk = account_page_layouts_bulk.merge(object_dataframe, left_on='LayoutTableEnumOrId', right_on='ObjectID', how='left').copy()
        account_page_layouts_bulk['DeveloperName'] = account_page_layouts_bulk.apply(lambda row: row['DeveloperName'] if pd.notnull(row['DeveloperName']) else row['LayoutTableEnumOrId'], axis=1)
        account_page_layouts_bulk.drop(['attributes'], axis=1, inplace=True)
        
        # Fill in the RecordTypeName colum with the Master Record Type Name
        account_page_layouts_bulk['RecordTypeName'] = account_page_layouts_bulk['RecordTypeName'].apply(lambda row: row if row else 'Master')
        # Filter out Deprecated Profiles
        account_page_layouts_bulk = account_page_layouts_bulk[(~account_page_layouts_bulk['ProfileName'].isnull()) & (account_page_layouts_bulk['ProfileName'] != '') & (account_page_layouts_bulk['PageLayout'] != 'Veeva Vpro Unit Testing Layout')].copy()
        
        if self.instance.__contains__("my.salesforce.com"):
            sf_meta_instance = self.instance.replace(".my.salesforce.com","")
        else:
            sf_meta_instance = ".".join(self.instance.split(".")[:1])
        
        account_page_layouts_bulk['Edit Link'] = account_page_layouts_bulk.apply(lambda row: "https://" + sf_meta_instance + ".lightning.force.com/lightning/setup/ObjectManager/" + (row['DeveloperName'] if str(row['ObjectID']) == 'nan' else row['ObjectID']) + "/PageLayouts/" + row['ProfileLayout.LayoutId'] + "/view", axis=1)
        
        if return_pivot_table:
            return account_page_layouts_bulk.pivot(index='ProfileName', columns=['DeveloperName','RecordTypeName'], values='PageLayout')
        else:
            return account_page_layouts_bulk

    async def field_permission_user_check(self, objects: list[str], permissions: list[str], users=None) -> pd.DataFrame:
        # Similar to the field_permission_check function, but this one will return a list of users that have the specified permission on the specified object
        
        # this is to avoid having a mutable default argument
        users = [] if users is None else users
        
        object_query = "','".join(objects)
        permission_query = ' OR '.join([f"({permission} = true)" for permission in permissions])

        relevant_ps_and_profiles = transform_sf_result_set_rec(self.sf.query_all(f"""
                                                SELECT ParentId,
                                                        Field,
                                                        PermissionsEdit,
                                                        PermissionsRead
                                                FROM FieldPermissions
                                                WHERE SObjectType IN ('{object_query}') AND
                                                ({permission_query})
                                                """)['records'])

        relevant_ps_and_profiles['Object API Name'] = relevant_ps_and_profiles['FieldPermissions.Field'].apply(lambda row: row.split('.')[0])
        relevant_ps_and_profiles['Field API Name'] = relevant_ps_and_profiles['FieldPermissions.Field'].apply(lambda row: row.split('.')[1])
        relevant_ps_and_profiles.drop(columns=['FieldPermissions.Field'], inplace=True)

        user_query = (" AND Assignee.UserName IN ('" + "','".join(users) + "')") if len(users) > 0 else ""

        relevant_ps_and_profiles_list = "','".join(relevant_ps_and_profiles['FieldPermissions.ParentId'].unique().tolist())

        data = transform_sf_result_set_rec(self.sf.query_all(f"""SELECT Assignee.Id, Assignee.Name,Assignee.IsActive, 
                                                                Assignee.UserName, PermissionSet.Id, 
                                                                PermissionSet.isOwnedByProfile, PermissionSet.Profile.Name, PermissionSet.Label
                                                                FROM PermissionSetAssignment
                                                                WHERE PermissionSetId
                                                                IN ('{relevant_ps_and_profiles_list}')
                                                                {user_query} AND Assignee.IsActive = TRUE""")['records'])
        
        if len(data) == 0:
            return pd.DataFrame(columns=['UserName', 'Profile', 'Field API Name', 'Object API Name','Permission', 'Permission Set'])
        
        # Retrieve Profile FLS data
        profiles = data[data['PermissionSet.IsOwnedByProfile']]['Profile.Name'].unique().tolist()
        profiles = ['Admin' if x == 'System Administrator' else x for x in profiles]


        async_metadata_read = async_wrap(self.metadata_read)
        profile_metadata_tasks = {}
        profile_metadata_dict = {}

        for profile in profiles:
                profile_metadata_tasks[profile] = asyncio.create_task(async_metadata_read('Profile', profile))


        task_result_list = await asyncio.gather(*profile_metadata_tasks.values())


        for profile in profiles:
                profile_metadata_dict["System Administrator" if profile == 'Admin' else profile] = pd.DataFrame(task_result_list[profiles.index(profile)]['fieldPermissions'][0])
    
        data = data.merge(relevant_ps_and_profiles, left_on='PermissionSet.Id', right_on='FieldPermissions.ParentId', how='left').copy()
        if (len(data) > 0):
                
                profile_violations = data[data['PermissionSet.IsOwnedByProfile']== True][['User.Username', 'Profile.Name']].drop_duplicates().copy()
                # profile_violations = data[data['PermissionSet.IsOwnedByProfile']== True][['User.Username', 'Profile.Name','Field API Name']]
                profile_metadata_pd = pd.concat(profile_metadata_dict.values(), keys=profile_metadata_dict.keys(), names=['Profile', 'Index']).reset_index(level=1, drop=True).reset_index()
                profile_metadata_pd.rename(columns={'Profile': 'Profile.Name'}, inplace=True)
                profile_metadata_pd['Field API Name'] = profile_metadata_pd['field'].str.split('.').str[1]
                profile_metadata_pd['Object API Name'] = profile_metadata_pd['field'].str.split('.').str[0]
                profile_metadata_pd = profile_metadata_pd[profile_metadata_pd['Object API Name'].isin(objects)].copy()
                profile_metadata_pd.drop(columns=['field'], inplace=True)

                # if permission == 'PermissionsEdit':
                #         profile_metadata_pd = profile_metadata_pd[profile_metadata_pd['editable'] == True].copy()
                #         profile_metadata_pd.drop(columns=['editable', 'readable'], inplace=True)
                # elif permission == 'PermissionsRead':
                #         profile_metadata_pd = profile_metadata_pd[profile_metadata_pd['readable'] == True].copy()
                #         profile_metadata_pd.drop(columns=['editable', 'readable'], inplace=True)
                
                profile_violations = profile_violations.merge(profile_metadata_pd, on='Profile.Name', how='left').copy()
                profile_editable = profile_violations[profile_violations['editable'] == True].drop(columns=['editable','readable']).copy()
                profile_editable['Permission'] = 'PermissionsEdit'
                profile_readable = profile_violations[profile_violations['readable'] == True].drop(columns=['editable','readable']).copy()
                profile_readable['Permission'] = 'PermissionsRead'

                profile_fls_final = pd.concat([profile_editable, profile_readable])
                profile_fls_final.columns = ['UserName','Profile','Field API Name','Object API Name','Permission']
                
                permission_set_violations = data[data['PermissionSet.IsOwnedByProfile']== False][['User.Username', 'PermissionSet.Label', 'Object API Name', 'FieldPermissions.PermissionsEdit','FieldPermissions.PermissionsRead','Field API Name']]
                
                ps_editable = permission_set_violations[permission_set_violations['FieldPermissions.PermissionsEdit'] == True].drop(columns=['FieldPermissions.PermissionsEdit','FieldPermissions.PermissionsRead']).copy()
                ps_editable['Permission'] = 'PermissionsEdit'
                ps_readable = permission_set_violations[permission_set_violations['FieldPermissions.PermissionsRead'] == True].drop(columns=['FieldPermissions.PermissionsEdit','FieldPermissions.PermissionsRead']).copy()
                ps_readable['Permission'] = 'PermissionsRead'
                
                ps_fls_final = pd.concat([ps_editable, ps_readable])
                ps_fls_final.columns = ['UserName','Permission Set','Object API Name','Field API Name', 'Permission']
                
                return pd.merge(profile_fls_final, ps_fls_final, on=['UserName','Object API Name', 'Field API Name','Permission'], how='outer')
        else:
                return pd.DataFrame(columns=['UserName', 'Profile', 'Field API Name', 'Object API Name','Permission', 'Permission Set'])

    async def retrieve_user_profile_metadata(self, username: str):
        profile_metadata = pd.DataFrame(zeep.helpers.serialize_object(self.metadata_list("Profile")))
        profile_metadata = profile_metadata[['id', 'fullName']].copy()
        profile_metadata
        user_profile_id = transform_sf_result_set_rec(self.sf.query_all(f"Select Id, ProfileId FROM User WHERE Username = '{username}'")['records'])
        if len(profile_metadata[profile_metadata['id'] == user_profile_id['User.ProfileId'].values[0]]['fullName']) == 0:
            raise Exception("User does not have a retrievable / valid profile")
        else:
            user_profile = profile_metadata[profile_metadata['id'] == user_profile_id['User.ProfileId'].values[0]]['fullName'].values[0]

        async_profile_read = async_wrap(self.metadata_read)
        
        user_profile_metadata = await async_profile_read('Profile', user_profile)

        return user_profile_metadata

    async def retrieve_user_profile_record_type_details(self, username: str, objects: list[str]):
        
        profile_metadata = pd.DataFrame(zeep.helpers.serialize_object(self.metadata_list("Profile")))
        profile_metadata = profile_metadata[['id', 'fullName']].copy()
        profile_metadata
        user_profile_id = transform_sf_result_set_rec(self.sf.query_all(f"Select Id, ProfileId FROM User WHERE Username = '{username}'")['records'])
        if len(profile_metadata[profile_metadata['id'] == user_profile_id['User.ProfileId'].values[0]]['fullName']) == 0:
            raise Exception("User does not have a retrievable / valid profile")
        else:
            user_profile = profile_metadata[profile_metadata['id'] == user_profile_id['User.ProfileId'].values[0]]['fullName'].values[0]

        async_profile_read = async_wrap(self.metadata_read)
        
        user_profile_metadata = async_profile_read('Profile', user_profile)
        
        results = {}
        
        async_object_describe = async_wrap(self.object_describe)
        
        tasks = {}
        
        for object in objects:
            tasks[object] = async_object_describe(object)
        tasks['get_profile_data'] = user_profile_metadata
        
        task_result_list = await asyncio.gather(*tasks.values())
        
        task_result_dict = {}
        
        for object in objects:
            task_result_dict[object] = task_result_list[objects.index(object)]
            
        task_result_dict['get_profile_data'] = task_result_list[-1]
        
        user_rt_visibilities = pd.DataFrame(task_result_dict['get_profile_data']['recordTypeVisibilities'][0])
        user_rt_visibilities['Object'] = user_rt_visibilities['recordType'].apply(lambda x: x.split('.')[0])
        user_rt_visibilities['RecordType'] = user_rt_visibilities['recordType'].apply(lambda x: x.split('.')[1])
        
        for object in objects:
            if object.lower() == 'account':
                object_describe = task_result_dict[object]['recordTypeInfos'].T
                object_record_types = object_describe[object_describe['active'] == True].reset_index()[['name','defaultRecordTypeMapping','developerName','master','recordTypeId']].copy()
                user_object_rt_visibilities = user_rt_visibilities[(user_rt_visibilities['Object'] == object) | (user_rt_visibilities['Object'] == 'PersonAccount')][['default','personAccountDefault','Object','RecordType','visible']].copy()
                
            else:
                object_describe = task_result_dict[object]['recordTypeInfos'].T
                object_record_types = object_describe[object_describe['active'] == True].reset_index()[['name','defaultRecordTypeMapping','developerName','master','recordTypeId']].copy()
                user_object_rt_visibilities = user_rt_visibilities[user_rt_visibilities['Object'] == object][['default','personAccountDefault','Object','RecordType','visible']].copy()

            object_rt_visibility_with_master = pd.merge(user_object_rt_visibilities, object_record_types, left_on='RecordType', right_on='developerName', how='outer')
            object_rt_visibility_with_master['visible'].fillna(False, inplace=True)
            if not object_rt_visibility_with_master['visible'].any():
                object_rt_visibility_with_master.loc[object_rt_visibility_with_master['developerName'] == 'Master', 'visible'] = True
            if not object_rt_visibility_with_master['default'].any():
                object_rt_visibility_with_master.loc[object_rt_visibility_with_master['developerName'] == 'Master', 'default'] = True
                
            visible_object_rt = object_rt_visibility_with_master[object_rt_visibility_with_master['visible'] == True].drop(['defaultRecordTypeMapping'], axis=1)
            results[object] = visible_object_rt
        
        return results
    
    
    async def permissionable_fields_bulk_check(self, object_list):
        permissionable_fields = {}
        nonpermissionable_fields = {}
        async_permissionable_fields =  async_wrap(self.object_describe)
        async_metadata_read = async_wrap(self.metadata_read)
        
        
        task_dict = {}
        task_result_dict = {}
        
        for object_name in object_list:
            task_dict[object_name] = async_permissionable_fields(object_name)
            task_dict[object_name + '_metadata'] = async_metadata_read('CustomObject', object_name)
            
        task_results = await asyncio.gather(*task_dict.values())
        
        for object_name, task_result in zip(task_dict.keys(), task_results):
            task_result_dict[object_name] = task_result
        
        
        for object in object_list:
            permissionable_fields[object] = pd.DataFrame(task_result_dict[object + "_metadata"]['fields'][0])['fullName'].to_list()
            
            nonpermissionable_fields[object] = task_result_dict[object]['fields'].T[task_result_dict[object]['fields'].T['permissionable'] == False].index.tolist()
        return permissionable_fields, nonpermissionable_fields, task_result_dict
    
    async def get_layout_metadata(self, layout_name):
        # Layout Name is the Object API Name + Page Layout Name of the layout, for example:
        # Account-Hospital Department
        
        async_metadata_read = async_wrap(self.metadata_read)
        
        layout_metadata = await async_metadata_read('Layout', layout_name)
        
        def parse_layoutSections(layout_metadata):
            layoutSections = pd.DataFrame(layout_metadata)
            layoutSections['layoutColumns'] = layoutSections['layoutColumns'].apply(lambda row: list(filter(lambda item: item is not None, row)))
            layoutSections = layoutSections.explode('layoutColumns').reset_index(drop=True)
            layoutSections['layoutColumns'] = layoutSections['layoutColumns'].apply(lambda row: "" if str(row) == 'nan' else row['layoutItems'])
            layoutSections = layoutSections.explode('layoutColumns').reset_index(drop=True)
            layoutSections = pd.concat([layoutSections, layoutSections['layoutColumns'].apply(pd.Series, dtype=str).add_prefix('layoutColumns.')], axis=1)
            if 'layoutColumns.0' in layoutSections.columns:
                # drop 'layoutColumns.0' column if it exists
                layoutSections.drop(['layoutColumns.0'], axis=1, inplace=True)
            
            if 'layoutColumns' in layoutSections.columns:
                layoutSections.drop(['layoutColumns'], axis=1, inplace=True)

            layoutSections.fillna("", inplace=True)
            layoutSections.drop_duplicates(inplace=True)
            return layoutSections

        def parse_platformActionList(platformActionList_metadata):
            platformActionList = pd.DataFrame(platformActionList_metadata)
            platformActionList = pd.concat([platformActionList, platformActionList['platformActionListItems'].apply(pd.Series, dtype=str).add_prefix('platformActionListItems.')], axis=1).drop(['platformActionListItems'], axis=1)
            return platformActionList


        def parse_quickActionList(quickActionList_metadata):
            quickActionList = pd.DataFrame(quickActionList_metadata)
            quickActionList = pd.concat([quickActionList, quickActionList['quickActionListItems'].apply(pd.Series, dtype=str).add_prefix('quickActionListItems.')], axis=1).drop(['quickActionListItems'], axis=1)
            return quickActionList

        parsed_layout_metadata = {}
        parsed_layout_metadata['customButtonsList'] = layout_metadata['customButtons'][0]
        parsed_layout_metadata['excludeButtonsList'] = layout_metadata['excludeButtons'][0]
        # Adding required fields from the main page layout gives you the final list of mini layout items
        parsed_layout_metadata['miniLayoutDict'] = dict(layout_metadata['miniLayout'][0]) if layout_metadata['miniLayout'][0] != None else {'fields': [],'relatedLists': []}
        parsed_layout_metadata['layoutSectionsDataFrame'] = parse_layoutSections(layout_metadata['layoutSections'][0]) if layout_metadata['layoutSections'][0] != None else pd.DataFrame()
        parsed_layout_metadata['platformActionListDataFrame'] = parse_platformActionList(layout_metadata['platformActionList'][0]) if layout_metadata['platformActionList'][0] != None else pd.DataFrame()
        parsed_layout_metadata['quickActionListDataFrame'] = parse_quickActionList(layout_metadata['quickActionList'][0]) if layout_metadata['quickActionList'][0] != None else pd.DataFrame()
        parsed_layout_metadata['relatedListDataFrame'] = pd.DataFrame(layout_metadata['relatedLists'][0]) if layout_metadata['relatedLists'][0] != None else pd.DataFrame()
        return parsed_layout_metadata

    async def get_all_reports_metadata(self, return_failed_reports=False):
        """
        Asynchronously fetches metadata for all reports from Salesforce.

        This function retrieves the metadata for all reports stored in Salesforce.
        It first gathers a list of all report folders and then fetches metadata for 
        each report in these folders. The function uses async operations to improve 
        performance by fetching metadata for multiple reports concurrently. The 
        results are then concatenated into a single DataFrame for easier processing.

        Returns:
            pandas.DataFrame: A DataFrame containing the metadata for all reports. 
                              The DataFrame is reset indexed for convenience.
        
        Raises:
            Exception: Any exception raised during metadata retrieval will result 
                       in an empty list for `report_folder_full_names`.
        """
        

        # Wrap the synchronous methods
        async_metadata_list = async_wrap(self.sf.mdapi.list_metadata)
        async_list_metadata_query = async_wrap(self.sf.mdapi.ListMetadataQuery)
        async_metadata_read = async_wrap(self.metadata_read)

        # Fetch report folder full names
        try:
            report_folder_full_names = [folder['fullName'] for folder in self.sf.mdapi.list_metadata(self.sf.mdapi.ListMetadataQuery(type='ReportFolder'))]
        
        # if zeep.exceptions.Fault is raised, return an empty list
        except zeep.exceptions.Fault as e:

            if e.code == 'sf:INVALID_SESSION_ID':
                if self.isSandbox and self.sfOrgId and self.sfPassword and self.sfUsername:
                    self.authenticate()
                    report_folder_full_names = [folder['fullName'] for folder in self.sf.mdapi.list_metadata(self.sf.mdapi.ListMetadataQuery(type='ReportFolder'))]
                else:
                    print("Invalid Session ID. Please reauthenticate with a valid session ID.")
                    report_folder_full_names = []
            else:
                print(f"Error fetching report folder names: {e}")
                report_folder_full_names = []
            
        except Exception as e:
            print(f"Error fetching report folder names: {e}")
            report_folder_full_names = []


        ############################################################################################################
        ## Retrieve Report Folders
        ############################################################################################################

        # List Metadata Queries
        task_list = []
        for report_folder in report_folder_full_names:
            task_list.append(async_list_metadata_query(type="Report", folder=report_folder))

        result_list = await asyncio.gather(*task_list, return_exceptions=True)

        folders_failed_to_retrieve = []
        # Filter out successful results and log exceptions
        successful_results = []
        for folder_name, result in zip(report_folder_full_names, result_list):
            if isinstance(result, Exception):
                folders_failed_to_retrieve.append((folder_name, result))
            else:
                successful_results.append(result)


        ############################################################################################################
        ## Retrieve Folder Content
        ############################################################################################################

        # Metadata List
        task_list = []
        for result in successful_results:
            task_list.append(async_metadata_list(result))

        report_metadata_list = await asyncio.gather(*task_list, return_exceptions=True)


        failed_folder_content_retrieval = []
        # Flatten the list and filter out exceptions
        flattened_report_metadata_list = []
        for report_metadata, sublist in zip(successful_results, report_metadata_list):
            if isinstance(sublist, Exception):
                failed_folder_content_retrieval.append((report_metadata['folder'], sublist))
            else:
                flattened_report_metadata_list.extend(sublist)


        ############################################################################################################
        ## Retrieve Report Metadata
        ############################################################################################################

        # Metadata Read
        task_list = []
        for report_details in flattened_report_metadata_list:
            task_list.append(async_metadata_read('Report', report_details['fullName']))

        report_metadata_result_list = await asyncio.gather(*task_list, return_exceptions=True)

        failed_report_metadata_retrieval = []
        # Filter out successful results and log exceptions
        successful_metadata_results = []
        for report_details, result in zip(flattened_report_metadata_list, report_metadata_result_list):
            if isinstance(result, Exception):
                failed_report_metadata_retrieval.append((report_details['fullName'], result))
            elif 'fullName' in result and result['fullName'][0] is None:
                failed_report_metadata_retrieval.append((report_details['fullName'], Exception("No report metadata found")))
            else:
                successful_metadata_results.append(result)

        # Concatenate successful results into a DataFrame
        if successful_metadata_results:
            all_report_metadata = pd.concat(successful_metadata_results).reset_index(drop=True)
        else:
            all_report_metadata = pd.DataFrame()
            

        ############################################################################################################
        ## Format failed results into a DataFrame
        ############################################################################################################

        failed_folders_df = pd.DataFrame(folders_failed_to_retrieve, columns=['Folder', 'Error'])
        failed_folders_df['Error Type'] = 'Folder'

        failed_folder_content_df = pd.DataFrame(failed_folder_content_retrieval, columns=['Folder', 'Error'])
        failed_folder_content_df['Error Type'] = 'Folder Content'

        failed_report_metadata_df = pd.DataFrame(failed_report_metadata_retrieval, columns=['Report', 'Error'])
        failed_report_metadata_df['Error Type'] = 'Report Metadata'

        failed_df = pd.concat([failed_folders_df, failed_folder_content_df, failed_report_metadata_df], ignore_index=True)

        # reorder the columns
        failed_df = failed_df[['Error Type', 'Folder', 'Report', 'Error']]    
        failed_df.fillna('', inplace=True)

        if return_failed_reports:
            return all_report_metadata, failed_df
        else:
            return all_report_metadata


    ### ----------------------------------------------------------------------------------------------------
    ### Synchronous Metadata Functions
    ### ----------------------------------------------------------------------------------------------------

    def object_describe(self, sobject_api_name: str, export_excel: bool=False):
        """

        """
        sfSchema = getattr(self.sf, sobject_api_name).describe()
        boolMetadata = {}
        nonetypeMetadata = {}
        strMetadata = {}
        orderedDictMetadata = pd.Series(dtype='object')
        childRelationshipsPD = pd.DataFrame()
        recordTypeInfosPD = pd.DataFrame()
        fieldsPD = pd.DataFrame()
        supportedScopesPD = pd.DataFrame()
        namedLayoutInfosPD = pd.DataFrame()
        actionOverridesPD = pd.DataFrame()

        for metadata in sfSchema:
            ## Processes all metadata that would return a boolean datatype
            if type(sfSchema[metadata]) is bool:
                boolMetadata[metadata] = sfSchema[metadata]

            ## Processes all metadata that would return a NoneType datatype
            elif type(sfSchema[metadata]) == type(None):
                nonetypeMetadata[metadata] = sfSchema[metadata]

            ## Processes all metadata that would return a string datatype
            elif type(sfSchema[metadata]) is str:
                strMetadata[metadata] = sfSchema[metadata]
            ## Processes all metadata that would return an OrderedDict data type
            elif type(sfSchema[metadata]) is OrderedDict and len(sfSchema[metadata]) != 0:
                orderedDictMetadata = pd.concat([orderedDictMetadata,pd.Series(sfSchema['urls'])])
            elif type(sfSchema[metadata]) is OrderedDict and len(sfSchema[metadata]) == 0:
                nonetypeMetadata[metadata] = "None"

            ## Processes all metadata that would return a list data type
            elif type(sfSchema[metadata]) is list and len(sfSchema[metadata]) != 0:
                if metadata == 'childRelationships':
                    childRelationshipsPD = pd.DataFrame(sfSchema['childRelationships'], index = pd.DataFrame(sfSchema['childRelationships'])['field'])
                    childRelationshipsPD = childRelationshipsPD.drop('field', axis=1).T
                if metadata == 'recordTypeInfos':
                    recordTypeInfosPD = pd.DataFrame(sfSchema['recordTypeInfos'], index = pd.DataFrame(sfSchema['recordTypeInfos'])['name'])
                    recordTypeInfosPD = recordTypeInfosPD.drop('name', axis = 1).T  
                if metadata == 'fields':
                    fieldsPD = pd.DataFrame(sfSchema['fields'], index = pd.DataFrame(sfSchema['fields'])['name'])
                    fieldsPD = fieldsPD.drop('name', axis = 1).T
                if metadata == 'supportedScopes':
                    supportedScopesPD = pd.DataFrame(sfSchema['supportedScopes'], index = pd.DataFrame(sfSchema['supportedScopes'])['name'])
                    supportedScopesPD = supportedScopesPD.drop('name', axis = 1).T
                if metadata == 'actionOverrides':
                    actionOverridesPD = pd.DataFrame(sfSchema['actionOverrides'], index = pd.DataFrame(sfSchema['actionOverrides'])['name'])
                    actionOverridesPD = actionOverridesPD.drop('name', axis = 1).T
                if metadata == 'namedLayoutInfos':
                    namedLayoutInfosPD = pd.DataFrame(sfSchema['namedLayoutInfos'], index = pd.DataFrame(sfSchema['namedLayoutInfos'])['name'])
                    namedLayoutInfosPD = namedLayoutInfosPD.drop('name', axis = 1).T
            ## Parses all empty list metadata
            elif type(sfSchema[metadata]) is list and len(sfSchema[metadata]) == 0:
                nonetypeMetadata[metadata] = "None"
            else:
                nonetypeMetadata[metadata] = "Unrecognized metadata type: " + metadata

        output = {'metadata': pd.concat([pd.Series(nonetypeMetadata),
                    pd.Series(boolMetadata),
                    pd.Series(strMetadata),
                    orderedDictMetadata]),
                    'childRelationships': childRelationshipsPD if len(childRelationshipsPD)!=0 else None,
                    'recordTypeInfos': recordTypeInfosPD if len(recordTypeInfosPD)!=0 else None,
                    'fields': fieldsPD if len(fieldsPD)!=0 else None,
                    'supportedScopes': supportedScopesPD if len(supportedScopesPD)!=0 else None, 
                    'namedLayoutInfos': namedLayoutInfosPD if len(namedLayoutInfosPD)!=0 else None,
                    'actionOverrides': actionOverridesPD if len(actionOverridesPD)!=0 else None}
        if export_excel:
            with pd.ExcelWriter(sobject_api_name + ' describe output.xlsx') as writer:  
                for key in output.keys():
                    try:
                        pd.DataFrame(output[key]).to_excel(writer, sheet_name=key)
                    except:
                        continue

        return output

    def field_describe(self, objects: List = ['Account','Address_vod__c','Child_Account_vod__c'], 
    attributes: List = ['name','type','length']) -> pd.DataFrame:
        """
        Returns a dataframe of the field metadata for the specified objects and attributes.

        Parameters
        ----------
        objects : List, optional
            A list of objects to get field metadata for. The default is ['Account','Address_vod__c','Child_Account_vod__c'].
        attributes : List, optional
            A list of attributes to get field metadata for. The default is ['name','type','length'].
            For a full list of attributes, see 
            https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_describesobjects_describesobjectresult.htm
            A list of attributes can also be found by using the object_describe() method's field attribute.

        Returns
        -------
        pd.DataFrame
            A dataframe of the field metadata for the specified objects and attributes.
        
        """
        outputList = []
        columnNames = []
        for sObjectAPIName in objects:
            for attribute in attributes:
                outputList.append([field[attribute] for field in getattr(self.sf, sObjectAPIName).describe()['fields']])
                if attribute == "name":
                    columnNames.append(sObjectAPIName)
                else:
                    columnNames.append(attribute.title())
        field_describe = pd.DataFrame(outputList).transpose()
        field_describe.columns = columnNames
        return field_describe

    def set_user_password(self, user_id, new_password):
        result = {}
        try:
            result = self.sf_api_call(f'/services/data/{self.api_version}/sobjects/User/{user_id}/password', method='POST', data={'NewPassword': new_password})
        except Exception as e:
            message_list = str(e).split(" : ")[1].strip().removeprefix("b'[").removesuffix("]'")
            result = ast.literal_eval(message_list)
            result['user_id'] = user_id
        
        if len(result) == 0:
            result = {'user_id': user_id,'message': 'success',  'errorCode': None}
        return result
        

    def picklist_dataframe_stacked(self,objects: List =['Account','Address_vod__c','Child_Account_vod__c']) -> pd.DataFrame:
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        output_df = pd.DataFrame()
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            processing_df = pd.DataFrame(pd.DataFrame([pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], 
                                                                   name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']).stack())
            processing_df.columns = ['Picklist API Value']
            processing_df['CRM Object and Field API'] = processing_df.index.get_level_values(0)
            processing_df[['CRM Object API','CRM Field API']] = processing_df['CRM Object and Field API'].str.split(".", expand = True)
            processing_df.reset_index(drop=True, inplace=True)
            output_df = pd.concat([output_df,processing_df])
        return output_df

    def picklist_dataframe(self,objects = ['Account','Address_vod__c','Child_Account_vod__c']) -> List:
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        referenceList = []
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            objectPicklistValues = pd.DataFrame(index=range(0,max(len(field["picklistValues"]) for field in objectDescribe['fields'] if field['type'] == 'picklist')))
            for x in [pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']:
                objectPicklistValues.insert(0, str(x.name), x)
            referenceList.append(objectPicklistValues)
        return referenceList

    def record_type_retrieval(self, objectAPIName, fieldAPINames = ["Id","Name",'SobjectType', 'IsActive']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        sfRTDF = pd.DataFrame(self.sf.query_all("SELECT "+ ",".join(fieldAPINames) + " from RecordType WHERE SobjectType = '" + objectAPIName + "'")['records'])
        
        # If only master RT exists
        if len(sfRTDF) == 0:
            master_rt = {
                "Name": "Master",
                "DeveloperName": "Master",
                "IsActive": True,
            }

            sfRTDF = pd.DataFrame(master_rt, index=[0])
        else:
            sfRTDF.drop(columns="attributes", inplace = True)
        return sfRTDF

    def object_permission_check(self, object, permission):
        data = transform_sf_result_set_rec(self.sf.query_all(f"""SELECT Assignee.Id, Assignee.Name,Assignee.IsActive, Assignee.UserName, PermissionSet.Id, PermissionSet.isOwnedByProfile, PermissionSet.Profile.Name, PermissionSet.Label
            FROM PermissionSetAssignment
            WHERE PermissionSetId
            IN (SELECT ParentId
            FROM ObjectPermissions
            WHERE SObjectType IN ('{object}') AND
            ({permission} = true)) AND Assignee.IsActive = TRUE""")['records'])
        
        profile_violations = data[data['PermissionSet.IsOwnedByProfile']== True][['User.Username', 'Profile.Name']]
        permission_set_violations = data[data['PermissionSet.IsOwnedByProfile']== False][['User.Username', 'PermissionSet.Label']]
        result = []
        for user in profile_violations['User.Username'].unique():
            result.append({"UserName": user, 
                            "Object API Name" : object,
                            "Permission": permission,
                            "Profile": "; ".join(list(profile_violations[profile_violations['User.Username'] == user]['Profile.Name'].unique())),
                            "Permission Set": ""
                        
                        }
                        
                        )
            
        for user in permission_set_violations['User.Username'].unique():
            result.append({"UserName": user, 
                                                            "Object API Name" : object,
                                                            "Permission": permission,
                                                            "Profile": "",
                                                            "Permission Set": "; ".join(list(permission_set_violations[permission_set_violations['User.Username'] == user]['PermissionSet.Label'].unique()))})
        return result

    def field_permission_check(self, object) -> dict[str, pd.DataFrame]:
        fls_results = transform_sf_result_set_rec(self.sf.query_all(f"""
                                            SELECT Field,
                                            ParentId,
                                            PermissionsEdit,
                                            PermissionsRead,
                                            SobjectType FROM FieldPermissions
                                            WHERE SobjectType in ('{object}')
                                            """)['records'])

        permissionSetProfiles = transform_sf_result_set_rec(self.sf.query_all("""
                                                    SELECT Id,Description,IsOwnedByProfile,Name,ProfileId, 
                                                    Profile.Name, Profile.Description,Type FROM PermissionSet
                                                    """)['records'])

        profiles = permissionSetProfiles[permissionSetProfiles['PermissionSet.IsOwnedByProfile'] == True][['PermissionSet.ProfileId','PermissionSet.Id','Profile.Name','Profile.Description']].copy()
        permissionSets = permissionSetProfiles[permissionSetProfiles['PermissionSet.IsOwnedByProfile'] == False][['PermissionSet.Id','PermissionSet.Name','PermissionSet.Description']].copy()

        permissionSetPermissions = pd.merge(fls_results, permissionSets, left_on='FieldPermissions.ParentId', right_on='PermissionSet.Id', how='inner').drop(columns=['PermissionSet.Id'], axis=1)
        permissionSetPermissions.columns = ['Field API Name', 'Permission Set Id', 'FLS Edit', 'FLS Read', 'Object API Name', 'Permission Set Name', 'Permission Set Description']
        permissionSetPermissions = permissionSetPermissions[['Permission Set Id', 'Permission Set Name', 'Permission Set Description', 'Object API Name', 'Field API Name', 'FLS Edit', 'FLS Read']]
        permissionSetPermissions['Field API Name'] = permissionSetPermissions['Field API Name'].apply(lambda x: x.split('.')[-1])


        profilePermissions = pd.merge(fls_results, profiles, left_on='FieldPermissions.ParentId', right_on='PermissionSet.Id', how='inner').drop(columns=['PermissionSet.Id','FieldPermissions.ParentId'], axis=1)
        profilePermissions.columns = ['Field API Name', 'FLS Edit', 'FLS Read', 'Object API Name','Profile Id',  'Profile Name', 'Profile Description']
        profilePermissions = profilePermissions[['Profile Id', 'Profile Name', 'Profile Description', 'Object API Name', 'Field API Name', 'FLS Edit', 'FLS Read']]
        profilePermissions['Field API Name'] = profilePermissions['Field API Name'].apply(lambda x: x.split('.')[-1])
        
        return {'permissionSetPermissions': permissionSetPermissions, 'profilePermissions': profilePermissions}


    # Retrieves the Page Layout by Profile by Record Type data for all objects in the org
    def retrieve_profile_layout_record_type_matrix_all(self, return_pivot_table = False):
        account_page_layouts_bulk = transform_sf_result_set_rec(self.tooling_query_all("""select LayoutId, 
                                                                                    ProfileId, Profile.Name, 
                                                                                    RecordTypeId, RecordType.Name, 
                                                                                    Layout.Name, TableEnumOrId from 
                                                                                    ProfileLayout"""))

        account_page_layouts_bulk['ProfileName'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Profile']['Name'] if row['ProfileLayout.Profile'] else "", axis=1)
        account_page_layouts_bulk['RecordTypeName'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.RecordType']['Name'] if row['ProfileLayout.RecordType'] else "", axis=1)
        account_page_layouts_bulk['PageLayout'] = account_page_layouts_bulk.apply(lambda row: row['ProfileLayout.Layout']['Name'] if row['ProfileLayout.Layout'] else "", axis=1)
        account_page_layouts_bulk.drop(['ProfileLayout.Profile','ProfileLayout.RecordType','ProfileLayout.Layout'], axis=1, inplace=True)


        object_dataframe = pd.DataFrame(self.tooling_query_all("Select DeveloperName from CustomObject"))
        object_dataframe['ObjectID'] = object_dataframe.apply(lambda row: row['attributes']['url'].split('/')[-1] if row['attributes']['url'] else "", axis=1)


        account_page_layouts_bulk = account_page_layouts_bulk.merge(object_dataframe, left_on='ProfileLayout.TableEnumOrId', right_on='ObjectID', how='left').copy()
        account_page_layouts_bulk['DeveloperName'] = account_page_layouts_bulk.apply(lambda row: row['DeveloperName'] if pd.notnull(row['DeveloperName']) else row['ProfileLayout.TableEnumOrId'], axis=1)
        account_page_layouts_bulk.drop(['ObjectID','attributes'], axis=1, inplace=True)
            
        # Fill in the RecordTypeName colum with the Master Record Type Name
        account_page_layouts_bulk['RecordTypeName'] = account_page_layouts_bulk['RecordTypeName'].apply(lambda row: row if row else 'Master')
        # Filter out Deprecated Profiles
        account_page_layouts_bulk = account_page_layouts_bulk[(~account_page_layouts_bulk['ProfileName'].isnull()) & (account_page_layouts_bulk['ProfileName'] != '') & (account_page_layouts_bulk['PageLayout'] != 'Veeva Vpro Unit Testing Layout')]
        
        if return_pivot_table:
            return account_page_layouts_bulk.pivot(index='ProfileName', columns=['DeveloperName','RecordTypeName'], values='PageLayout')
        else:
            return account_page_layouts_bulk
    
    #######################################################################################
    # Veeva CRM Server API Functions
    #######################################################################################

    def load_veeva_common(self):
        self.veeva_common = self.query("Select * From Veeva_Common_vod__c").to_dict()
    
    def load_org_info(self):
        self.org_info = self.query("Select * From Organization").to_dict()
        
    def get_network_admin_sf_user_info(self):
        
        if self.veeva_common is None:
            self.load_veeva_common()
        
        if self.org_info is None:
            self.load_org_info()
            
        try:
            response = requests.get(f"{self.veeva_common['Veeva_Server_vod__c'][0]}/{self.veeva_common['Veeva_Version_vod__c'][0]}?VER={self.veeva_common['Veeva_Version_vod__c'][0]}&SSID={self.session_id}&url=https://{self.instance}/services/Soap/u/24.0/{self.org_info['Id'][0]}&ses={self.session_id}&oType=networkAdmin&event=getSFCredentials")
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to get network admin credentials"}}
        
    def get_network_admin_network_user_info(self):
        
        if self.veeva_common is None:
            self.load_veeva_common()
        
        if self.org_info is None:
            self.load_org_info()
            
        try:
            response = requests.get(f"{self.veeva_common['Veeva_Server_vod__c'][0]}/{self.veeva_common['Veeva_Version_vod__c'][0]}?VER={self.veeva_common['Veeva_Version_vod__c'][0]}&SSID={self.session_id}&url=https://{self.instance}/services/Soap/u/24.0/{self.org_info['Id'][0]}&ses={self.session_id}&oType=networkAdmin&event=getNetworkCredentials")
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to get network admin credentials"}}

    def engage_admin_retrieve_groups(self):

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }
        
        if self.veeva_common is None:
            self.load_veeva_common()

        veeva_server = self.veeva_common['Veeva_Server_vod__c'][0]
        veeva_version = self.veeva_common['Veeva_Version_vod__c'][0]


        try:
            response = requests.get(f'{veeva_server}/{veeva_version}/api/v1/hcpproxy/groups', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage groups"}}
        
    def engage_admin_retrieve_users(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        veeva_server = self.veeva_common['Veeva_Server_vod__c'][0]
        veeva_version = self.veeva_common['Veeva_Version_vod__c'][0]


        try:
            response = requests.get(f'{veeva_server}/{veeva_version}/api/v1/hcpproxy/usersinfo', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage users."}}

    def engage_admin_get_license_info(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        veeva_server = self.veeva_common['Veeva_Server_vod__c'][0]
        veeva_version = self.veeva_common['Veeva_Version_vod__c'][0]


        try:
            response = requests.get(f'{veeva_server}/{veeva_version}/api/v1/remoteMeetings/orgs/{self.sfOrgId}', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage license info."}}
        
    def engage_meeting_process_admin_retrieve_history(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/epp-service/refresh/records', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage process admin history."}}
    
    def engage_meeting_process_admin_retrieve_veeva_crm_connection_management(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/credentials/SalesForce_EPP?systemId={self.sfOrgId}', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage process admin Veeva CRM connection management."}}
        
    def engage_meeting_process_admin_retrieve_veeva_vault_login_credential_management(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/credentials/Vault_EPP', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage process admin Veeva Vault login credential management."}}

    def engage_metadata_sync_admin_retrieve_vault_connection_management(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/credentials/Vault_Engage', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage metadata sync admin Veeva Vault connection management."}}

    def engage_metadata_sync_admin_retrieve_crm_connection_management(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/credentials/SalesForce_Engage?systemId=00D2g0000000ipMEAQ', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage metadata sync admin CRM connection management."}}

    def engage_metadata_sync_admin_retrieve_activity_debug_log(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/debug-log/collection?count=20&orgId=00D2g0000000ipMEAQ', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage metadata sync admin activity debug log."}}

    def engage_metadata_sync_admin_retrieve_metadata_sync(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/mcservice/status/refresh?count=10&recordType=Engage', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Engage metadata sync admin metadata sync."}}
        
    def veeva_process_admin_alerts_status_report(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/email-alert/recipients', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve Veeva process admin alerts status report."}}

    def process_scheduler_get_jobs(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sfendpoint": f"https://{self.instance.split('.')[0]}--c{'' if self.isSandbox == False else '.sandbox'}.vf.force.com/services/Soap/u/54.0/{self.sfOrgId}",
            "Sfsession": self.session_id,
        }

        if self.veeva_common is None:
            self.load_veeva_common()

        mc_server = self.veeva_common['Multichannel_Server_vod__c'][0]
        mc_context_root = self.veeva_common['Multichannel_Context_Root_vod__c'][0]


        try:
            response = requests.get(f'{mc_server}/{mc_context_root}/api/v1/scheduler/jobs', headers=headers)
            return {'status': response.status_code, 'response': response.json()}
        except:
            return {'status': 500, 'response': {"error": "Unable to retrieve process scheduler jobs."}}


    ##############################################################################################################
    # UI Functions
    # Functions that parses UI HTML responses
    ##############################################################################################################
    

    async def ui_retrieve_all_installed_packages_and_components(self):
        from bs4 import BeautifulSoup

        """
        Asynchronously retrieve all installed packages and their components in the current Salesforce instance.

        This method carries out the following operations:
        1. Queries the Salesforce Tooling API to obtain details of all installed subscriber packages.
        2. For each package, the components are retrieved by querying the Salesforce package page using HTTP requests.
        3. Organizes the extracted package data in a structured manner, flattening nested dictionaries and creating a Pandas DataFrame.
        4. Merges the package components data with the main package data, providing a comprehensive view.
        5. Extracts the Salesforce ID for each component from its corresponding link.
        6. Finally, the method returns a DataFrame containing the detailed info of all installed packages and their associated components.

        Returns:
            pd.DataFrame: DataFrame with columns representing package and component details such as package namespace, version, and component IDs.

        Dependencies:
            - Uses Beautiful Soup (bs4) for HTML parsing.
            - Uses Pandas for data structuring and manipulation.
            - Assumes Salesforce session and instance details are handled by the class.

        Internal Methods:
        - `subscriber_package_to_df(data)`: Converts subscriber package data into a DataFrame.
        - `get_package_components_by_id(package_id, sf_instance)`: Gets package components based on package ID.
        - `get_all_packages(subscriber_package_df: pd.DataFrame, sf_instance)`: Asynchronously retrieves all package components for given packages.

        Note: This method also handles specific structure of Salesforce pages and can be sensitive to changes on Salesforce's end.
        """
        def subscriber_package_to_df(data):
            # Flattening the nested dictionaries
            flattened_data = []
            for entry in data:
                flattened_entry = {
                    'Id': entry.get('Id', None),
                    'SubscriberPackageId': entry.get('SubscriberPackageId', None),
                    'SubscriberPackage.NamespacePrefix': entry['SubscriberPackage'].get('NamespacePrefix', None),
                    'SubscriberPackage.Name': entry['SubscriberPackage'].get('Name', None),
                    'SubscriberPackageVersion.Id': entry['SubscriberPackageVersion'].get('Id', None),
                    'SubscriberPackageVersion.Name': entry['SubscriberPackageVersion'].get('Name', None),
                    'SubscriberPackageVersion.MajorVersion': entry['SubscriberPackageVersion'].get('MajorVersion', None),
                    'SubscriberPackageVersion.MinorVersion': entry['SubscriberPackageVersion'].get('MinorVersion', None),
                    'SubscriberPackageVersion.PatchVersion': entry['SubscriberPackageVersion'].get('PatchVersion', None),
                    'SubscriberPackageVersion.BuildNumber': entry['SubscriberPackageVersion'].get('BuildNumber', None),
                }
                flattened_data.append(flattened_entry)

            # Convert to Pandas DataFrame
            df = pd.DataFrame(flattened_data)
            return df


        def get_package_components_by_id(package_id, sf_instance):
            url = f"https://{sf_instance.instance}/{package_id}"

            headers = {
                "Cookie": f"sid={sf_instance.session_id};"
            }

            payload = {
                "pkgComp": "show",
                "isdtp": "p1"
            }

            response = requests.get(url, headers=headers, params=payload)


            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            section_title = "Metadata Components Included in Package"
            metadata_section = soup.find('h3', text=section_title).find_parent('div', class_='bPageBlock')

            # Extract table headers
            headers = [header.text for header in metadata_section.select('tr.headerRow th')]

            # Appending "Link" to headers
            headers.append('Link')

            data = []

            # Extract table rows
            for row in metadata_section.select('tr.dataRow'):
                cells = row.select('td, th')
                row_data = [cell.text.strip() for cell in cells]
                
                # Check if the cell contains a link and extract it
                link = cells[1].find('a')
                row_data.append(link['href'] if link else None)
                
                data.append(row_data)

            df = pd.DataFrame(data, columns=headers)

            return df

        subscriber_packages = subscriber_package_to_df(self.tooling_query_all("""
                            SELECT Id, SubscriberPackageId, SubscriberPackage.NamespacePrefix,
                            SubscriberPackage.Name, SubscriberPackageVersion.Id,
                            SubscriberPackageVersion.Name, SubscriberPackageVersion.MajorVersion,
                            SubscriberPackageVersion.MinorVersion,
                            SubscriberPackageVersion.PatchVersion,
                            SubscriberPackageVersion.BuildNumber
                            FROM InstalledSubscriberPackage
                            ORDER BY SubscriberPackageId"""))


        async def get_all_packages(subscriber_package_df: pd.DataFrame, sf_instance):
            package_ids = subscriber_package_df['Id'].tolist()
            
            async_get_package_components_by_id = async_wrap(get_package_components_by_id)
            task_list = [async_get_package_components_by_id(package_id, sf_instance) for package_id in package_ids]
            
            result_list = await asyncio.gather(*task_list)
            
            result_df = None
            result_dict = {}
            for package_id, package_components in zip(package_ids, result_list):
                if result_df is None:
                    result_df = package_components
                    # Add Installed Package Id column
                    result_df['InstalledPackageId'] = package_id
                else:
                    # Add Installed Package Id column
                    package_components['InstalledPackageId'] = package_id
                    result_df = pd.concat([result_df, package_components])
            
            return result_df


        all_org_subscriber_packages = await get_all_packages(subscriber_packages, self)

        all_org_subscriber_packages_extended = all_org_subscriber_packages.merge(subscriber_packages[['Id','SubscriberPackage.NamespacePrefix','SubscriberPackage.Name','SubscriberPackageVersion.Name']], 
                                                left_on='InstalledPackageId', 
                                                right_on='Id', 
                                                how='left')

        # gets the 15 charactesr after %27%2F in the link column, this is basically the SFDC ID of the component
        pattern = r'%27%2F(\w{15})'

        all_org_subscriber_packages_extended['Component ID'] = all_org_subscriber_packages_extended['Link'].str.extract(pattern)

        # Drop ID and Link column
        all_org_subscriber_packages_extended.drop(columns=['Id','Link'], inplace=True)

        return all_org_subscriber_packages_extended



    ##############################################################################################################
    # WSDL Derived Functions
    ##############################################################################################################

    @serialze_zeep
    def metadata_read(self, metadata_type: str, fullName: str):
        return getattr(self.sf.mdapi, metadata_type).read(fullName)

    def metadata_delete(self, metadata_type: str, fullName: str):
        return getattr(self.sf.mdapi, metadata_type).delete(fullName)

    def metadata_update(self, metadata_type: str, parsed_metadata: dict):
        mdapi_object = getattr(self.sf.mdapi, metadata_type)()
        for key in parsed_metadata:
            setattr(mdapi_object, key, parsed_metadata[key])
        getattr(self.sf.mdapi, metadata_type).update(mdapi_object)
        return mdapi_object

    def metadata_create(self, metadata_type: str, parsed_metadata: dict):
        mdapi_object = getattr(self.sf.mdapi, metadata_type)()
        for key in parsed_metadata:
            setattr(mdapi_object, key, parsed_metadata[key])
        getattr(self.sf.mdapi, metadata_type).create(mdapi_object)
        return mdapi_object

    def metadata_list(self, metadata_type: str = '', metadata_type_list: list[str] = []) -> list:
        if len(metadata_type_list) == 0 and metadata_type != '':
            query = self.sf.mdapi.ListMetadataQuery(type=metadata_type)
        elif len(metadata_type_list) > 3:
            raise Exception("You can only query up to 3 metadata types at a time")
        
        elif len(metadata_type_list) > 0:
            query = []
            for metadata_type in metadata_type_list:
                query.append(self.sf.mdapi.ListMetadataQuery(type=metadata_type))
        else:
            raise Exception("Please populate either metadata_type or metadata_type_list, but not both.")
        
        query_response = self.sf.mdapi.list_metadata(query)
        return query_response
    
    def metadata_rename(self, metadata_type: str, previous_name: str, new_name: str): 
        """
        Renames the API name of SFDC metadata
        """
        getattr(self.sf.mdapi, metadata_type).rename(previous_name, new_name)
    
    ### ----------------------------------------------------------------------------------------------------
    ### Custom Tooling API Methods
    ### ----------------------------------------------------------------------------------------------------
    
    def tooling_query_all(self, query):
        done = False
        full_results = []
        result = self.sf_api_call(f'/services/data/v52.0/tooling/query', method='get', parameters={'q': query})
        while not done:
            full_results.extend(result['records'])
            done = result['done']
            if not done:
                result = self.sf_api_call(result['nextRecordsUrl'])
        return full_results

    ### ----------------------------------------------------------------------------------------------------
    ### Utility Functions
    ### ----------------------------------------------------------------------------------------------------
    def query_performance_feedback(self, query: str):
        # https://developer.salesforce.com/docs/atlas.en-us.240.0.api_rest.meta/api_rest/dome_query_explain.htm
        
        return self.sf_api_call(f'/services/data/{self.api_version}/query?explain={query}')
    
    def parse_sf_limits(self, sfdc_limits_result: dict, prefix=None) -> dict:
        ## Recursively parse the limits result to find the limits that are not 0
        result = {}
        for key, item in sfdc_limits_result.items():
            if set(['Max','Remaining']).issubset(set(item.keys())): 
                if item['Max'] == 0:
                    continue
                else:
                    result[key if prefix is None else prefix+' - '+key] = dict(zip(['Max','Remaining'],[item['Max'], item['Remaining']]))
            
            if len(set(item.keys()) - set(['Max','Remaining'])) > 0:
                sub_item = item.copy()
                if 'Max' in sub_item: 
                    del sub_item['Max']
                if 'Remaining' in sub_item: 
                    del sub_item['Remaining']
                result.update(self.parse_sf_limits(sub_item, prefix=key))
        return result
        
    def sf_api_call(self, action, parameters = {}, method = 'get', data = {}, timeout = 30):
        """
        Helper function to make calls to Salesforce REST API.
        Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
        """
        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.session_id
        }
        if method.lower() == 'get':
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, params=parameters, timeout=timeout)
        elif method.lower() in ['post', 'patch']:
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, json=data, params=parameters, timeout=timeout)
        elif method.lower() == 'delete':
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, params=parameters, timeout=timeout)
        else:
            # other methods not implemented in this example
            raise ValueError('Method should be get or post or patch.')
#         print('Debug: API %s call: %s' % (method, r.url) )
        if r.status_code < 300:
            if method=='patch':
                return None
            else:
                try:
                    return r.json()
                except:
                    return {}
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))


    def join(self, 
                dataframe, 
                rt_dataframe, 
                left_on="", 
                right_on="", 
                new_columns=[], 
                suffix = "_new"):
        """
        Joins and appends the Name and DeveloperName columns of record type to the dataframe.
        The dataframe must contain a column named "RecordTypeId" with the 18 digit SFID of the record type.
        """
        df_columns = dataframe.columns.to_list()
        if right_on not in new_columns:
            new_columns.insert(0,right_on)
        dataframe = pd.merge(dataframe, rt_dataframe[new_columns], how = 'inner', 
                                left_on = left_on,right_on = right_on, suffixes=('', suffix))
#         dataframe.drop([col for col in dataframe.columns if 'drop' in col], axis=1, inplace=True)
        return dataframe
