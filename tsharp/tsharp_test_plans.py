from tsharp_base import TSharpBase

class TestPlans(TSharpBase):
    """
    A class that represents test plans in TSharp.

    This class provides methods to interact with test plans, such as retrieving test plans,
    creating new test plans, updating existing test plans, and checking if a test plan already exists.
    """

    def __init__(self):
        super().__init__()

    def get_test_plans(self):
        """
        Retrieves all test plans.

        Returns:
            dict: The response data containing the test plans.
        """
        url = f"/_apis/test/plans?api-version=5.0"
        response_data = self.requests_get(url)
        
        return response_data
        
    def create_test_plan(self, name, description):
        """
        Creates a new test plan.

        Args:
            name (str): The name of the test plan.
            description (str): The description of the test plan.

        Returns:
            dict: The response data containing the created test plan.
        """
        url = f"/_apis/test/plans?api-version=5.0"
        response_data = self.requests_post(url, data={
            "name": name,
            "description": description
        })
        
        return response_data
    
    def get_test_plan(self, id):
        """
        Retrieves a specific test plan.

        Args:
            id (int): The ID of the test plan.

        Returns:
            dict: The response data containing the test plan.
        """
        url = f"/_apis/test/plans/{id}?api-version=5.0"
        response_data = self.requests_get(url)

        return response_data
    
    def update_test_plan(self, id, name, description):
        """
        Updates an existing test plan.

        Args:
            id (int): The ID of the test plan.
            name (str): The new name of the test plan.
            description (str): The new description of the test plan.

        Returns:
            dict: The response data containing the updated test plan.
        """
        url = f"/_apis/test/plans/{id}?api-version=5.0"
        response_data = self.requests_patch(url, data={
            "name": name,
            "description": description
        })
        
        return response_data
    
    def create_test_plan_if_not_exists(self, name, description):
        """
        Creates a new test plan if it doesn't already exist, otherwise updates the existing test plan.

        Args:
            name (str): The name of the test plan.
            description (str): The description of the test plan.

        Returns:
            dict: The response data containing the created or updated test plan.
        """
        test_plans = self.get_test_plans()
        for test_plan in test_plans["value"]:
            if test_plan["name"] == name:
                return self.update_test_plan(test_plan["id"], name, description)
        return self.create_test_plan(name, description)

