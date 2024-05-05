from azure_sharp_base import AzureSharpBase

class AzureSharp(AzureSharpBase):
    def __init__(self, azure_tenant:str=None, azure_client_id:str=None, azure_secret:str=None,
                 verbose:str="v") -> None:
        super().__init__(azure_tenant, azure_client_id, azure_secret, verbose)
        
        self._subscriptions = list()
        self._management_groups = list()

    @property
    def subscriptions(self):
        if not self._subscriptions or len(self._subscriptions) == 0:
            self.query_subscriptions()
        return self._subscriptions
    
    @property
    def management_groups(self):
        if not self._management_groups or len(self._management_groups) == 0:
            self.query_management_groups()
        return self._management_groups
    
    def query_management_groups(self):
        query = '''resourcecontainers
                | where type == "microsoft.management/managementgroups"
            '''
        return self.run_query_named("ManagementGroup", query)


    def query_subscriptions(self):
        query = '''resourcecontainers
                | where type == "microsoft.resources/subscriptions"
                | project name, id, subscriptionId, properties, ['tags']
                | sort by name asc
            '''
        return self.run_query_named("Subscription", query)


    def query_subscriptions_by_management_group(self, management_group_name: str):
        query = f'''resourcecontainers
                | where type == 'microsoft.resources/subscriptions'
                | mv-expand managementGroupParent = properties.managementGroupAncestorsChain
                | where managementGroupParent.name =~ '{management_group_name}'
                | project name, id, subscriptionId, properties, ['tags']
                | sort by name asc
            '''
        return self.run_query_named("Subscription", query)


    def subscription(self, subscription_id: str):
        return [subscription for subscription in self.subscriptions if subscription.subscription_id == subscription_id][0]
    
    @property
    def subscription_ids(self):
        return self.subscriptions.keys()    