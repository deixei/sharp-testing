import os
import yaml
import requests

class TSharpBase:
    """
    Represents the base class for TSharp.

    Args:
        ado_url (str, optional): The Azure DevOps URL. Defaults to None.
        ado_pat (str, optional): The Azure DevOps Personal Access Token. Defaults to None.
        ado_project (str, optional): The Azure DevOps project name. Defaults to None.
        verbose (str, optional): The verbosity level. Defaults to None.

    Raises:
        ValueError: If `ado_url`, `ado_pat`, or `ado_project` is not set.
        ValueError: If the `ado_url` has an invalid URL format for Azure DevOps.

    Attributes:
        ado_url (str): The Azure DevOps URL.
        ado_pat (str): The Azure DevOps Personal Access Token.
        ado_project (str): The Azure DevOps project name.
        verbose (str): The verbosity level.
        base_url (str): The base URL formed by combining `ado_url` and `ado_project`.

    Methods:
        requests_get: Sends a GET request to the specified partial URL and returns the response data.
        requests_post: Sends a POST request to the specified URL with the provided data.
        requests_put: Sends a PUT request to the specified URL with the provided data.
        requests_patch: Sends a PATCH request to the specified URL with the provided data.
    """

    class TSharpBase:
        def __init__(self, ado_url:str=None, ado_pat:str=None, ado_project:str=None, 
                     verbose:str=None):
            """
            Initializes a new instance of the TSharpBase class.

            Args:
                ado_url (str, optional): The URL of the Azure DevOps organization. Defaults to None.
                ado_pat (str, optional): The personal access token (PAT) for authenticating with Azure DevOps. Defaults to None.
                ado_project (str, optional): The name of the Azure DevOps project. Defaults to None.
                verbose (str, optional): The verbosity level for logging. Defaults to None.

            Raises:
                ValueError: If ado_url is not set.
                ValueError: If ado_pat is not set.
                ValueError: If ado_project is not set.
                ValueError: If the base URL has an invalid format.

            """
            self.ado_url = ado_url
            self.ado_pat = ado_pat
            self.ado_project = ado_project
            self.verbose = verbose
            
            if self.ado_url is None:
                raise ValueError("ADO_URL is not set")
            
            if self.ado_pat is None:
                raise ValueError("AZURE_DEVOPS_EXT_PAT is not set")
            
            if self.ado_project is None:
                raise ValueError("AZURE_DEVOPS_EXT_PROJECT is not set")
            
            self.base_url = f"{self.ado_url}/{self.ado_project}"

            # check if base url has a valid URL regex
            if not self.base_url.startswith("https://"):
                raise ValueError("Invalid URL format for Azure DevOps")

    def requests_get(self, partial_url):
        """
        Sends a GET request to the specified partial URL and returns the response data.

        Args:
            partial_url (str): The partial URL to append to the base URL.

        Returns:
            dict: The response data in JSON format.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the request.
        """
        url = f"{self.base_url}/{partial_url}"
        response = requests.get(url, auth=('PAT', self.ado_pat))
        data = response.json()

        if self.verbose and "vvv" in self.verbose: 
            print(f"#"*40)
            print(f"GET {url}")
            print(f"#"*40)
            print(data)
        
        return data
    
    def requests_post(self, partial_url, data):
        """
        Sends a POST request to the specified URL with the provided data.

        Args:
            partial_url (str): The partial URL to append to the base URL.
            data (dict): The data to be sent in the request body as JSON.

        Returns:
            dict: The response data as a dictionary.

        Raises:
            Exception: If the response data contains an item "$id" with value 1, an exception is raised with the response data message.
        """
        url = f"{self.base_url}/{partial_url}"
        response = requests.post(url, auth=('PAT', self.ado_pat), json=data)
        data = response.json()

        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data as an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])

        if self.verbose and "vvv" in self.verbose: 
            print(f"#"*40)
            print(f"POST {url}")
            print(f"#"*40)
            print(data)

        return data
    
    def requests_put(self, partial_url, data):
        """
        Sends a PUT request to the specified URL with the provided data.

        Args:
            partial_url (str): The partial URL to append to the base URL.
            data (dict): The data to be sent in the request body as JSON.

        Returns:
            dict: The response data as a dictionary.

        Raises:
            Exception: If the response data contains an item "$id" with value 1, an exception is raised with the response data message.
        """
        url = f"{self.base_url}/{partial_url}"
        response = requests.put(url, auth=('PAT', self.ado_pat), json=data)
        data = response.json()
        
        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data has an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])
        
        if self.verbose and "vvv" in self.verbose: 
            print(f"#"*40)
            print(f"PUT {url}")
            print(f"#"*40)
            print(data)

        return data
    
    def requests_patch(self, partial_url, data, include_content_type=False):
        """
        Sends a PATCH request to the specified URL with the provided data.

        Args:
            partial_url (str): The partial URL to append to the base URL.
            data (dict): The JSON data to be sent in the request body.
            include_content_type (bool, optional): Whether to include the 'Content-Type' header. 
                Defaults to False.

        Returns:
            dict: The JSON response data.

        Raises:
            Exception: If the response data contains an item "$id" with value 1, 
                an exception is raised with the response data message.
        """
        url = f"{self.base_url}/{partial_url}"
        
        headers = {
            "Content-Type": "application/json-patch+json"
        }

        if include_content_type:
            response = requests.patch(url, auth=('PAT', self.ado_pat), json=data, headers=headers)
        else:
            response = requests.patch(url, auth=('PAT', self.ado_pat), json=data)

        data = response.json()
        # in case the response data is empty, return an empty dict
        if not data:
            return {}
        
        # in case the response data as an item "$id" with value 1, throw an exception with the response data message
        if data.get("$id", "0") == "1":
            raise Exception(data["message"])

        if self.verbose and "vvv" in self.verbose: 
            print(f"#"*40)
            print(f"PATCH {url}")
            print(f"#"*40)
            print(data)

        return data

class TSharpConfig:
    """
    Represents the configuration for TSharp.

    Args:
        config_folder (str): The path to the configuration folder.
        dataset (str): The name of the dataset.

    Attributes:
        dataset_folder (str): The path to the dataset folder.
        filename_configs (str): The name of the configs file.
        filename_testcases (str): The name of the testcases file.
        filename_vars (str): The name of the vars file.
        path_configs (str): The path to the configs file.
        path_testcases (str): The path to the testcases file.
        path_vars (str): The path to the vars file.
        _configs (dict): The loaded configs.
        _testcases (dict): The loaded testcases.
        _vars (dict): The loaded vars.

    """

    def __init__(self, config_folder:str=None, dataset:str=None) -> None:
        self.dataset_folder = os.path.join(config_folder, dataset)

        self.filename_configs = "configs.yaml"
        self.filename_testcases = "testcases.yaml"
        self.filename_vars = "vars.yaml"
        
        self.ado_path_configs = os.path.join(self.dataset_folder, self.filename_configs)
        self.ado_path_testcases = os.path.join(self.dataset_folder, self.filename_testcases)
        self.ado_path_vars = os.path.join(self.dataset_folder, self.filename_vars)

        self._configs = {}
        self._testcases = {}
        self._vars = {}

        self.reload()

    def reload(self):
        """
        Reloads the configuration files.

        Raises:
            ValueError: If the dataset folder or any of the configuration files does not exist.

        """
        if not os.path.exists(self.dataset_folder):
            raise ValueError(f"Dataset folder {self.dataset_folder} does not exist")

        if not os.path.exists(self.ado_path_configs):
            raise ValueError(f"Configs file {self.ado_path_configs} does not exist")

        if not os.path.exists(self.ado_path_testcases):
            raise ValueError(f"Testcases file {self.ado_path_testcases} does not exist")

        if not os.path.exists(self.ado_path_vars):
            raise ValueError(f"Vars file {self.ado_path_vars} does not exist")

        if self.verbose and "vvv" in self.verbose:
            print(f"Reloading configurations from {self.dataset_folder}")
            print(f"Vars: {self.ado_path_vars}")
            print(f"Configs: {self.ado_path_configs}")
            print(f"Testcases: {self.ado_path_testcases}")

        self._configs = self.load(self.ado_path_configs)
        self._testcases = self.load(self.ado_path_testcases)
        self._vars = self.load(self.ado_path_vars)

    @property
    def configs(self):
        """
        Get or set the configs.

        Returns:
            dict: The configs.

        """
        return self._configs
    
    @configs.setter
    def configs(self, value):
        self._configs = value

    @property
    def testcases(self):
        """
        Get or set the testcases.

        Returns:
            dict: The testcases.

        """
        return self._testcases
    
    @testcases.setter
    def testcases(self, value):
        self._testcases = value

    @property
    def vars(self):
        """
        Get or set the vars.

        Returns:
            dict: The vars.

        """
        return self._vars
    
    @vars.setter
    def vars(self, value):
        self._vars = value

    def load(self, config_path):
        """
        Loads the data from a YAML file.

        Args:
            config_path (str): The path to the YAML file.

        Returns:
            dict: The loaded data.

        """
        data = {}

        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)

        return data
    
    def save(self, config_path, data):
        """
        Saves the data to a YAML file.

        Args:
            config_path (str): The path to the YAML file.
            data (dict): The data to be saved.

        """
        with open(config_path, 'w') as file:
            yaml.dump(data, file)

    def save_all(self):
        """
        Saves all the configuration files.

        """
        self.save(self.ado_path_configs, self._configs)
        self.save(self.ado_path_testcases, self._testcases)
        self.save(self.ado_path_vars, self._vars)