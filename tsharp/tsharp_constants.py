"""
This module contains constants used in the tsharp module.

- TARGET_ADO_URL: The URL of the Azure DevOps instance.
- TARGET_ADO_PROJECT: The name of the Azure DevOps project.
- VERBOSE: A flag indicating whether verbose logging is enabled.
"""

TARGET_ADO_URL = "https://dev.azure.com/deixeicom" ## /{self.url}/
TARGET_ADO_PROJECT = "deixei" ## /{self.project}/

DEBUG_RUN_ID = "1000229"

VERBOSE = True

# usage: AZURE_CREDENTIAL_ENV_MAPPING.get('tenant', 'AZURE_TENANT')
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

class EnviromentVariables:
    def env_config(self, name, default=None) -> str:
        return os.environ.get(name, default)

    @property
    def subscription_id(self) -> str:
        return self.env_config(AZURE_CREDENTIAL_ENV_MAPPING.get('subscription_id', 'SUBSCRIPTION_ID'), '')

    @property
    def client_id(self) -> str:
        return self.env_config(AZURE_CREDENTIAL_ENV_MAPPING.get('client_id', 'AZURE_CLIENT_ID'), '')
    
    @property
    def client_secret(self) -> str:
        return self.env_config(AZURE_CREDENTIAL_ENV_MAPPING.get('secret', 'AZURE_SECRET'), '')

    @property
    def tenant_id(self) -> str:
        return self.env_config(AZURE_CREDENTIAL_ENV_MAPPING.get('tenant', 'AZURE_TENANT'), '')


    @property
    def ado_url(self) -> str:
        return self.env_config(ADO_ENV_MAPPING.get('ado_url', 'DX_ADO_URL'), TARGET_ADO_URL)

    @property
    def ado_project(self) -> str:
        return self.env_config(ADO_ENV_MAPPING.get('ado_project', 'AZURE_DEVOPS_EXT_PROJECT'), TARGET_ADO_PROJECT)
    
    @property
    def ado_pat(self) -> str:
        return self.env_config(ADO_ENV_MAPPING.get('ado_pat', 'AZURE_DEVOPS_EXT_PAT'), '')

    @property
    def run_id(self) -> str:
        return self.env_config(ADO_ENV_MAPPING.get('run_id', 'RUN_ID'), DEBUG_RUN_ID)