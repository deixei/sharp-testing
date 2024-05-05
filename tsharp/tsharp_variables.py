# This file contains the TestVariables class, which is responsible for managing test variables in TSharp.
from tsharp_base import TSharpBase

class TestVariables(TSharpBase):
    """
    Represents a class for managing test variables in TSharp.
    """

    def __init__(self, ado_url:str=None, ado_pat:str=None, ado_project:str=None, verbose:str=None):
        super().__init__(ado_url, ado_pat, ado_project, verbose)

    def get_test_variables(self):
        """
        Retrieves all test variables.

        Returns:
            dict: The response data containing the test variables.
        """
        url = f"/_apis/test/variables?api-version=5.0-preview.1"
        response_data = self.requests_get(url)
        return response_data

    def create_test_variable(self, variable):
        """
        Creates a new test variable.

        Args:
            variable (dict): The test variable to create.

        Returns:
            dict: The response data containing the created test variable.
        """
        url = f"/_apis/test/variables?api-version=5.0-preview.1"
        response_data = self.requests_post(url, variable)

        return response_data

    def get_test_variable(self, id):
        """
        Retrieves a specific test variable by its ID.

        Args:
            id (str): The ID of the test variable.

        Returns:
            dict: The response data containing the test variable.
        """
        url = f"/_apis/test/variables/{id}?api-version=5.0-preview.1"
        response_data = self.requests_get(url)
        return response_data
    
    def update_test_variable(self, id, variable):
        """
        Updates a specific test variable.

        Args:
            id (str): The ID of the test variable.
            variable (dict): The updated test variable.

        Returns:
            dict: The response data containing the updated test variable.
        """
        url = f"/_apis/test/variables/{id}?api-version=5.0-preview.1"
        response_data = self.requests_patch(url, variable)
        return response_data

    def create_test_variable_if_not_exists(self, variable):
        """
        Creates a new test variable if it does not already exist,
        otherwise updates the existing test variable.

        Args:
            variable (dict): The test variable to create or update.

        Returns:
            dict: The response data containing the created or updated test variable.
        """
        test_variables = self.get_test_variables()
        for test_variable in test_variables["value"]:
            if test_variable["name"] == variable["name"]:
                return self.update_test_variable(test_variable["id"], variable)
        return self.create_test_variable(variable)
