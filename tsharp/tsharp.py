import os
import requests
import yaml

class Main:
    def __init__(self):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.config = self.load_yaml_config()

        self.update_variables()
        self.update_configurations()
        self.update_test_plans()

        self.save_yaml_config()
        
    def load_yaml_config(self):
        # Get the current script directory
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the config file name
        config_path = os.path.join(script_dir, 'config.yaml')
        
        config = {}

        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        return config
    
    def save_yaml_config(self):
        # Get the current script directory
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the config file name
        config_path = os.path.join(script_dir, 'config.yaml')
        
        with open(config_path, 'w') as file:
            yaml.dump(self.config, file)

    def run(self):
        print(f"# This is TSharp.")
        # pretty print the config in yaml format
        print(yaml.dump(self.config))



    def update_variables(self):
        print("## Updating variables")
        test_variables = TestVariables()
        for test_variable in self.config["variables"]:
            item = test_variables.create_test_variable_if_not_exists(test_variable)
            test_variable["id"] = item["id"]

    def update_configurations(self):
        print("## Updating configurations")
        test_configurations = TestConfigurations()
        for test_configuration in self.config["configurations"]:
            item = test_configurations.create_test_configuration_if_not_exists(test_configuration)
            test_configuration["id"] = item["id"]


    def update_test_plans(self):
        print("## Updating test plans")
        test_plans = TestPlans()
        for test_plan in self.config["test_plans"]:
            tp = test_plans.create_test_plan_if_not_exists(test_plan["name"], test_plan["description"])
            test_plan_id = tp["id"]
            test_plan["id"] = test_plan_id

            root_suite_id = tp["rootSuite"]["id"]
            test_suites = TestSuites(test_plan_id, root_suite_id)
            print(f"PlanId: {test_plan_id}")
            print(tp)
            print("### Updating test suites")
            for test_suite in test_plan.get("test_suites", []):
                ts = test_suites.create_test_suite_if_not_exists(test_suite["name"], test_suite["description"])
                test_suite_id = ts["id"]
                test_suite["id"] = test_suite_id
                print("Test Suite")
                print(ts)
                for test_case in test_suite.get("test_cases", []):
                    print("Test Case")
                    print(test_case)
                    test_case_id = test_case.get("id", 0)
                    work_item = WorkItem("Test Case", test_case["name"], test_case_id)

                    work_item.get()
                    wi = work_item.create_if_not_exists()
                    print("Work Item")
                    print(wi)
                    test_case["id"] = wi["id"]


class WorkItem:
    def __init__(self, workitem_type, name, id=0):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.workitem_type = workitem_type
        self._name = name
        self._id = id
        self._description = ""


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



    def build_work_item(self):     
        return [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "from": "",
                "value": self.name
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "from": "",
                "value": self.description
            }
            ]
    

    
    def get_by_name(self):
        # get all work items of type TestCase
        url = f"{self.url}/deixei/_apis/wit/wiql?api-version=7.1-preview.2"

        query = {
            "query": f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = '{self.workitem_type}' and [System.TeamProject] = 'deixei' and [System.Title] = '{self.name}'"
        }

        response = requests.post(url, json=query, auth=('PAT', self.pat))
        data = response.json()

        if data["workItems"]:
            self.id = data["workItems"][0]["id"]
            self.name = data["workItems"][0]["fields"]["System.Title"]
            self.description = data["workItems"][0]["fields"]["System.Description"]

        return data

    def get_by_id(self):
        url = f"{self.url}/deixei/_apis/wit/workitems/{self.id}?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        data = response.json()
        if data:
            self.name = data["fields"]["System.Title"]
            self.description = data["fields"]["System.Description"]

        return data
    
    def get(self):
        if self.id == 0:
            return self.get_by_name()
        return self.get_by_id()
    
    def create(self):
        url = f"{self.url}/deixei/_apis/wit/workitems/{self.workitem_type}?api-version=5.0"
        response = requests.post(url, auth=('PAT', self.pat), json=self.build_work_item())
        return response.json()
    
    def update(self):
        url = f"{self.url}/deixei/_apis/wit/workitems/{self.id}?api-version=5.0"
        response = requests.patch(url, auth=('PAT', self.pat), json=self.build_work_item)
        return response.json()
    
    def create_if_not_exists(self):
        if self.id != 0:
            return self.update()
        return self.create()    


class WorkItems:
    def __init__(self, workitem_type):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.workitem_type = workitem_type

    def get_all_work_items(self):
        # get all work items of type TestCase
        url = f"{self.url}/deixei/_apis/wit/wiql?api-version=7.1-preview.2"

        query = {
            "query": f"Select [System.Id], [System.Title] From WorkItems Where [System.WorkItemType] = '{self.workitem_type}'"
        }

        response = requests.post(url, json=query, auth=('PAT', self.pat))
        return response.json()


        


class TestSuites:
    def __init__(self, test_plan_id, parent_suite_id):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.test_plan_id = test_plan_id
        self.parent_suite_id = parent_suite_id

    def get_test_suites(self):
        url = f"{self.url}/deixei/_apis/test/plans/{self.test_plan_id}/suites?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
    
    def create_test_suite(self, name, description):
        url = f"{self.url}/deixei/_apis/test/plans/{self.test_plan_id}/suites/{self.parent_suite_id}/?api-version=5.0"
        response = requests.post(url, auth=('PAT', self.pat), json={
            "name": name,
            "suiteType": "StaticTestSuite"
        })
        return response.json()
    
    def get_test_suite(self, id):
        url = f"{self.url}/deixei/_apis/test/plans/{self.test_plan_id}/suites/{id}?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
    
    def update_test_suite(self, id, name, description):
        url = f"{self.url}/deixei/_apis/test/plans/{self.test_plan_id}/suites/{id}?api-version=5.0"
        response = requests.patch(url, auth=('PAT', self.pat), json={
            "description": description,
            "suiteType": "StaticTestSuite"
        })
        return response.json()
    
    def create_test_suite_if_not_exists(self, name, description):
        test_suites = self.get_test_suites()
        for test_suite in test_suites["value"]:
            if test_suite["name"] == name:
                return self.update_test_suite(test_suite["id"], name, description)
        return self.create_test_suite(name, description)



class TestPlans:
    def __init__(self):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")

    def get_test_plans(self):
        url = f"{self.url}/deixei/_apis/test/plans?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
        
    def create_test_plan(self, name, description):
        url = f"{self.url}/deixei/_apis/test/plans?api-version=5.0"
        response = requests.post(url, auth=('PAT', self.pat), json={
            "name": name,
            "description": description
        })
        return response.json()
    
    def get_test_plan(self, id):
        url = f"{self.url}/deixei/_apis/test/plans/{id}?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
    
    def update_test_plan(self, id, name, description):
        url = f"{self.url}/deixei/_apis/test/plans/{id}?api-version=5.0"
        response = requests.patch(url, auth=('PAT', self.pat), json={
            "name": name,
            "description": description
        })
        return response.json()
    
    def create_test_plan_if_not_exists(self, name, description):
        test_plans = self.get_test_plans()
        for test_plan in test_plans["value"]:
            if test_plan["name"] == name:
                return self.update_test_plan(test_plan["id"], name, description)
        return self.create_test_plan(name, description)

class TestConfigurations:
    def __init__(self):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")

    def get_test_configurations(self):
        url = f"{self.url}/deixei/_apis/test/configurations?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
        
    def create_test_configuration(self, configuration):
        url = f"{self.url}/deixei/_apis/test/configurations?api-version=5.0"
        response = requests.post(url, auth=('PAT', self.pat), json=configuration)
        return response.json()
    
    def get_test_configuration(self, id):
        url = f"{self.url}/deixei/_apis/test/configurations/{id}?api-version=5.0"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
    
    def update_test_configuration(self, id, configuration):
        url = f"{self.url}/deixei/_apis/test/configurations/{id}?api-version=5.0"
        response = requests.patch(url, auth=('PAT', self.pat), json=configuration)
        return response.json()
    
    def create_test_configuration_if_not_exists(self, configuration):
        test_configurations = self.get_test_configurations()
        for test_configuration in test_configurations["value"]:
            if test_configuration["name"] == configuration["name"]:
                return self.update_test_configuration(test_configuration["id"], configuration)
        return self.create_test_configuration(configuration)

class TestVariables:
    def __init__(self):
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")

    def get_test_variables(self):
        url = f"{self.url}/deixei/_apis/test/variables?api-version=5.0-preview.1"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()

    def create_test_variable(self, variable):
        url = f"{self.url}/deixei/_apis/test/variables?api-version=5.0-preview.1"
        response = requests.post(url, auth=('PAT', self.pat), json=variable)
        return response.json()

    def get_test_variable(self, id):
        url = f"{self.url}/deixei/_apis/test/variables/{id}?api-version=5.0-preview.1"
        response = requests.get(url, auth=('PAT', self.pat))
        return response.json()
    
    def update_test_variable(self, id, variable):
        url = f"{self.url}/deixei/_apis/test/variables/{id}?api-version=5.0-preview.1"
        response = requests.patch(url, auth=('PAT', self.pat), json=variable)
        return response.json()

    def create_test_variable_if_not_exists(self, variable):
        test_variables = self.get_test_variables()
        for test_variable in test_variables["value"]:
            if test_variable["name"] == variable["name"]:
                return self.update_test_variable(test_variable["id"], variable)
        return self.create_test_variable(variable)


if __name__ == "__main__":
    main = Main()
    main.run()

