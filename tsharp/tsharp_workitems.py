from tsharp_base import TSharpBase

class WorkItems(TSharpBase):
    """
    Represents a collection of work items of a specific type.

    Args:
        workitem_type (str): The type of work items to retrieve.

    Attributes:
        workitem_type (str): The type of work items.

    """

    def __init__(self, workitem_type):
        super().__init__()

        self.workitem_type = workitem_type

    def get_all_work_items(self):
        """
        Retrieves all work items of the specified type.

        Returns:
            dict: The response data containing the work items.

        """

        # get all work items of type TestCase
        url = f"/_apis/wit/wiql?api-version=7.1-preview.2"

        query = {
            "query": f"Select [System.Id], [System.Title] From WorkItems Where [System.WorkItemType] = '{self.workitem_type}'"
        }

        response_data = self.requests_post(url, data=query)

        return response_data


class WorkItem(TSharpBase):
    """
    Represents a work item in the TSharp system.

    Args:
        workitem_type (str): The type of the work item.
        name (str): The name of the work item.
        id (int, optional): The ID of the work item. Defaults to 0.

    Attributes:
        workitem_type (str): The type of the work item.
        name (str): The name of the work item.
        id (int): The ID of the work item.
        description (str): The description of the work item.
        plan_name (str): The name of the test plan associated with the work item.
        suite_name (str): The name of the test suite associated with the work item.
    """

    def __init__(self, workitem_type, name, id=0):
        super().__init__()
        self.workitem_type = workitem_type
        self._name = name
        self._id = id
        self._description = ""
        self._plan_name = ""
        self._suite_name = ""

    @property
    def test_plan(self):
        """
        Returns the name of the test plan.

        :return: The name of the test plan.
        """
        return self._plan_name

    @test_plan.setter
    def test_plan(self, value):
        """
        Sets the test plan name.

        Args:
            value (str): The name of the test plan.

        Returns:
            None
        """
        self._plan_name = value

    @property
    def suite_name(self):
        """
        Returns the name of the test suite.

        :return: The name of the test suite.
        """
        return self._suite_name

    @suite_name.setter
    def suite_name(self, value):
        self._suite_name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value



    @property
    def test_function_name(self):
        # Associated Automation, https://learn.microsoft.com/en-us/azure/devops/boards/queries/build-test-integration?view=azure-devops#fields
        ## test_my_test_plan2/test_my_test_suite_2.py::test_my_test_case_2
        ## Automated test name, Microsoft.VSTS.TCM.AutomatedTestName
        ## test_my_test_suite_2.py::test_my_test_case_2
        return f"test_{self.suite_name}.py::test_{self.name}"
    
    @property
    def test_folder(self):
        ## Automated test storage, Microsoft.VSTS.TCM.AutomatedTestStorage
        ## tests/test_my_test_plan2
        ## Automated test type, Microsoft.VSTS.TCM.AutomationStatus
        return f"tests/test_{self.test_plan}"


    def build_work_item(self):
        return [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": self.name
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": self.description
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.automatedTestId",
                "value": self.test_function_name
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestName",
                "value": self.test_function_name
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestStorage",
                "value": self.test_folder
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestType",
                "value": "Automated"
            }
            ]

    def get_by_name(self):
        # get all work items of type TestCase
        url = f"/_apis/wit/wiql?api-version=7.1-preview.2"

        query = {
            "query": f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = '{self.workitem_type}' and [System.Title] = '{self.name}'"
        }

        data = self.requests_post(url, data=query)

        if data["workItems"]:
            self.id = data["workItems"][0]["id"]
            #TODO: this can be a bug with invalide charecters
            #self.name = data["workItems"][0]["fields"]["System.Title"]
            #self.description = data["workItems"][0]["fields"]["System.Description"]

        return data

    def get_by_id(self):
        url = f"/_apis/wit/workitems/{self.id}?api-version=5.0&$expand=all"
        data = self.requests_get(url)

        if data:
            self.name = data["fields"]["System.Title"]
            self.description = data["fields"].get("System.Description", "")

        return data

    def get(self):
        if self.id == 0:
            return self.get_by_name()
        return self.get_by_id()

    def create(self):
        url = f"/_apis/wit/workitems/${self.workitem_type}?api-version=5.0"
        json_data=self.build_work_item()
        response_data = self.requests_patch(url,data=json_data, include_content_type=True)

        return response_data

    def update(self):
        url = f"/_apis/wit/workitems/{self.id}?api-version=5.0"
        json_data=self.build_work_item()
        response_data = self.requests_patch(url,data=json_data, include_content_type=True)

        return response_data

    def create_if_not_exists(self):
        if self.id != 0:
            return self.update()
        return self.create()
