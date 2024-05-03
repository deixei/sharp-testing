import os
import yaml
import requests

TARGET_ADO_URL = "https://dev.azure.com/deixeicom" ## /{self.url}/
TARGET_ADO_PROJECT = "deixei" ## /{self.project}/

class TSharpBase:
    def __init__(self):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.project = os.environ.get("AZURE_DEVOPS_EXT_PROJECT", TARGET_ADO_PROJECT)
        
        if self.url is None:
            raise ValueError("DX_ADO_URL is not set")
        
        if self.pat is None:
            raise ValueError("AZURE_DEVOPS_EXT_PAT is not set")
        
        if self.project is None:
            raise ValueError("AZURE_DEVOPS_EXT_PROJECT is not set")
        
        self.base_url = f"{self.url}/{self.project}"

        # check if base url has a valid URL regex
        if not self.base_url.startswith("https://"):
            raise ValueError("Invalid URL format for Azure DevOps")

    def requests_get(self, partial_url):
        url = f"{self.base_url}/{partial_url}"
        response = requests.get(url, auth=('PAT', self.pat))
        data = response.json()

        return data
    
    def requests_post(self, partial_url, data):
        url = f"{self.base_url}/{partial_url}"
        response = requests.post(url, auth=('PAT', self.pat), json=data)
        data = response.json()

        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data as an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])

        return data
    
    def requests_put(self, partial_url, data):
        url = f"{self.base_url}/{partial_url}"
        response = requests.put(url, auth=('PAT', self.pat), json=data)
        data = response.json()
        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data as an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])
        
        return data
    
    def requests_patch(self, partial_url, data, include_content_type=False):
        url = f"{self.base_url}/{partial_url}"
        
        headers = {
            "Content-Type": "application/json-patch+json"
        }

        if include_content_type:
            response = requests.patch(url, auth=('PAT', self.pat), json=data, headers=headers)
        else:
            response = requests.patch(url, auth=('PAT', self.pat), json=data)

        data = response.json()
        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data as an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])
        
        return data

class TSharpConfig:
    def __init__(self, path, filename, load_on_init=True) -> None:
        # Get the current script directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        if path is None or path == '':
            self.path = script_dir

        if filename is None or filename == '':
            self.filename = 'config.yaml'

        self.path = path
        self.filename = filename

        self.config_path = os.path.join(self.path, self.filename)

        self._config = {}

        if load_on_init:
            self.load()

    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        self._config = value

    def load(self):
        self._config = {}

        with open(self.config_path, 'r') as file:
            self._config = yaml.safe_load(file)

        return self._config
    
    def save(self):
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file)