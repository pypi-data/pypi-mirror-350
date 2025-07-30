from sys import platform
import requests
import pandas as pd
import os
import json
from typing import List, Tuple, Optional, Union, Type, OrderedDict, Iterable
import numpy as np
import sys
import importlib.resources
from urllib.parse import urlparse
try:
    from custom_exceptions.veevanetwork_exceptions import *
except:
    from veevanetwork.custom_exceptions.veevanetwork_exceptions import *

class Vn:
    def __init__(self):
        self.os_platform: str = platform
        self.networkURL: str = None # https://verteonetwork.veevanetwork.com
        self.networkUserName: str = None
        self.networkPassword: str = None
        self.networkCountry: str = 'US'
        self.networkConnection: requests.models.Response = None
        self.networkLanguages: list = None # List of languages supported by this instance of Veeva Network
        self.networkObjects: dict = None # Dictionary of Network Objects and their properties
        self.networkObjectMetadata: dict = None # {'HCP': {'my_custom_field__c': {'fieldId': 'my_custom_field__c','type': {'dataType': 'STRING', 'discriminator': None}, 'labels': {'en': 'My Custom Field'}}}}
        self.networkReferenceTypes: dict = None # {'AddressAdminArea': {'type': 'AddressAdminArea','customerOwned': False,'inactive': False,'description': 'AddressAdminArea'}, 'AddressCBSA': {'type': 'AddressCBSA' ... }}
        self.networkReferenceValueMetadata: dict = None # Dictionary of Network Reference Value Metadata, including countries, reference codes, translated values, etc.
        self.sessionId: str = None
        self.networkId: str = None
        self.APIheaders: dict = None
        self.APIversionList: list = []
        self.LatestAPIversion: str = None
        self.network_references_all: pd.DataFrame = None
        self.network_DNS: str = None # verteonetwork.veevanetwork.com
        self.network_protocol: str = None # https

        #----------------------------------------------------------------
        # Load Network API Json
        self.network_api_json: dict = None
        try: # Try to load the network API json, to be used in a packaged distribution context
            with importlib.resources.open_text("veevanetwork", "network_api_v25.json") as file:
                self.network_api_json = json.load(file)
        except: # If the above fails, try to load the network API json, to be used in a development context
            with open('network_api_v25.json', encoding="utf-8") as file:
                self.network_api_json = json.load(file)
        self.network_api_parsed: dict = self.__parse_network_api_json(self.network_api_json)
        self.api_categories: list = list(self.network_api_parsed['item'].keys())

        self.api_change_request = self.network_api_parsed['item']['Change Request']
        self.api_custom_key = self.network_api_parsed['item']['Custom Key']
        self.api_entity = self.network_api_parsed['item']['Entity']
        self.api_hco = self.network_api_parsed['item']['HCO']
        self.api_hcp = self.network_api_parsed['item']['HCP']
        self.api_metadata = self.network_api_parsed['item']['Metadata']
        self.api_subscriptions = self.network_api_parsed['item']['Subscriptions']
        self.api_subscriptions_compliance = self.network_api_parsed['item']['Subscriptions - Compliance']
        self.api_subscriptions_source = self.network_api_parsed['item']['Subscriptions - Source']
        self.api_subscriptions_target = self.network_api_parsed['item']['Subscriptions - Target']
        self.api_events = self.network_api_parsed['item']['Events']
        self.api_match = self.network_api_parsed['item']['Match']
        self.api_suspect_match = self.network_api_parsed['item']['Suspect Match']
        self.api_authentication = self.network_api_parsed['item']['Authentication']
        self.api_retrieve_available_api_versions = self.network_api_parsed['item']['Retrieve Available API Versions']
        self.api_search = self.network_api_parsed['item']['Search']
        self.call = {
            "Change Request": {
                "change_request_create": self.change_request_create,
                "change_request_cancel": self.change_request_cancel,
                "change_request_retrieve": self.change_request_retrieve,
                "change_request_batch_retrieve": self.change_request_batch_retrieve,
                "change_request_update": self.change_request_update,
                "change_request_batch_update": self.change_request_batch_update,
                "change_request_process": self.change_request_process,
                "change_request_batch_process": self.change_request_batch_process,
                "change_request_search": self.change_request_search,
                "change_request_match": self.change_request_match,
                "change_request_batch_approve": self.change_request_batch_approve,
                "change_request_batch_reject": self.change_request_batch_reject
            },
            "Custom Key": {
                "custom_key_associate_to_entity": self.custom_key_associate_to_entity,
                "custom_key_associate_to_child": self.custom_key_associate_to_child,
                "custom_key_batch_associate_to_entities": self.custom_key_batch_associate_to_entities,
                "custom_key_batch_associate_to_children": self.custom_key_batch_associate_to_children,
                "custom_key_disassociate": self.custom_key_disassociate,
                "custom_key_batch_disassociate": self.custom_key_batch_disassociate
            },
            "Entity": {
                "entity_retrieve": self.entity_retrieve,
                "entity_retrieve_child": self.entity_retrieve_child,
                "entity_batch_retrieve": self.entity_batch_retrieve,
                "entity_batch_retrieve_children": self.entity_batch_retrieve_children
            },
            "HCO": {
                "hco_retrieve": self.hco_retrieve,
                "hco_associate_custom_key": self.hco_associate_custom_key,
                "hco_address_associate_custom_key": self.hco_address_associate_custom_key,
                "hco_license_associate_custom_key": self.hco_license_associate_custom_key,
                "hco_parenthco_associate_custom_key": self.hco_parenthco_associate_custom_key
            },
            "HCP": {
                "hcp_retrive": self.hcp_retrive,
                "hcp_associate_custom_key": self.hcp_associate_custom_key,
                "hcp_address_associate_custom_key": self.hcp_address_associate_custom_key,
                "hcp_license_associate_custom_key": self.hcp_license_associate_custom_key,
                "hcp_parenthco_associate_custom_key": self.hcp_parenthco_associate_custom_key
            },
            "Metadata": {
                "metadata_retrieve_available_api_versions": self.metadata_retrieve_available_api_versions,
                "metadata_retrieve_hashtags": self.metadata_retrieve_hashtags,
                "metadata_retrieve_object_types": self.metadata_retrieve_object_types,
                "metadata_retrieve_field": self.metadata_retrieve_field,
                "metadata_retrieve_field_details": self.metadata_retrieve_field_details,
                "metadata_retrieve_field_groups": self.metadata_retrieve_field_groups,
                "metadata_retrieve_reference_data_types": self.metadata_retrieve_reference_data_types,
                "metadata_retrieve_reference_data_type_details": self.metadata_retrieve_reference_data_type_details,
                "metadata_retrieve_reference_data_type_code_details": self.metadata_retrieve_reference_data_type_code_details
            },
            "Subscriptions": {
                "subscriptions_create_job": self.subscriptions_create_job,
                "subscriptions_retrieve_job": self.subscriptions_retrieve_job,
                "subscriptions_cancel_job": self.subscriptions_cancel_job,
                "subscriptions_retrieve_export_job_file": self.subscriptions_retrieve_export_job_file
            },
            "Subscriptions - Compliance": {
                "subscriptions_compliance_create_job": self.subscriptions_compliance_create_job,
                "subscriptions_compliance_retrieve_job": self.subscriptions_compliance_retrieve_job,
                "subscriptions_compliance_cancel_job": self.subscriptions_compliance_cancel_job
            },
            "Subscriptions - Source": {
                "subscriptions_source_create_job": self.subscriptions_source_create_job,
                "subscriptions_source_retrieve_job": self.subscriptions_source_retrieve_job,
                "subscriptions_source_cancel_job": self.subscriptions_source_cancel_job
            },
            "Subscriptions - Target": {
                "subscriptions_target_create_job": self.subscriptions_target_create_job,
                "subscriptions_target_retrieve_job": self.subscriptions_target_retrieve_job,
                "subscriptions_target_cancel_job": self.subscriptions_target_cancel_job
            },
            "Events": {
                "events_retrieve_merge": self.events_retrieve_merge,
                "events_retrieve_unmerge": self.events_retrieve_unmerge
            },
            "Match": {
                "match_retrieve": self.match_retrieve,
                "suspect_match_batch_reject_task": self.suspect_match_batch_reject_task,

            },
            "Suspect Match": {
                "suspect_match_batch_process": self.suspect_match_batch_process,
                "suspect_match_batch_create": self.suspect_match_batch_create,
                "suspect_match_batch_reject_task": self.suspect_match_batch_reject_task,
                "suspect_match_batch_retrieve": self.suspect_match_batch_retrieve
            },
            "Retrieve Available API Versions": {
                "retrieve_available_api_versions": self.retrieve_available_api_versions
            },
            "Search": {
                "search": self.search
            }
            }
    
    # =============================================================================
    # Authentication
    # =============================================================================

    # Refactored - MP 20220610
    def authenticate(
        self, 
        networkURL: str=None, 
        networkUserName: str=None, 
        networkPassword: str=None, 
        networkCountry: str=None, 
        networkId: str=None,
        sessionId: str=None,
        if_return: bool=False, 
        *args, **kwargs
    ) -> Optional[dict]:
        """
        Authenticates Veeva Network and retrieves the auth token.

        Example:
        authenticate using unpacked kwargs from the retrieve_credentials function
            authenticate_vn(**retrieve_credentials(platform, 'credentials.xlsx')[0])

        Return Example:
            {'sf': <simple_salesforce.api.Salesforce at 0x24a045c7b50>,
             'bulk': <salesforce_bulk.salesforce_bulk.SalesforceBulk at 0x24a045c7e20>,
             'sfMeta': <sfdclib.session.SfdcSession at 0x24a044b3400>,
             'tooling': <sfdclib.tooling.SfdcToolingApi at 0x24a045d17f0>,
             'session_id': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjDfxAAzYm.1uOKmNPXlKMW0sVz5ilIQ9ZwVTh6kOlaRuqfPuuzNnZNb3461sUGeUZ57ttE.GBawbt5h',
             'instance': 'cslbehring-core--devr01.my.salesforce.com',
             'sfMeta_is_connected': True,
             'bulk_api_sessionId': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjDfxAAzYm.1uOKmNPXlKMW0sVz5ilIQ9ZwVTh6kOlaRuqfPuuzNnZNb3461sUGeUZ57ttE.GBawbt5h'}

        Dependencies:
            import requests

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Authenticate
        
        """
        if (networkId and sessionId and networkURL):
            self.networkId = self.networkId if networkId is None else networkId
            self.sessionId = self.sessionId if sessionId is None else sessionId
        
        url_parse = urlparse(networkURL)
        if len(url_parse.scheme) == 0:
            self.network_protocol = 'https'
            if len(url_parse.path) > 0:
                self.network_DNS = url_parse.path
                self.networkURL = self.network_protocol + '://' + url_parse.path

        if len(url_parse.scheme) > 0:
            self.network_protocol = url_parse.scheme
            if len(url_parse.netloc) > 0:
                self.network_DNS = url_parse.netloc
                self.networkURL = url_parse.scheme + '://' + url_parse.netloc

        if (self.networkURL is None) or (len(self.networkURL) == 0):
            raise Exception('networkURL is required')


        # self.networkURL = self.networkURL if networkURL is None else networkURL
        self.networkUserName = self.networkUserName if networkUserName is None else networkUserName
        self.networkPassword = self.networkPassword if networkPassword is None else networkPassword
        self.networkCountry = self.networkCountry if networkCountry is None else networkCountry
        
        if self.networkUserName and self.networkPassword and self.networkURL:
            payload = {
                'username': self.networkUserName,
                'password': self.networkPassword
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            self.networkConnection = requests.post(self.networkURL + '/api/v29.0/auth', data=payload, headers=headers)
            
            if self.networkConnection.json()['responseStatus'] == 'SUCCESS':
                self.sessionId = self.networkConnection.json()['sessionId']
                self.userId = self.networkConnection.json()['userId']
                self.networkId = self.networkConnection.json()['networkId']
            else:
                raise Exception(self.networkConnection.json())


        
        self.APIheaders = {'authorization': self.sessionId}
        self.APIversionList = []
        
        # Error checking whether the required parameters are passed in
        # The check happens here because this is where all the self assignments has completed
        if (not (self.networkId and self.sessionId and self.networkURL)) and (not (self.networkUserName and self.networkPassword and self.networkCountry and self.networkURL)):
            raise Exception("Please provide either networkId, sessionId, and networkURL or networkUserName, networkPassword, and networkURL")
        
        for API in requests.get(self.networkURL +'/api', headers=self.APIheaders).json()['values'].keys():
            self.APIversionList.append(float(API.replace("v", "")))
        self.APIversionList.sort()
        self.LatestAPIversion = "v" + str(self.APIversionList[-1])
        

        if if_return:
            return {'networkURL':self.networkURL, 
                    'networkUserName':self.networkUserName, 
                    'networkPassword':self.networkPassword, 
                    'networkConnection':self.networkConnection, 
                    'sessionId':self.sessionId, 
                    'APIheaders':self.APIheaders, 
                    'APIversionList':self.APIversionList, 
                    'LatestAPIversion':self.LatestAPIversion}    

    # Refactored - MP 20220610
    def get_networkObjects(self) -> pd.DataFrame:
        """
        Returns a list of all objects in the Veeva Network.
        """
        self.authenticate()

        self.networkObjects = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/objectTypes',
                                      headers=self.APIheaders).json()['objectTypes'], 'name')
        return self.networkObjects

    # Refactored - MP 20220610
    def get_networkObjectMetadata(self) -> pd.DataFrame:
        self.authenticate()
        if self.networkObjects is None:
            self.get_networkObjects()

        processing_dict = {}
        __empty =[
            processing_dict.update({networkObject: 
                self.list_of_dicts_to_dict(requests.get(
                        self.networkURL + 
                        '/api/'+ self.LatestAPIversion +
                        '/metadata/fields?objectTypes=' + 
                        networkObject + '&details=full' + 
                        '&countries='+ self.networkCountry, 
                        headers=self.APIheaders).json()['attributes'],
                        'fieldId')}) 
                        for networkObject in self.networkObjects.keys()]
        self.networkObjectMetadata = processing_dict
        return self.networkObjectMetadata


    # Refactored - MP 20220612
    def process_networkReferenceCodeMetadata(
        self,
        referenceTypes: Optional[list] = None, # List of reference types to retrieve, leave empty (None) to retrieve all
        customerOwned: Optional[bool] = None, # True (customer owned only), False (ootb), None (customer owned and ootb)
        activeReferences: Optional[bool]= None, # True (active only), False (inactive only), None (active and inactive)
        languages: Optional[list]= None, # List of languages to retrieve, leave empty (None) to retrieve all
        countries: Optional[list]= None, # List of countries to retrieve, leave empty (None) to retrieve all
    ):
        """
        Processes Network Reference Metadata and returns a DataFrame of the reference codes based on the parameters.

        Parameters:
        referenceTypes: List of reference types to retrieve, leave empty (None) to retrieve all
        customerOwned (bool): Filter references by customerOwned status. Values: True (customerOwned only), False (ootb only), None (customerOwned and ootb)
        activeReferences (bool): Filter references by status. Values: True (active only), False (inactive only), None (active and inactive)
        languages (list): List of languages to return. Default: ['en']
        countries (list): List of countries to return. Default: ['US']

        Returns:
        DataFrame: A DataFrame of the reference codes based on the parameters.
        """

        if self.networkReferenceValueMetadata is None:
            self.get_networkReferenceValueMetadata()
        
        if languages is None:
            if self.networkLanguages is None:
                self.get_networkLanguages()
            languages = self.networkLanguages
            
        networkReferenceDF = pd.DataFrame(self.networkReferenceValueMetadata)
        networkReferenceCodeDataframe = networkReferenceDF.loc['reference_type_codes', :].dropna()
        reference_code_dict_unfiltered: dict[str, pd.DataFrame] = {}
        for index, values in zip(networkReferenceCodeDataframe.index, networkReferenceCodeDataframe.values):
            reference_code_dict_unfiltered.update({index: pd.DataFrame(self.list_of_dicts_to_dict(values, 'code'))})
        
        final_df = pd.DataFrame()
        for reference_type, reference_dataframe in zip(reference_code_dict_unfiltered.keys(), reference_code_dict_unfiltered.values()):
            if referenceTypes is None or reference_type in referenceTypes:
                activeReferences = None
                customerOwned = None
                activeReferences_filter = [True,False] if activeReferences is None else [not(activeReferences)]
                customerOwned_filter = [True,False] if customerOwned is None else [customerOwned]
                reference_dataframe = reference_dataframe.T.copy()
                filtered_customerOwned_and_active = reference_dataframe[
                                                (reference_dataframe['customerOwned'].isin(customerOwned_filter)) & 
                                                (reference_dataframe['inactive'].isin(activeReferences_filter))
                                                ]

                filtered_languages = pd.DataFrame()

                for language in languages:
                    filtered_languages = pd.concat([filtered_languages,
                                                pd.DataFrame(
                                                    filtered_customerOwned_and_active["values"]
                                                    .apply(lambda value: value[language] 
                                                    if value.keys()
                                                    .__contains__(language) 
                                                    else np.nan)
                                                    .dropna()
                                                    .rename(language))], axis=1)
                filtered_languages.insert(0, 'Network Code', filtered_languages.index)
                filtered_languages.insert(1, 'Reference Type', reference_type)
                filtered_languages.insert(2, 'Active Countries', pd.DataFrame(filtered_customerOwned_and_active["countries"]
                                                    .apply(lambda value: ";".join(sorted(value)) if (countries is None or len(set(value).intersection(set(countries)))>0 ) else np.nan).rename('countries')
                                                )['countries'])
                filtered_languages.insert(3, 'Definition', pd.DataFrame(
                                                    filtered_customerOwned_and_active["values"]
                                                    .apply(lambda value: value['en'] 
                                                    if value.keys()
                                                    .__contains__('en') 
                                                    else np.nan)
                                                    .dropna()
                                                    .rename('en'))['en'])
                filtered_languages.insert(4, 'Active?', filtered_customerOwned_and_active["inactive"] == False)
                filtered_languages.insert(5, 'Veeva Maintained?', filtered_customerOwned_and_active["customerOwned"] == False)             
                filtered_languages.reset_index(drop=True, inplace=True)
                filtered_languages.dropna(subset=['Active Countries'], inplace=True)
                filtered_languages.replace(np.nan, "", inplace=True)
                filtered_languages
                final_df = pd.concat([final_df, filtered_languages], axis=0)

        final_df.reset_index(drop=True, inplace=True)
        
        return final_df

    # To be deprecated, used by object_metadata_dataframe()
    def object_metadata(self):
        self.networkObjects = requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/objectTypes',
                                      headers=self.APIheaders).json()['objectTypes']
        networkObjectList = []
        for obj in self.networkObjects:
            if obj['status'] == 'ACTIVE':
                networkObjectList.append(obj['name'])
            else:
                pass
        object_metadata = pd.DataFrame([requests.get(self.networkURL + '/api/'+ self.LatestAPIversion +'/metadata/fields?objectTypes=' + networkObject + '&details=full' + '&countries='+ self.networkCountry, headers=self.APIheaders).json()['attributes'] 
                                              for networkObject in networkObjectList])
        object_metadata = object_metadata.transpose()
        object_metadata.columns = networkObjectList
        return object_metadata

    # To be deprecated, use get_networkObjectMetadata() instead
    def object_metadata_dataframe(self, object_metadata = None, attribute = None, *args):
        """
        Function that takes an input of data table with metadata values containing field for each row and objects for each column, 
        lists of input attributes available in the meta data (i.e. ['type','dataType']), 
        and optional arguments containing comma separated lists of additional attributes available in the meta data 
        
        Example:
            VeevaNetwork.object_metadata_dataframe(self.object_metadata(), ['fieldId'], ['type','dataType'], ['type','discriminator'], ['labels','en'],['maximumLength'])
            
        Return Example:
        (Dataframe)
            HCP.fieldId    HCP.type.dataType    HCP.type.discriminator    HCP.labels.en    HCP.maximumLength    HCO.fieldId      ...
            hcp_type__v    REFERENCE            HCPType                   HCP Type         100.0                340B_eligible__v ...
        
        """
        self.authenticate()
        
        object_metadata = self.object_metadata() if object_metadata is None else object_metadata
        
        object_metadata_dataframe = pd.DataFrame()
        attribute1 = attribute[0]
        attribute2 = attribute[1] if len(attribute) > 1 else ""
        for networkObjectName, networkObjectMetaData in object_metadata.iteritems():
            attributeList = []
            for fieldMetaData in networkObjectMetaData:
                try:
                    if attribute2 == "":
                        attributeList.append(fieldMetaData[attribute1])
                    else:
                        attributeList.append(fieldMetaData[attribute1][attribute2])
                except TypeError:
                    continue
    #        object_metadata_dataframe[networkObjectName + '.' + attribute1 + (("." + attribute2) if attribute2 != "" else "")] = pd.Series(attributeList, name = networkObjectName)
            object_metadata_dataframe = pd.concat([object_metadata_dataframe,pd.Series(attributeList, name = networkObjectName + '.' + attribute1 + (("." + attribute2) if attribute2 != "" else "")).to_frame()], ignore_index=False, axis=1)


            # parse arguments
            if args:
                for arg in args:
                    argAttribute1 = arg[0]
                    argAttribute2 = arg[1] if len(arg)>1 else ""
                    argAttributeList = []
                    for fieldMetaData in networkObjectMetaData:
                        try:
                            if argAttribute2 == "":
                                argAttributeList.append(fieldMetaData[argAttribute1])
                            else:
                                argAttributeList.append(fieldMetaData[argAttribute1][argAttribute2])
                        except:
                            argAttributeList.append("")
                            continue
    #                object_metadata_dataframe[networkObjectName + '.' + argAttribute1 + (("." + argAttribute2) if argAttribute2 != "" else "")] = pd.Series(argAttributeList, name = networkObjectName)
                    object_metadata_dataframe = pd.concat([object_metadata_dataframe,pd.Series(argAttributeList, name = networkObjectName + '.' + argAttribute1 + (("." + argAttribute2) if argAttribute2 != "" else "")).to_frame()], ignore_index=False, axis=1)
            else:
                continue
        return object_metadata_dataframe

    # Refactored - MP 20220611
    def get_networkReferenceValueMetadata(self):
        """
        Retruns a Dictionary of Network Reference Value Metadata, including countries, reference codes, translated values, etc.
        """
        self.authenticate()
        self.networkReferenceValueMetadata = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/reference_values?includeCodes=True', headers = self.APIheaders).json()['reference_type_values'],'type')
        return self.networkReferenceValueMetadata

    # Deprecated
    def reference_value_dataframe(self):
        """
        Retrieve all reference values in Network  
        ** formula can be enhanced or take input parameters so it doesn't query every single reference alias

        """
        self.authenticate()

        self.networkReferenceTypes = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/reference_values?includeCodes=True', headers = self.APIheaders).json()['reference_type_values'],'type')
        reference_value_dataframe = pd.DataFrame()
        for x in self.networkReferenceTypes.keys():
            try:
                referenceCall = requests.get(self.networkURL + '/api/'+ self.LatestAPIversion + '/metadata/reference_values/' + x + '?countries='+ self.networkCountry, headers = self.APIheaders).json()['reference_type_codes']
                newColumn = pd.Series([x['values']['en'] for x in referenceCall],name = str(x) + " Value")
                
                newColumn2 = pd.Series([x['code'] for x in referenceCall], name = x)
                reference_value_dataframe.insert(len(reference_value_dataframe.columns), column = x, value = newColumn2)
                reference_value_dataframe.insert(len(reference_value_dataframe.columns), column = str(x) + " Value", value = newColumn)
            except:
                pass
        return reference_value_dataframe

    def extract_network_reference_table(self):
        self.authenticate()
        
        references_all = pd.DataFrame(requests.get(self.networkURL + '/api/'+ self.LatestAPIversion + '/metadata/reference_values?includeCodes=true&countries='+ self.networkCountry, headers = self.APIheaders).json()['reference_type_values'])
        network_reference_table = pd.DataFrame()
        self.network_references_all = references_all
        for row in references_all['reference_type_codes']:
            if isinstance(row, list):
                network_reference_table = pd.concat([network_reference_table, pd.json_normalize(row)], axis=1)
            else:
                continue
        network_reference_table.fillna('',inplace=True)
        return network_reference_table
    
    # =============================================================================
    # WIP Functions
    # =============================================================================


    # =============================================================================
    # Change Request
    # =============================================================================

    def change_request_create(self, *args, **kwargs):
        """
        This API enables you to create a Network change request to add or update an HCP or HCO and related entities (including addresses, licenses, or parentHCOs) for **gray** data only.

        Change requests created using the API against orange data will be rejected.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Createachangerequest

        """
        
        return self.api_call(self.api_change_request['item']['Create Change Request'], *args, **kwargs)
        
    def change_request_cancel(self, *args, **kwargs):
        """
        This API enables you to cancel a change request by providing the change request ID.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Cancelchangerequest

        """
        return self.api_call(self.api_change_request['item']['Cancel Change Request'], *args, **kwargs)

    def change_request_retrieve(self, *args, **kwargs):
        """
        This API enables you to retrieve response information for the create, update, and merge change requests submitted by a client application.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveChangeRequest

        """
        return self.api_call(self.api_change_request['item']['Retrieve Change Request'], *args, **kwargs)
        
    def change_request_batch_retrieve(self, *args, **kwargs):
        """
        This API enables you to obtain information about multiple change requests through the API.

        Documenatation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchretrievechangerequest  

        """
        return self.api_call(self.api_change_request['item']['Change Request Batch Retrieve'], *args, **kwargs)
        
    def change_request_update(self, *args, **kwargs):
        """
        This API enables you to update an unprocessed change request through the API.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#UpdateChangeRequest

        """
        return self.api_call(self.api_change_request['item']['Change Request Update'], *args, **kwargs)

    def change_request_batch_update(self, *args, **kwargs):
        """
        This API enables you to update multiple unprocessed change requests.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchUpdateChangeRequests

        """
        return self.api_call(self.api_change_request['item']['Change Request Batch Update'], *args, **kwargs)

    def change_request_process(self, *args, **kwargs):
        """
        This API enables you to process an unprocessed change request through the API.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#ProcessChangeRequest

        """
        return self.api_call(self.api_change_request['item']['Change Request Process'], *args, **kwargs)

    def change_request_batch_process(self, *args, **kwargs):
        """
        This API enables you to process multiple unprocessed change requests.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchProcessChangeRequests
        """
        return self.api_call(self.api_change_request['item']['Change Request Batch Process'], *args, **kwargs)

    def change_request_search(self, *args, **kwargs):
        """
        This API enables you to retrieve all change requests that match a specified search criteria.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#ChangeRequestSearch

        """
        return self.api_call(self.api_change_request['item']['Change Request Search'], *args, **kwargs)

    def change_request_match(self, *args, **kwargs):
        """
        This API enables you to match a request to an existing entity. You can use either the Veeva ID or custom key of an existing entity to match the request against.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#ChangeRequestMatch

        """
        return self.api_call(self.api_change_request['item']['Change Request Match'], *args, **kwargs)

    def change_request_batch_approve(self, *args, **kwargs):
        """
        This API enables you to bulk approve up to 500 change requests.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchApproveChangeRequests

        """
        return self.api_call(self.api_change_request['item']['Change Request Batch Approve'], *args, **kwargs)

    def change_request_batch_reject(self, *args, **kwargs):
        """
        This API enables you to bulk reject up to 500 change requests.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchRejectChangeRequests

        """
        return self.api_call(self.api_change_request['item']['Change Request Batch Reject'], *args, **kwargs)
    
    # =============================================================================
    # Custom Key
    # =============================================================================

    def custom_key_associate_to_entity (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCPs or HCOs are downloaded from Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoentity

        """
        return self.api_call(self.api_custom_key['item']['Associate Custom Key to Entity'], *args, **kwargs)

    def custom_key_associate_to_child (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new children (address, license, or parent HCOs) are downloaded from Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytochildren

        """
        return self.api_call(self.api_custom_key['item']['Associate Custom Key to Children'], *args, **kwargs)

    def custom_key_batch_associate_to_entities (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers whenever new HCPs or HCOs are downloaded from Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchassociatecustomkeystoentities

        """
        return self.api_call(self.api_custom_key['item']['Batch Associate Custom Keys to Entities'], *args, **kwargs)

    def custom_key_batch_associate_to_children (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new children (address, license, or parent HCOs) are downloaded from Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchassociatecustomkeytochildren

        """
        return self.api_call(self.api_custom_key['item']['Batch Associate Custom Keys to Children'], *args, **kwargs)

    def custom_key_disassociate (self, *args, **kwargs):
        """
        This API enables you to deactivate external key identifiers for any entity (an HCP, HCO, Address, License, or ParentHCO) in Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Disassociatecustomkey

        """
        return self.api_call(self.api_custom_key['item']['Disassociate Custom Key'], *args, **kwargs)

    def custom_key_batch_disassociate (self, *args, **kwargs):
        """
        This API enables you to inactivate external key identifiers for any entity (HCP, HCO, Address, License, or ParentHCO) in Network without going through the full change request process.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchdisassociatecustomkey

        """
        return self.api_call(self.api_custom_key['item']['Batch Disassociate Custom Key'], *args, **kwargs)


    # =============================================================================
    # Entity
    # =============================================================================

    def entity_retrieve (self, *args, **kwargs):
        """
        This API enables you to obtain information on any entity without identifying the specific entity type. It is only used to retrieve information from Network using the GET method.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveentity

        """
        return self.api_call(self.api_entity['item']['Retrieve Entity'], *args, **kwargs)

    def entity_retrieve_child (self, *args, **kwargs):
        """
        This API enables you to retrieve child entity information; for example address or license details, for the Network ID provided without identifying the specific entity type.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievechildentity

        """
        return self.api_call(self.api_entity['item']['Retrieve Child Entity'], *args, **kwargs)

    def entity_batch_retrieve (self, *args, **kwargs):
        """
        This API enables you to retrieve entity details directly from Network. It is only used to retrieve information using the GET method. To update or delete entity data, you must use the change request APIs.

        The entities you can retrieve include HCPs and HCOs, and details are returned for all corresponding child entities: addresses, licenses, parent HCOs, and custom keys.
        
        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchretrieveentities

        """
        return self.api_call(self.api_entity['item']['Batch Retrieve Entities'], *args, **kwargs)

    def entity_batch_retrieve_children (self, *args, **kwargs):
        """
        This API enables you to obtain information on child entities without identifying the specific entity type. Users are only allowed to retrieve (GET) information from Network.

        All other operations (POST and DELETE) are restricted and can only be performed by submitting a change request using the change request APIs.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Batchretrievechildentities

        """
        return self.api_call(self.api_entity['item']['Batch Retrieve Child Entities'], *args, **kwargs)


    # =============================================================================
    # HCO
    # =============================================================================

    def hco_retrieve (self, *args, **kwargs):
        """
        This API enables you to retrieve information about an HCO. Information you can retrieve for an HCO includes the HCO, address, license, and parent HCO information (including their custom keys) for the HCO vid_key you provide.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveHCO

        """
        return self.api_call(self.api_hco['item']['Retrieve HCO'], *args, **kwargs)

    def hco_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCOs are downloaded from Network without going through the full change request process. This API associates the external identifier you submit to the HCO vid_key you provide.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#AssociatecustomkeytoHCO

        """
        return self.api_call(self.api_hco['item']['Associate Custom Key to HCO'], *args, **kwargs)

    def hco_address_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCO child objects (addresses) 
        are downloaded from Network without going through the full change request process. 
        This API associates the external identifier you submit to the child object key you provide.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject

        """
        return self.api_call(self.api_hco['item']['Associate Custom Key to HCO Address'], *args, **kwargs)

    def hco_license_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCO child objects (licenses) 
        are downloaded from Network without going through the full change request process. 
        This API associates the external identifier you submit to the child object key you provide.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject

        """
        return self.api_call(self.api_hco['item']['Associate Custom Key to HCO License'], *args, **kwargs)

    def hco_parenthco_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCO child objects (parent HCOs) 
        are downloaded from Network without going through the full change request process. 
        This API associates the external identifier you submit to the child object key you provide.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject

        """
        return self.api_call(self.api_hco['item']['Associate Custom Key to HCO ParentHCO'], *args, **kwargs)

    # =============================================================================
    # HCP
    # =============================================================================
    def hcp_retrive (self, *args, **kwargs):
        """
        This API enables you to retrieve information about an HCP including the HCP itself, address, license, and parent HCO information (including their custom keys) for the HCP vid_key you provide.

        This API downloads the record for the specified entity from Veeva OpenData to your customer instance.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveHCP

        """
        return self.api_call(self.api_hcp['item']['Retrieve HCP'], *args, **kwargs)

    def hcp_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCPs are downloaded from Network without going through the full change request process. This API associates the external identifier you submit to the HCP vid_key you provide.

        This API requires system administrator or API-only permissions.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#AssociatecustomkeytoHCP

        """
        return self.api_call(self.api_hcp['item']['Associate Custom Key to HCP'], *args, **kwargs)

    def hcp_address_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCP child objects (addresses) are downloaded from Network without going through the full change request process. This API associates the external identifier you submit to the child object key you provide.

        This API requires system administrator or API-only permissions.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject1

        """
        return self.api_call(self.api_hcp['item']['Associate Custom Key to HCP Address'], *args, **kwargs)

    def hcp_license_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCP child objects (licenses) are downloaded from Network without going through the full change request process. This API associates the external identifier you submit to the child object key you provide.

        This API requires system administrator or API-only permissions.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject1
        
        """
        return self.api_call(self.api_hcp['item']['Associate Custom Key to HCP License'], *args, **kwargs)

    def hcp_parenthco_associate_custom_key (self, *args, **kwargs):
        """
        This API enables you to submit external key identifiers when new HCP child objects (parent HCOs) are downloaded from Network without going through the full change request process. This API associates the external identifier you submit to the child object key you provide.

        This API requires system administrator or API-only permissions.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Associatecustomkeytoachildobject1
        
        """
        return self.api_call(self.api_hcp['item']['Associate Custom Key to HCP ParentHCO'], *args, **kwargs)

    # =============================================================================
    # Metadata
    # =============================================================================
    def metadata_retrieve_available_api_versions (self, *args, **kwargs):
        """
        This enables you to retrieve summary information about each API version available in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveavailableAPIversions
        
        """
        return self.api_call(self.api_metadata['item']['Retrieve Available API Versions'], *args, **kwargs)
        
    def metadata_retrieve_hashtags (self, *args, **kwargs):
        """
        This API enables you to retrieve the list of hashtags available in a Network instance.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievehashtags

        """
        return self.api_call(self.api_metadata['item']['Retrieve hashtags'], *args, **kwargs)

    # TODO: rename/refactor method.
    def get_networkLanguages(self) -> list:
        """
        This API enables you to retrieve the list of reference data languages available in a Network instance.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievelanguages

        """

        self.authenticate()
        self.networkLanguages = list(self.list_of_dicts_to_dict(
            requests.get(
                self.networkURL + 
                '/api/' + 
                self.LatestAPIversion + 
                '/metadata/languages', 
                headers=self.APIheaders).json()['languages'], 
                'name'
                ).keys())
        return self.networkLanguages

    def metadata_retrieve_object_types (self, *args, **kwargs):
        """
        This API enables you to retrieve the list of object types available in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveobjecttypesmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Object Types Metadata'], *args, **kwargs)

    def metadata_retrieve_field (self, *args, **kwargs):
        """
        This API enables you to retrieve detailed or summary information about the fields on each entity in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievefieldsmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Fields Metadata'], *args, **kwargs)

    def metadata_retrieve_field_details (self, *args, **kwargs):
        """
        This API enables you to retrieve detailed information about the fields on each entity in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievefielddetailsmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Field Details Metadata'], *args, **kwargs)

    def metadata_retrieve_field_groups (self, *args, **kwargs):
        """
        This API enables you to retrieve detailed information about the field groups available in Network. These field groups are used by the CRM bridge when retrieving and displaying information from Network in CRM.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievefieldgroupsmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Field Groups Metadata'], *args, **kwargs)

    def metadata_retrieve_reference_data_types (self, *args, **kwargs):
        """
        This API enables you to retrieve information about reference data types in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievereferencedatatypesmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Reference Data Types Metadata'], *args, **kwargs)

    def metadata_retrieve_reference_data_type_details (self, *args, **kwargs):
        """
        This API enables you to retrieve detailed information about reference data types in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievereferencedatatypedetailsmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Reference Data Type Details Metadata'], *args, **kwargs)

    def metadata_retrieve_reference_data_type_code_details (self, *args, **kwargs):
        """
        This API enables you to retrieve detailed information about reference data type codes in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievereferencedatatypecodedetailsmetadata

        """
        return self.api_call(self.api_metadata['item']['Retrieve Reference Data Type Code Details Metadata'], *args, **kwargs)

    # =============================================================================
    # Subscriptions
    # =============================================================================
    def subscriptions_create_job (self, *args, **kwargs):
        """
        This API enables you to create a subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Createasubscriptionjob

        """
        return self.api_call(self.api_subscriptions['item']['Create Subscription Job'], *args, **kwargs)

    def subscriptions_retrieve_job (self, *args, **kwargs):
        """
        This API enables you to retrieve the status of a source or target subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveasubscriptionjobstatus

        """
        return self.api_call(self.api_subscriptions['item']['Retrieve Subscription Job'], *args, **kwargs)

    def subscriptions_cancel_job (self, *args, **kwargs):
        """
        This API enables you to cancel a subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Cancelasubscriptionjob

        """
        return self.api_call(self.api_subscriptions['item']['Cancel Subscription Job'], *args, **kwargs)

    def subscriptions_retrieve_export_job_file (self, *args, **kwargs):
        """
        This API enables you to retrieve the artifacts (file contents) of a target subscription job.
        AKA: Retrieve target subscription artifact

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievetargetsubscriptionartifact
        
        """
        return self.api_call(self.api_subscriptions['item']['Retrieve Export Job File'], *args, **kwargs)

    # =============================================================================
    # Subscriptions - Compliance
    # =============================================================================
    def subscriptions_compliance_create_job (self, *args, **kwargs):
        """
        This API enables you to create a compliance subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Createacompliancesubscriptionjob

        """
        return self.api_call(self.api_subscriptions_compliance['item']['Create Compiance Subscription Job'], *args, **kwargs)

    def subscriptions_compliance_retrieve_job (self, *args, **kwargs):
        """
        This API enables you to retrieve the status of a source or target subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveacompliancesubscriptionjobstatus
        
        """
        return self.api_call(self.api_subscriptions_compliance['item']['Retrieve Compliance Subscription Job'], *args, **kwargs)

    def subscriptions_compliance_cancel_job (self, *args, **kwargs):
        """
        This API enables you to cancel a compliance subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Cancelacompliancesubscriptionjob

        """
        return self.api_call(self.api_subscriptions_compliance['item']['Cancel Compliance Subscription Job'], *args, **kwargs)

    # =============================================================================
    # Subscriptions - Source
    # =============================================================================
    def subscriptions_source_create_job (self, *args, **kwargs):
        """
        This API enables you to create a source subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Createasourcesubscriptionjob

        """
        return self.api_call(self.api_subscriptions_source['item']['Create Source Subscription Job'], *args, **kwargs)

    def subscriptions_source_retrieve_job (self, *args, **kwargs):
        """
        This API enables you to retrieve the status of a source subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveasourcesubscriptionjobstatus

        """
        return self.api_call(self.api_subscriptions_source['item']['Retrieve Source Subscription Job'], *args, **kwargs)

    def subscriptions_source_cancel_job (self, *args, **kwargs):
        """
        This API enables you to cancel a source subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Cancelasourcesubscriptionjob
        
        """
        return self.api_call(self.api_subscriptions_source['item']['Cancel Source Subscription Job'], *args, **kwargs)

    # =============================================================================
    # Subscriptions - Target
    # =============================================================================
    def subscriptions_target_create_job (self, *args, **kwargs):
        """
        This API enables you to create a target subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Createatargetsubscriptionjob

        """
        return self.api_call(self.api_subscriptions_target['item']['Create Target Subscription Job'], *args, **kwargs)

    def subscriptions_target_retrieve_job (self, *args, **kwargs):
        """
        This API enables you to retrieve the status of a source or target subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrieveatargetsubscriptionjobstatus

        """
        return self.api_call(self.api_subscriptions_target['item']['Retrieve Target Subscription Job'], *args, **kwargs)

    def subscriptions_target_cancel_job (self, *args, **kwargs):
        """
        This API enables you to cancel a target subscription job.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Cancelatargetsubscriptionjob
        """
        return self.api_call(self.api_subscriptions_target['item']['Cancel Target Subscription Job'], *args, **kwargs)

    # =============================================================================
    # Events
    # =============================================================================
    def events_retrieve_merge (self, *args, **kwargs):
        """
        This API enables you to retrieve the results of merge events that occurred in your Network instance.

        Merges initiated by Veeva OpenData on a master instance are included if the surviving and losing records of the merge have been downloaded to your instance.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveMerges

        """
        return self.api_call(self.api_events['item']['Retrieve Merge Events'], *args, **kwargs)

    def events_retrieve_unmerge (self, *args, **kwargs):
        """
        This API enables you to retrieve the results of unmerge events that occurred in your Network instance.

        Unmerges include events that occurred in your Network instance; only customer (gray) records are reported.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveUnmerges

        """
        return self.api_call(self.api_events['item']['Retrieve Unmerge Events'], *args, **kwargs)

    # =============================================================================
    # Match
    # =============================================================================
    def match_retrieve (self, *args, **kwargs):
        """
        This API enables you to match data immediately for a single record using match rules from the specified Network instance.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveMatches

        """
        return self.api_call(self.api_match['item']['Retrieve Matches'], *args, **kwargs)

    # =============================================================================
    # Suspect Match
    # =============================================================================
    def suspect_match_batch_process (self, *args, **kwargs):
        """
        This API enables enables you to process multiple unprocessed suspect matches.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchProcessSuspectMatch

        """
        return self.api_call(self.api_suspect_match['item']['Batch Process Suspect Match'], *args, **kwargs)

    def suspect_match_batch_create (self, *args, **kwargs):
        """
        This API enables enables you to create multiple suspect matches.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchCreateSuspectMatch

        """
        return self.api_call(self.api_suspect_match['item']['Batch Create Suspect Match'], *args, **kwargs)

    def suspect_match_batch_reject_task (self, *args, **kwargs):
        """
        This API enables enables you to reject multiple suspect match tasks.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchRejectSuspectMatch

        """
        return self.api_call(self.api_suspect_match['item']['Batch Reject Suspect Match Task'], *args, **kwargs)

    def suspect_match_batch_retrieve (self, *args, **kwargs):
        """
        This API enables enables you to retrieve information about multiple suspect matches.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#BatchRetrieveSuspectMatch

        """
        self.api_call(suspect_match['item']['Batch Retrieve Suspect Match'], *args, **kwargs)

    # =============================================================================
    # Retrieve Available API Versions
    # =============================================================================
    def retrieve_available_api_versions (self, *args, **kwargs):
        """
        This enables you to retrieve summary information about each API version available in Network.

        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#RetrieveavailableAPIversions

        """
        return self.api_call(self.api_retrieve_available_api_versions, *args, **kwargs)
    # =============================================================================
    # Search
    # =============================================================================
    def search (self, *args, **kwargs):
        """
        Search calls enable you to construct simple, yet powerful searches to retrieve data from Network.

        Calls through the Search API pass a query string in an expression that specifies the search text and specific parameters to get the intended set of entities from Network. Search results are ranked according to closeness to the search terms specified.
        
        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#search
        
        """
        return self.api_call(self.api_search, *args, **kwargs)
    # =============================================================================
    # System Settings
    # =============================================================================
    def system_settings_retrieve (self):
        """
        This API enables you to retrieve the value for the geolocation system setting.

        Currently only api.search.geolocation.countries is supported.
        
        Documentation:
        https://developer.veevanetwork.com/API_reference/API_reference.htm#Retrievesystemsettings
        
        """
        result = requests.get(
            url=f"{self.networkURL}/api/v26.0/systemSettings/api.search.geolocation.countries", 
            headers=self.APIheaders).json()
        return result
        

    # =============================================================================
    # Utilities
    # =============================================================================

    def api_call (
        self,
        api: dict, 
        body: dict = None, 
        variables: dict = None, 
        queries: dict = None, 
        if_print: bool=False,  # If True, prints each component of the api call, the api call will still execute unless if_debug or if_example paramters are set to True.
        if_debug: bool=False, # If True, the api call does not execute, but instead returns the api call as a string for debugging
        if_example: bool=False # If True, the api call does not execute and returns examples of any body, variables, or queries.
    ):

        examples = {}

        result = {
            'api_body' : body,
            'api_variables' : variables,
            'api_queries' : queries
        }

        request_params = {}

        def print_if(text):
            if if_print:
                print(text)

        if api.keys().__contains__('name'):
            print_if('\n- Name: ')
            print_if(api['name'])
            result['api_name'] = api['name'] ### Updating Result Name

        if api.keys().__contains__('protocolProfileBehavior'):
            print_if('\n- protocolProfileBehavior: ')
            if api['protocolProfileBehavior'].keys().__contains__('disableBodyPruning'):
                print_if('- disableBodyPruning: ')
                print_if(api['protocolProfileBehavior']['disableBodyPruning'])
                result['api_protocolProfileBehavior_disableBodyPruning'] = api['protocolProfileBehavior']['disableBodyPruning'] ### Updating Result disableBodyPruning

        if api.keys().__contains__('request'):

            ### =============================================================================
            ### Parsing Header
            ### =============================================================================

            if api['request'].keys().__contains__('header'):
                if isinstance(api['request']['header'], dict):
                    print_if("\n- Request header keys: ")
                    print_if(api['request']['header'].keys())
                    result['api_header'] = {}
                    request_params['headers'] = {}
                    for header_key, header_value in api['request']['header'].items():
                        print_if("\n- Request header key:")
                        print_if(header_key)
                        if isinstance(header_value, dict):
                            if header_value.keys().__contains__('value'):
                                result['api_header'].update({header_key: self.sub_request_params(api['request']['header'][header_key]['value'])}) ### Updating Result API Header
                                request_params['headers'].update({header_key: self.sub_request_params(api['request']['header'][header_key]['value'])}) ### Updating Request Header

                            for key, value in header_value.items():
                                print_if("\n- Request header value dict key and value:")
                                print_if(key)
                                print_if(value)
                        else:
                            print_if("Request Header Value: ")
                            print_if(header_value)
                            raise NetworkAPIHeaderValueNotFound

            ### =============================================================================
            ### Parsing Method
            ### =============================================================================

            if api['request'].keys().__contains__('method'):
                print_if("\n- Request method: ")
                print_if(api['request']['method'])

                match api['request']['method']:
                    case 'POST':
                        result['api_method'] = requests.post # Updating Result Method
                        print_if("\n- Request Method Post:")
                        print_if("requests.post")
                    case 'GET':
                        result['api_method'] = requests.get # Updating Result Method
                        print_if("\n- Request Method Get:")
                        print_if("requests.get")
                    case 'PUT':
                        result['api_method'] = requests.put # Updating Result Method
                        print_if("\n- Request Method Put:")
                        print_if("requests.put")
                    case 'DELETE':
                        result['api_method'] = requests.delete # Updating Result Method
                        print_if("\n- Request Method Delete:")
                        print_if("requests.delete")
                    case _:
                        print_if("\n- Request Method Unknown:")
                        print_if("unknown method")
                        raise NetworkAPIRequestMethodNotFound

            ### =============================================================================
            ### Parsing Body
            ### =============================================================================

            if (api['request'].keys().__contains__('body') == True) and \
                (api['request']['body'].keys().__contains__('raw') == True) and \
                (api['request']['body']['raw'] != ''):
                print_if("\n- Request body raw: ")
                print_if(json.loads(api['request']['body']['raw']))
                examples['body'] = json.loads(api['request']['body']['raw']) ### Updating Result API Body
                # If the body parameter is not provided in an API call that requires a body. Raise Error.
                if body is None and if_example==False:
                    raise NetworkAPIRequestBodyNotFound
                else:
                    request_params['data']=json.dumps(body)
            else:
                print_if("\n- Request body raw: ")
                print_if("No Body Found")
            
            ### =============================================================================
            ### Parsing URL
            ### =============================================================================

            if api['request'].keys().__contains__('url'):
                print_if("\n- Request url keys: ")
                print_if(api['request']['url'].keys())

                ### =============================================================================
                ### Parsing Raw URL
                ### =============================================================================

                if api['request']['url'].keys().__contains__('raw'):
                    print_if("\n- Request url raw: ")
                    print_if(api['request']['url']['raw'])
                    result['api_url'] = self.sub_request_params(api['request']['url']['protocol'] + "://" + api['request']['url']['host'][0] + "/" + "/".join(api['request']['url']['path'])) ### Updating Result API URL
                    request_params['url'] = self.sub_request_params(api['request']['url']['protocol'] + "://" + api['request']['url']['host'][0] + "/" + "/".join(api['request']['url']['path'])) ### Updating Request URL
                else:
                    raise NetworkAPIRequestURLNotFound

                
                ### =============================================================================
                ### Parsing URL Protocol
                ### =============================================================================
                
                if api['request']['url'].keys().__contains__('protocol'):
                    print_if("\n- Request url protocol: ")
                    # always "https"
                    print_if(api['request']['url']['protocol'])

                ### =============================================================================
                ### Parsing URL Host
                ### =============================================================================
                
                if api['request']['url'].keys().__contains__('host'):
                    print_if("\n- Request url host: ")
                    # always ['{{DNS}}]
                    print_if(api['request']['url']['host'][0])

                ### =============================================================================
                ### Parsing URL Path
                ### =============================================================================

                if api['request']['url'].keys().__contains__('path'):
                    print_if("\n- Request url path: ")
                    # A list of path components. i.e. ['api', '{{version}}', 'hcos', ':vid_key', 'addresses', ':address_key', 'custom_keys']
                    print_if(api['request']['url']['path'])

                ### =============================================================================
                ### Parsing URL Variable
                ### =============================================================================

                if api['request']['url'].keys().__contains__('variable'):
                    if variables is None and if_example==False:
                        raise NetworkAPIRequestVariableNotFound
                    elif if_example==False:
                        for variable in variables.keys():
                            result['api_url'] = result['api_url'].replace(":" + variable, variables[variable]['value'])
                            request_params['url'] = request_params['url'].replace(":" + variable, variables[variable]['value'])

                    if isinstance(api['request']['url']['variable'], dict):
                        print_if("\n- Request url variable keys: ")
                        print_if(api['request']['url']['variable'].keys())
                        variables: dict = api['request']['url']['variable']
                        examples['variables'] = variables ### Updating Result API URL Variable Examples
                        
                        for key, value in variables.items():
                            if isinstance(value, dict):
                                print_if("\n- Request url variable key and value dict: ")
                                print_if(key)
                                print_if(value)
                            else:
                                print_if("\n- Request url variable value: ") 
                                print_if(str(value))

                ### =============================================================================
                ### Parsing URL Query
                ### =============================================================================

                if api['request']['url'].keys().__contains__('query'):
                    if queries is None and if_example==False:
                        raise NetworkAPIRequestQueryNotFound
                    elif if_example==False:
                        result['api_url'] = result['api_url'] + '?'
                        request_params['url'] = request_params['url'] + '?'
                        for key, value in queries.items():
                            if result['api_url'][-1] == '?':
                                result['api_url'] = result['api_url'] + key + '=' + value['value']
                                request_params['url'] = request_params['url'] + key + '=' + value['value']
                            else:
                                result['api_url'] = result['api_url'] + '&' + key + '=' + value['value']
                                request_params['url'] = request_params['url'] + '&' + key + '=' + value['value']

                    print_if("\n- Request url query keys: ")
                    print_if(api['request']['url']['query'].keys())
                    queries: dict = api['request']['url']['query'] 
                    examples['query'] = queries ### Updating Result API URL Query Examples
                    for key, value in queries.items():
                        print_if("\n- Request url query key and value: ")
                        if isinstance(value, dict):
                            print_if(key)
                            print_if(value)
                        else:
                            print_if(str(value))

            ### =============================================================================
            ### Parsing Description
            ### =============================================================================

            if api['request'].keys().__contains__('description'):
                print_if("\n- Request Description: ")
                print_if(api['request']['description'])
                examples['description'] = api['request']['description'] ### Updating Description

        if api.keys().__contains__('response'):
            print_if(api['response'])

        if (not if_debug) & (not if_example) & (result.keys().__contains__('api_method')):
            response = result['api_method'](**request_params)

        if if_debug & if_example:
            return result, examples, request_params
        if if_debug:
            return result, request_params
        if if_example:
            return examples
        return response


    @staticmethod
    def list_of_dicts_to_dict(list_of_dict: list, key) -> dict:
        """
        Function takes a list of dicts and returns a single dict.

        Parameters:
        list_of_dict: list of dicts, i.e. [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value1', 'key2': 'value2'}]
        key (str): key to use for the dict. i.e. 'key1'
            in our example, [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value1', 'key2': 'value2'}]
            The output dictionary would have value1, value2 as the keys:
            {'value1': {'key1': 'value1', 'key2': 'value2'}, 'value2': {'key1': 'value1', 'key2': 'value2'}}

        """
        obj_dict = {}
        __empty = [obj_dict.update({x[key]: x}) for x in list_of_dict]
        return obj_dict

    @staticmethod
    def cartesian_join(pd1, pd2):
        df1 = pd1.copy()
        df2 = pd2.copy()
        df1.reset_index()
        df2.reset_index()
        df1['cartesian_join_key'] = 1
        df2['cartesian_join_key'] = 1
        result = pd.merge(df1, df2, on ='cartesian_join_key').drop(labels="cartesian_join_key", axis=1)
        return result
        
    def sub_request_params (self, request: str) -> str:
        substitutions_dict = {
            '{{AUTHORIZATION}}': self.APIheaders['authorization'],
            '{{DNS}}': self.network_DNS,
            '{{version}}': self.LatestAPIversion
        }
        for key, value in substitutions_dict.items():
            request = request.replace(key, value)
        return request
    
    def __parse_network_api_json(self, network_api: dict):
        output = {}
        for key, value in network_api.items():
            if isinstance(value, dict):
                output[key] = self.__parse_network_api_json(value)
            elif isinstance(value, list):
                first_key_set = set()
                for item in value:
                    if isinstance(item, dict):
                        first_key_set.add(list(item.keys())[0])
                if len(first_key_set) == 1:
                    output[key] = self.__parse_network_api_json(self.list_of_dicts_to_dict(value, list(first_key_set)[0]))
                else:
                    output[key] = value
            else:
                output[key] = value
        return output