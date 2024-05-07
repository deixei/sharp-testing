"""
This module contains constants used in the tsharp module.

- TARGET_ADO_URL: The URL of the Azure DevOps instance.
- TARGET_ADO_PROJECT: The name of the Azure DevOps project.
- VERBOSE: A flag indicating whether verbose logging is enabled.
"""

TARGET_ADO_URL = "https://dev.azure.com/deixeicom" ## /{self.url}/
TARGET_ADO_PROJECT = "deixei" ## /{self.project}/
VERBOSE = True

AZURE_CREDENTIAL_ENV_MAPPING = dict(
    client_id='AZURE_CLIENT_ID',
    secret='AZURE_SECRET',
    tenant='AZURE_TENANT',
    subscription_id='SUBSCRIPTION_ID'
)

ADO_ENV_MAPPING = dict(
    ado_url='DX_ADO_URL',
    ado_project='AZURE_DEVOPS_EXT_PROJECT',
    ado_pat='AZURE_DEVOPS_EXT_PAT',
    run_id='RUN_ID'
)
