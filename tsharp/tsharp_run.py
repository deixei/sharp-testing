import base64
from datetime import datetime
import os
import requests
import argparse
from tsharp import TestConfigurations, TestVariables
import pytest
import json

class MainRun:

    def __init__(self, run_id):
        self.run_id = run_id
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        
        if self.url is None:
            raise ValueError("DX_ADO_URL is not set")
        if self.pat is None:
            raise ValueError("AZURE_DEVOPS_EXT_PAT is not set")
        if self.run_id is None:
            raise ValueError("RUN_ID is not set")

        self.project = "deixei"
    
    def execute(self):
        print(f"This is a test run {self.run_id}")
        print(f"This is the url {self.url}")
        print(f"This is the pat {self.pat}")

        run = self.get_run_id()
        #print(run)

        results = self.get_test_results()
        print(results)

        self.iterate_test_results(results)

    def get_run_id(self):
        url = f"{self.url}/{self.project}/_apis/test/runs/{self.run_id}?includeDetails=True&api-version=7.1-preview.3"

        response = requests.get(url, auth=('PAT', self.pat))
        data = response.json()

        return data
    
    def get_test_results(self):
        url = f"{self.url}/{self.project}/_apis/test/runs/{self.run_id}/results?api-version=7.1-preview.6"

        response = requests.get(url, auth=('PAT', self.pat))
        data = response.json()

        return data
    
    def complete_test_run(self, run_id, test_result_id, planId, test_point_id, test_case_id, output_file):
        url = f"{self.url}/{self.project}/_apis/test/runs/{run_id}/results?api-version=7.1-preview.6"
        current_time = datetime.now().isoformat()
        # outcome	string
        # Test outcome of test result. Valid values = (Unspecified, None, Passed, Failed, Inconclusive, Timeout, Aborted, Blocked, NotExecuted, Warning, Error, NotApplicable, Paused, InProgress, NotImpacted)
        
        # read xml file output_file
        with open(output_file, "r") as file:
            content = file.read()




        data = [{
            "id": test_result_id,
            "comment": "Test run completed",
            "state": "Completed",
            "completedDate": current_time,
            "errorMessage": "No errors",
            "outcome": "Passed",
            "testPoint": {
                "id": test_point_id
            },
            "testPlan": {
                "id": planId
            },
            "testRun": {
                "id": run_id
            },
            "testCase": {
                "id": test_case_id
            }

        }]

        response = requests.patch(url, auth=('PAT', self.pat), json=data)
        data = response.json()

        return data


    def iterate_test_results(self, results):
        if results is None:
            return
        if results["count"] == 0:
            return
        
        tc = TestConfigurations()
        for result in results["value"]:
            id = result["id"]
            test_point_id = result["testPoint"]["id"]
            planId = result["testPlan"]["id"]

            automatedTestStorage = result["automatedTestStorage"]
            automatedTestName = result["automatedTestName"]
            automatedTestType = result["automatedTestType"]
            #print(result)
            test_case_id =  result["testCase"]["id"]

            print(f"Storage: {automatedTestStorage}; Name: {automatedTestName}; Type: {automatedTestType}")

            if automatedTestType != "Automated":
                print("Test Type is not Automated")
                continue
            else:
                print("Test Type is Automated")
                print("Id:", id)

                print("Test Point:", test_point_id)
                configuration_id = result["configuration"]["id"]
                config = tc.get_test_configuration(configuration_id)
                config_values = config["values"]
                encode_config_values = encode_list(config_values)
            
                print(f"Configuration (id:{configuration_id}): ", config_values)

                # invoke a pytest test function

                test_func_name = f"./{automatedTestStorage}/{automatedTestName}"
                
                output_file = f"junit/test-results-{test_point_id}.xml"

                print(f"Test Function Name: {test_func_name}; Output File: {output_file}")

                retcode = pytest.main(["-s", "--ado_config", encode_config_values ,test_func_name, "--junitxml", output_file])

                print(f"retcode: {retcode}")

                u1 = self.complete_test_run(self.run_id, id, planId, test_point_id, test_case_id, output_file)
                print(u1)



def encode_list(list_values):
    json_string = json.dumps(list_values)
    encoded_string = base64.b64encode(json_string.encode()).decode()
    return encoded_string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', default=os.environ.get('RUN_ID'))
    args = parser.parse_args()

    test_execution_engine = MainRun(args.run_id)
    test_execution_engine.execute()

if __name__ == "__main__":
    main()
