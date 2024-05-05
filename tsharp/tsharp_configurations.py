# This file contains the TestConfigurations class which provides methods to interact with test configurations in TSharp.
from tsharp_base import TSharpBase

class TestConfigurations(TSharpBase):
    """
    Class representing test configurations in TSharp.

    This class provides methods to interact with test configurations in TSharp.
    """

    def __init__(self, ado_url:str=None, ado_pat:str=None, ado_project:str=None, verbose:str=None):
        super().__init__(ado_url, ado_pat, ado_project, verbose)

    def get_test_configurations(self):
        """
        Get all test configurations.

        Returns:
            dict: The response data containing the test configurations.
        """
        url = f"/_apis/test/configurations?api-version=5.0"
        response_data = self.requests_get(url)
        return response_data
        
    def create_test_configuration(self, configuration):
        """
        Create a new test configuration.

        Args:
            configuration (dict): The configuration data for the test configuration.

        Returns:
            dict: The response data containing the created test configuration.
        """
        url = f"/_apis/test/configurations?api-version=5.0"
        response_data = self.requests_post(url, configuration)
        return response_data
    
    def get_test_configuration(self, id):
        """
        Get a specific test configuration by ID.

        Args:
            id (int): The ID of the test configuration.

        Returns:
            dict: The response data containing the test configuration.
        """
        url = f"/_apis/test/configurations/{id}?api-version=5.0"
        response_data = self.requests_get(url)
        return response_data
    
    def update_test_configuration(self, id, configuration):
        """
        Update a specific test configuration.

        Args:
            id (int): The ID of the test configuration.
            configuration (dict): The updated configuration data for the test configuration.

        Returns:
            dict: The response data containing the updated test configuration.
        """
        url = f"/_apis/test/configurations/{id}?api-version=5.0"
        response_data = self.requests_patch(url, configuration)
        return response_data
    
    def create_test_configuration_if_not_exists(self, configuration):
        """
        Create a new test configuration if it does not already exist, otherwise update the existing one.

        Args:
            configuration (dict): The configuration data for the test configuration.

        Returns:
            dict: The response data containing the created or updated test configuration.
        """
        test_configurations = self.get_test_configurations()
        for test_configuration in test_configurations["value"]:
            if test_configuration["name"] == configuration["name"]:
                return self.update_test_configuration(test_configuration["id"], configuration)
        return self.create_test_configuration(configuration)
