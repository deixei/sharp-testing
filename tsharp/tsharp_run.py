import os
import base64
import requests
import argparse
import pytest
import json
from datetime import datetime
import xml.etree.ElementTree as ET

from tsharp import TestConfigurations, TestVariables
from tsharp_constants import TARGET_ADO_URL, TARGET_ADO_PROJECT, VERBOSE


def verbose_print(message):
    if VERBOSE == True:
        print(message)


class TSharpPyTestPlugin:
    def pytest_sessionfinish(self):
        verbose_print("*** [TSharpPyTestPlugin]: test run reporting finishing")

class MainRun:

    def __init__(self, run_id):
        self.run_id = run_id

        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.project = os.environ.get("AZURE_DEVOPS_EXT_PROJECT", TARGET_ADO_PROJECT)
        
        if self.url is None:
            raise ValueError("DX_ADO_URL is not set")
        
        if self.pat is None:
            raise ValueError("AZURE_DEVOPS_EXT_PAT is not set")
        
        if self.run_id is None:
            raise ValueError("RUN_ID is not set")

        if self.project is None:
            raise ValueError("AZURE_DEVOPS_EXT_PROJECT is not set")
    
    def execute(self):
        #verbose_print(f"This is a test run {self.run_id}")
        #verbose_print(f"This is the url {self.url}")
        #verbose_print(f"This is the pat {self.pat}")

        run = self.get_run_id()
        #verbose_print(run)

        results = self.get_test_results()
        #verbose_print(results)

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
    
    def complete_test_run(self, run_id, test_result_id, planId, test_point_id, test_case_id, output_file, retcode):
        url = f"{self.url}/{self.project}/_apis/test/runs/{run_id}/results?api-version=7.1-preview.6"
        current_time = datetime.now().isoformat()
        # outcome	string
        # Test outcome of test result. Valid values = (Unspecified, None, Passed, Failed, Inconclusive, Timeout, Aborted, Blocked, NotExecuted, Warning, Error, NotApplicable, Paused, InProgress, NotImpacted)
        
        # read xml file output_file
        current_path_for_this_file = os.path.dirname(os.path.realpath(__file__))
        output_file_full_path = os.path.join(current_path_for_this_file, "..", output_file)

        tree = ET.parse(output_file_full_path)
        root = tree.getroot()

        ts_element = root.find("testsuite")
        #verbose_print(ts_element.attrib)

        tc_element = ts_element.find("testcase")
        #verbose_print(tc_element.attrib)

        comment = "Nothing"
        errorMessage = "Nothing"
        outcome = "Failed"


        if retcode == 0:
            outcome = "Passed"
            errorMessage = "No errors"
            comment = "Test run completed by TSharp-Test-Runner"
        else:
            outcome = "Failed"

            failure_element = tc_element.find("failure")
            if failure_element is not None:
                #verbose_print(failure_element.attrib)
                #verbose_print(failure_element.text)

                errorMessage = failure_element.text
                comment = failure_element.attrib["message"]
            else:
                errorMessage = "No error message found"
                comment = "Test run failed"
            

        data = [{
            "id": test_result_id,
            "comment": comment,
            "state": "Completed",
            "completedDate": current_time,
            "errorMessage": errorMessage,
            "outcome": outcome,
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
        #print("Data: ", data)
        response = requests.patch(url, auth=('PAT', self.pat), json=data)
        data = response.json()

        ## data = {'$id': '1', 'innerException': None, 'message': 'Value cannot be null.\r\nParameter name: results', 'typeName': 'Microsoft.VisualStudio.Services.Common.VssServiceException, Microsoft.VisualStudio.Services.Common', 'typeKey': 'VssServiceException', 'errorCode': 0, 'eventId': 3000}
        ## handle the response data when there is an error indicated bz the $id=1

        id = data.get("$id", None)
        if id is not None:
            print("Error: ", data["message"])

        attachment_res = self.add_test_result_attachment(run_id, test_result_id, output_file, "junit-test-results.xml" ,comment)

        print(attachment_res)

        return data

    def add_test_result_attachment(self, run_id, test_result_id, attachment_file, attachment_filename, comment):
        url = f"{self.url}/{self.project}/_apis/test/runs/{run_id}/results/{test_result_id}/attachments?api-version=7.1-preview.1"

        data = {
            "stream": base64.b64encode(open(attachment_file, "rb").read()).decode(),
            "fileName": attachment_filename,
            "comment": comment,
            "attachmentType": "GeneralAttachment"
        }

        response = requests.post(url, auth=('PAT', self.pat), json=data)
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

            #verbose_print(f"Storage: {automatedTestStorage}; Name: {automatedTestName}; Type: {automatedTestType}")

            if automatedTestType != "Automated":
                print("Test Type is not Automated")
                continue
            else:
                print("Test Type is Automated")
                configuration_id = result["configuration"]["id"]
                config = tc.get_test_configuration(configuration_id)
                config_values = config["values"]
                encode_config_values = encode_list(config_values)
            
                #verbose_print(f"Configuration (id:{configuration_id}): ", config_values)

                # invoke a pytest test function

                test_func_name = f"./{automatedTestStorage}/{automatedTestName}"
                
                output_file = f"junit/test-results-{test_point_id}.xml"

                #verbose_print(f"Test Function Name: {test_func_name}; Output File: {output_file}")

                retcode = pytest.main([
                    "-s", 
                    test_func_name, 
                    "--junitxml", output_file,
                    "--ado_config", encode_config_values,
                    "--test_run_id", f"{self.run_id}",
                    "--test_result_id", f"{id}"
                    ], 
                    plugins=[TSharpPyTestPlugin()])

                u1 = self.complete_test_run(self.run_id, id, planId, test_point_id, test_case_id, output_file, retcode)

                

                print("complete_test_run:", u1)




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
