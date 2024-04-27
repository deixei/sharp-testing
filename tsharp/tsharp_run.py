import base64
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
        print(run)

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
    
    def iterate_test_results(self, results):
        if results is None:
            return
        if results["count"] == 0:
            return
        
        tc = TestConfigurations()
        for result in results["value"]:
            test_point_id = result["testPoint"]["id"]
            automatedTestStorage = result["automatedTestStorage"]
            automatedTestName = result["automatedTestName"]
            automatedTestType = result["automatedTestType"]
            id = result["id"]
            
            print(automatedTestStorage)
            print(automatedTestName)
            print(automatedTestType)
            print(id)

            print(test_point_id)
            configuration_id = result["configuration"]["id"]
            print(f"configuration_id: {configuration_id}")
            config = tc.get_test_configuration(configuration_id)
            config_values = config["values"]
            encode_config_values = encode_list(config_values)
            print(config_values)

            # invoke a pytest test function

            test_func_name = f"./{automatedTestStorage}/{automatedTestName}"

            retcode = pytest.main(["--ado_config", encode_config_values ,test_func_name, "--junitxml", f"junit/test-results-{test_point_id}.xml"])

            print(f"retcode: {retcode}")


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
