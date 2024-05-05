from tsharp_base import TSharpBase

class TestSuites(TSharpBase):
    """
    A class representing test suites in TSharp.

    Args:
        test_plan_id (int): The ID of the test plan.
        parent_suite_id (int): The ID of the parent suite.
        ado_url (str, optional): The URL of the Azure DevOps organization. Defaults to None.
        ado_pat (str, optional): The personal access token for the Azure DevOps organization. Defaults to None.
        ado_project (str, optional): The name of the Azure DevOps project. Defaults to None.
        verbose (str, optional): The verbosity level of the output. Defaults to v.

    Attributes:
        test_plan_id (int): The ID of the test plan.
        parent_suite_id (int): The ID of the parent suite.
    """

    def __init__(self, test_plan_id, parent_suite_id, ado_url:str=None, ado_pat:str=None, ado_project:str=None, verbose:str="v"):
        super().__init__(ado_url, ado_pat, ado_project, verbose)
        self.test_plan_id = test_plan_id
        self.parent_suite_id = parent_suite_id

    def get_test_suites(self):
        """
        Get all test suites for the specified test plan.

        Returns:
            dict: The response data containing the test suites.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites?api-version=5.0"
        response_data = self.requests_get(url)
        
        return response_data
    
    def create_test_suite(self, name, description):
        """
        Create a new test suite.

        Args:
            name (str): The name of the test suite.
            description (str): The description of the test suite.

        Returns:
            dict: The created test suite item.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites/{self.parent_suite_id}/?api-version=5.0"
        response_data = self.requests_post(url, data={
            "name": name,
            "suiteType": "StaticTestSuite"
        })

        item = response_data["value"][0]
        
        return item
    
    def get_test_suite(self, id):
        """
        Get a specific test suite by ID.

        Args:
            id (int): The ID of the test suite.

        Returns:
            dict: The response data containing the test suite.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites/{id}?api-version=5.0"
        response_data = self.requests_get(url)
        
        return response_data
    
    def update_test_suite(self, id, name, description):
        """
        Update a test suite.

        Args:
            id (int): The ID of the test suite.
            name (str): The new name of the test suite.
            description (str): The new description of the test suite.

        Returns:
            dict: The response data containing the updated test suite.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites/{id}?api-version=5.0"
        response_data = self.requests_patch(url, data={
            "description": description,
            "suiteType": "StaticTestSuite"
        })
        
        return response_data
    
    def create_test_suite_if_not_exists(self, name, description):
        """
        Create a new test suite if it does not already exist, otherwise update the existing test suite.

        Args:
            name (str): The name of the test suite.
            description (str): The description of the test suite.

        Returns:
            dict: The response data containing the created or updated test suite.
        """
        test_suites = self.get_test_suites()
        for test_suite in test_suites["value"]:
            if test_suite["name"] == name:
                return self.update_test_suite(test_suite["id"], name, description)
        return self.create_test_suite(name, description)

    def add_test_case(self, id, test_case_id):
        """
        Add a test case to a test suite.

        Args:
            id (int): The ID of the test suite.
            test_case_id (int): The ID of the test case to add.

        Returns:
            dict: The response data containing the added test case.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites/{id}/testcases/{test_case_id}?api-version=5.0"
        data = {}
        response_data = {}
        try:
            response_data = self.requests_post(url, data)
        except Exception as e:
            exception_data = str(e)
            if not "Duplicate test case" in exception_data:
                raise e
        
        return response_data

    def get_test_case(self, id, test_case_id):
        """
        Get a test case in a test suite.

        Args:
            id (int): The ID of the test suite.
            test_case_id (int): The ID of the test case to add.

        Returns:
            dict: The response data containing the added test case.
        """
        url = f"/_apis/test/plans/{self.test_plan_id}/suites/{id}/testcases/{test_case_id}?api-version=5.0"
        response_data = self.requests_get(url)
        
        return response_data