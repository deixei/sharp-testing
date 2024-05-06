import os
import requests
from azure_sharp import AzureSharp
from ado_sharp import ADOLog, ADOTask
class PyTestSharp:
    """
    A class representing a PyTestSharp object.

    Args:
        ado_config (str): The ADO configuration.
        test_run_id (str): The test run ID.
        test_result_id (str): The test result ID.
        work_item_id (int): The work item ID.
        test_case_description (str): The test case description.
        ado_url (str, optional): The ADO URL. Defaults to None.
        ado_pat (str, optional): The ADO personal access token. Defaults to None.
        ado_project (str, optional): The ADO project. Defaults to None.
        verbose (str, optional): The verbosity level. Defaults to "v".
        azure_tenant (str, optional): The Azure tenant. Defaults to None.
        azure_client_id (str, optional): The Azure client ID. Defaults to None.
        azure_secret (str, optional): The Azure secret. Defaults to None.

    Methods:
        show_inputs: Prints the input values.
        add_evidence: Placeholder method for adding evidence.
    """

    def __init__(self, 
                 ado_config, test_run_id, test_result_id, 
                 work_item_id:int, test_case_description:str,
                 ado_url:str=None, ado_pat:str=None, ado_project:str=None, 
                 verbose:str="v",
                 azure_tenant:str=None, azure_client_id:str=None, azure_secret:str=None) -> None:
        
        self.ado_config = ado_config
        self.test_run_id = test_run_id
        self.test_result_id = test_result_id
        self.work_item_id = work_item_id
        self.test_case_description = test_case_description
        self.ado_url = ado_url
        self.ado_pat = ado_pat
        self.ado_project = ado_project
        self.verbose = verbose

        self.azure_tenant = azure_tenant
        self.azure_client_id = azure_client_id
        self.azure_secret = azure_secret

        self.azure_sharp = AzureSharp(azure_tenant, azure_client_id, azure_secret, verbose)

    def show_inputs(self):
        """
        Prints the input values of the PyTestSharp object.
        """
        print(f"\n")
        print(f"#"*80)
        print(f"# Sharp Testing Runner Helper")
        print(f"## Inputs")
        ADOLog.group("Inputs")
        print(f"#"*80)        
        print(f"- ado_config: {self.ado_config}")
        print(f"- test_run_id: {self.test_run_id}")
        print(f"- test_result_id: {self.test_result_id}")
        print(f"- work_item_id: {self.work_item_id}")
        print(f"- test_case_description: {self.test_case_description}")

        if self.verbose and "vv" in self.verbose:
            print(f"- ado_url: {self.ado_url}")
            print(f"- ado_project: {self.ado_project}")
            print(f"- azure_tenant: {self.azure_tenant}")
            print(f"- azure_client_id: {self.azure_client_id}")
        ADOLog.endgroup()
        print(f"#"*80)

    def add_evidence(self):
        """
        Placeholder method for adding evidence.
        """
        pass
    