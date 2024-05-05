import hmac
from datetime import datetime
from typing import List, Optional
from azure.identity import ClientSecretCredential
from collections import OrderedDict
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.managementgroups import ManagementGroupsAPI as ManagementGroupsClient
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import *
from collections import namedtuple

class AzureSharpBase:
    def __init__(self, azure_tenant:str=None, azure_client_id:str=None, azure_secret:str=None,
                 verbose:str="v") -> None:
        self.azure_tenant = azure_tenant
        self.azure_client_id = azure_client_id
        self.azure_secret = azure_secret
        self.verbose = verbose

        if not self.azure_tenant:
            raise ValueError("[Azure-Sharp ERROR]: Azure tenant not set.")
        if not self.azure_client_id:
            raise ValueError("[Azure-Sharp ERROR]: Azure client ID not set.")
        if not self.azure_secret:
            raise ValueError("[Azure-Sharp ERROR]: Azure secret not set.")

        # Creds
        self.azure_login, self.credential = self.get_azure_login_credential()

        # Clients
        self._resource_client = OrderedDict()
        self._management_group_client = None
        self._subscription_client = None

    def get_azure_login_credential(self, azure_login: dict = None):
        if azure_login != None:
            credential_data, credential = self.get_defaults_azure_login_credential(azure_login)
        else:
            credential_data, credential = self.get_defaults_azure_login_credential()

        return credential_data, credential

    def get_defaults_azure_login_credential(self, azure_login_credential=None):
        """
        Returns a dictionary containing default values for Azure credentials,
        optionally updated with the values from the provided AzureLoginCredential object.

        :param azure_login_credential: An AzureLoginCredential object containing values to update defaults (optional).
        :return: A dictionary containing default values for Azure credentials.
        """

        # Set default values for credential dictionary
        default_credential = {
            'token': "",
            'expires_on': 0,
            'credential': {
                'client_id': self.azure_client_id,
                'client_secret': self.azure_secret,
                'tenant_id': self.azure_tenant
            }
        }

        # Update defaults with values from AzureLoginCredential object (if provided)
        if azure_login_credential:
            # Update token and expires_on values (if provided)
            token = azure_login_credential.get('token')
            expires_on = azure_login_credential.get('expires_on')

            if token and expires_on:
                current_time = datetime.now().timestamp()
                if expires_on > current_time:
                    default_credential['token'] = token
                    default_credential['expires_on'] = expires_on

            # Update credential dictionary values (if provided)
            credential = azure_login_credential.get('credential', default_credential['credential'])
            if credential:
                default_credential['credential']['client_id'] = credential.get('client_id', default_credential['credential']['client_id'])
                default_credential['credential']['client_secret'] = credential.get('client_secret', default_credential['credential']['client_secret'])
                default_credential['credential']['tenant_id'] = credential.get('tenant_id', default_credential['credential']['tenant_id'])

        # Check if credential values are empty
        if not all(default_credential['credential'].values()):
            raise ValueError("[Ansible-Sharp ERROR]: Azure credentials not set.")

        credential = ClientSecretCredential(
            client_id=default_credential['credential']['client_id'],
            client_secret=default_credential['credential']['client_secret'],
            tenant_id=default_credential['credential']['tenant_id']
        )

        if not hmac.compare_digest(default_credential.get('token', ''), '') or default_credential.get('expires_on', 0) == 0:
            token = credential.get_token("https://management.azure.com/.default")
            default_credential['token'] = token.token
            default_credential['expires_on'] = token.expires_on

        return default_credential, credential

    def rm_client(self, subscription_id: str):
        if not self._resource_client.get(subscription_id):
            self._resource_client[subscription_id] = ResourceManagementClient(self.credential, subscription_id)
        return self._resource_client[subscription_id]

    @property
    def management_groups_client(self):
        if not self._management_group_client:
            self._management_group_client = ManagementGroupsClient(self.credential, base_url=self._cloud_environment.endpoints.resource_manager)
        return self._management_group_client

    @property
    def subscription_client(self):
        if not self._subscription_client:
            self._subscription_client = SubscriptionClient(self.credential, base_url=self._cloud_environment.endpoints.resource_manager)
        return self._subscription_client

    def run_query(self,
            query: str,
            subscriptions: Optional[List[str]] = None,
            management_groups: Optional[List[str]] = None):

        resourcegraph_client = ResourceGraphClient(
            credential=self.credential
        )
        # Basic query up to 2 pieces of object array
        query = QueryRequest(
                query=query,
                subscriptions=subscriptions,
                management_groups=management_groups,
                options=QueryRequestOptions(
                    result_format=ResultFormat.object_array
                )
            )
        query_response = resourcegraph_client.resources(query)

        return query_response

    def run_query_named(self,
            name: str,
            query: str,
            subscriptions: Optional[List[str]] = None,
            management_groups: Optional[List[str]] = None,):

        query_return_data = self.run_query(query, subscriptions, management_groups).data

        res = list()
        for item in query_return_data:
            Item = namedtuple(name, item.keys())
            data_object = Item(**item)
            res.append(data_object)

        return res