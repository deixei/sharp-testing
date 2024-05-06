import os
import base64
import requests
import argparse
import pytest
import json
from datetime import datetime
import xml.etree.ElementTree as ET

from tsharp_base import TSharpBase
from tsharp import TestConfigurations, TestVariables
from tsharp_constants import TARGET_ADO_URL, TARGET_ADO_PROJECT, VERBOSE
from tsharp_pytest_plugin import TSharpPyTestPlugin

class TSharpRunner(TSharpBase):

    def __init__(self, run_id:str="0", test_folder:str=None, 
                 ado_url:str=None, ado_pat:str=None, ado_project:str=None, 
                 print_verbose:str="v", junitxml_folder:str=None,
                 azure_tenant:str=None, azure_client_id:str=None, azure_secret:str=None):
        super().__init__(ado_url, ado_pat, ado_project, print_verbose)
        self.run_id = run_id
        self.test_folder = test_folder
        self.junitxml_folder = junitxml_folder

        self.azure_tenant = azure_tenant
        self.azure_client_id = azure_client_id
        self.azure_secret = azure_secret
    
    def execute(self):
        print(f"#"*80)
        print(f"# Sharp Testing Runner")
        print(f"#"*80)        
        if self.verbose and "v" in self.verbose: print(f"Test Run Id: {self.run_id}")

        run = self.get_run_id()
        if self.verbose and "vv" in self.verbose: print(run)

        results = self.get_test_results()
        if self.verbose and "vv" in self.verbose: print(results)

        self.iterate_test_results(results)

    def get_run_id(self):
        url = f"/_apis/test/runs/{self.run_id}?includeDetails=True&api-version=7.1-preview.3"
        response_data = self.requests_get(url)

        return response_data
    
    def get_test_results(self):
        url = f"/_apis/test/runs/{self.run_id}/results?api-version=7.1-preview.6"
        response_data = self.requests_get(url)

        return response_data
    
    def complete_test_run(self, run_id, test_result_id, planId, test_point_id, test_case_id, output_file, retcode):
        url = f"/_apis/test/runs/{run_id}/results?api-version=7.1-preview.6"
        current_time = datetime.now().isoformat()
        # outcome	string
        # Test outcome of test result. Valid values = (Unspecified, None, Passed, Failed, Inconclusive, Timeout, Aborted, Blocked, NotExecuted, Warning, Error, NotApplicable, Paused, InProgress, NotImpacted)
        
        # read xml file output_file
        current_path_for_this_file = os.path.dirname(os.path.realpath(__file__))
        output_file_full_path = os.path.join(current_path_for_this_file, "..", output_file)
        if os.path.exists(output_file_full_path) is False:
            raise ValueError(f"Output file {output_file_full_path} does not exist")
        
        tree = ET.parse(output_file_full_path)
        root = tree.getroot()

        if root is None:
            raise ValueError(f"Root element not found in {output_file_full_path}")

        ts_element = root.find("testsuite")
        if ts_element is None:
            raise ValueError(f"TestSuite element not found in {output_file_full_path}")
        
        if self.verbose and "vvv" in self.verbose: print(ts_element.attrib)

        tc_element = ts_element.find("testcase")
        if tc_element is None:
            raise ValueError(f"TestCase element not found in {output_file_full_path}")
        
        if self.verbose and "vvv" in self.verbose: print(tc_element.attrib)

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
                if self.verbose and "vvv" in self.verbose: print(failure_element.attrib)
                if self.verbose and "vvv" in self.verbose: print(failure_element.text)

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
        response_data = self.requests_patch(url, data)

        ## data = {'$id': '1', 'innerException': None, 'message': 'Value cannot be null.\r\nParameter name: results', 'typeName': 'Microsoft.VisualStudio.Services.Common.VssServiceException, Microsoft.VisualStudio.Services.Common', 'typeKey': 'VssServiceException', 'errorCode': 0, 'eventId': 3000}
        ## handle the response data when there is an error indicated bz the $id=1

        id = response_data.get("$id", None)
        if id is not None:
            print("Error: ", response_data["message"])

        attachment_res = self.add_test_result_attachment(run_id, test_result_id, output_file, "junit-test-results.xml" ,comment)

        print(attachment_res)

        return response_data

    def add_test_result_attachment(self, run_id, test_result_id, attachment_file, attachment_filename, comment):
        url = f"/_apis/test/runs/{run_id}/results/{test_result_id}/attachments?api-version=7.1-preview.1"

        if os.path.exists(attachment_file) is False:
            raise ValueError(f"Attachment file {attachment_file} does not exist")

        data = {
            "stream": base64.b64encode(open(attachment_file, "rb").read()).decode(),
            "fileName": attachment_filename,
            "comment": comment,
            "attachmentType": "GeneralAttachment"
        }
        response_data = self.requests_post(url, data)

        return response_data


    def iterate_test_results(self, results):
        if results is None:
            return
        if results["count"] == 0:
            return
        
        tc = TestConfigurations(self.ado_url, self.ado_pat, self.ado_project, self.verbose)
        for result in results["value"]:
            id = result["id"]
            test_point_id = result["testPoint"]["id"]
            planId = result["testPlan"]["id"]

            automatedTestStorage = result["automatedTestStorage"]
            automatedTestName = result["automatedTestName"]
            automatedTestType = result["automatedTestType"]
            #print(result)
            test_case_id =  result["testCase"]["id"]

            if self.verbose and "vv" in self.verbose: print(f"Storage: {automatedTestStorage}; Name: {automatedTestName}; Type: {automatedTestType}")

            if automatedTestType != "Automated":
                print("Test Type is not Automated")
                continue
            else:
                print("Test Type is Automated")
                print(f"Starting execution for Test Case ID: {test_case_id}")

                configuration_id = result["configuration"]["id"]
                config = tc.get_test_configuration(configuration_id)
                config_values = config["values"]
                encode_config_values = encode_list(config_values)
            
                if self.verbose and "vv" in self.verbose: print(f"Configuration (id:{configuration_id}): ", config_values)

                # invoke a pytest test function

                test_folder_parent = os.path.join(self.test_folder, "..")
                test_func_name = os.path.join(test_folder_parent, automatedTestStorage, automatedTestName)
                #test_func_name = f"./{automatedTestStorage}/{automatedTestName}"

                output_file = os.path.join(self.junitxml_folder, f"test-results-{test_point_id}.xml")

                if self.verbose and "vv" in self.verbose: print(f"Test Function Name: {test_func_name}; Output File: {output_file}")

                retcode = pytest.main([
                    "-s", 
                    test_func_name, 
                    "--junitxml", output_file,
                    "--ado_config", encode_config_values,
                    "--test_run_id", f"{self.run_id}",
                    "--test_result_id", f"{id}",
                    "--ado_url", f"{self.ado_url}",
                    "--ado_pat", f"{self.ado_pat}",
                    "--ado_project", f"{self.ado_project}",
                    "--print_verbose", f"{self.verbose}",

                    "--azure_tenant", f"{self.azure_tenant}",
                    "--azure_client_id", f"{self.azure_client_id}",
                    "--azure_secret", f"{self.azure_secret}",

                    ], 
                    plugins=[TSharpPyTestPlugin()])

                u1 = self.complete_test_run(self.run_id, id, planId, test_point_id, test_case_id, output_file, retcode)

                

                print("complete_test_run:", u1)




def encode_list(list_values):
    json_string = json.dumps(list_values)
    encoded_string = base64.b64encode(json_string.encode()).decode()
    return encoded_string

#TODO: remove this in PROD
RUN_ID = "1000229"

def parse_args():
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.join(script_dir, "..")

    default_test_folder = os.path.join(parent_dir, "tests")
    default_junitxml_folder = os.path.join(parent_dir, "junit")

    parser = argparse.ArgumentParser(description='Sharp Testing Runner from deixei')

    parser.add_argument('--run_id', default=os.environ.get('RUN_ID', RUN_ID), help='The test run ID')
    
    parser.add_argument('--test_folder', type=str, default=default_test_folder, help='Folder for PyTest Test Cases')
    parser.add_argument('--junitxml_folder', type=str, default=default_junitxml_folder, help='Folder for JUnit XML Test Results')

    parser.add_argument('--ado_url', type=str, default=os.environ.get('DX_ADO_URL', TARGET_ADO_URL), help='Azure DevOps URL: https://dev.azure.com/deixeicom')
    parser.add_argument('--ado_project', type=str, default=os.environ.get('AZURE_DEVOPS_EXT_PROJECT', TARGET_ADO_PROJECT), help='Azure DevOps Project: deixei')
    parser.add_argument('--ado_pat', type=str, default=os.environ.get('AZURE_DEVOPS_EXT_PAT'), help='Azure DevOps PAT')

    parser.add_argument('--verbose', type=str, default="v",choices=["v", "vv", "vvv"] , help='Verbose output')

    parser.add_argument('--azure_tenant', type=str, default=os.environ.get('AZURE_TENANT'), help='Azure TENANT')
    parser.add_argument('--azure_client_id', type=str, default=os.environ.get('AZURE_CLIENT_ID'), help='Azure CLIENT_ID')
    parser.add_argument('--azure_secret', type=str, default=os.environ.get('AZURE_SECRET'), help='Azure SECRET')

    return parser.parse_args()

def main():
    args = parse_args()

    if args.run_id is None:
        raise ValueError("run_id is not set")
    
    if args.test_folder is None:
        raise ValueError("test_folder is not set")
    
    if os.path.exists(args.test_folder) is False:
        # TODO: potentially create the folder if it does not exist
        raise ValueError("test_folder does not exist")

    if args.junitxml_folder is None:
        raise ValueError("junitxml_folder is not set")
    
    if os.path.exists(args.junitxml_folder) is False:
        os.makedirs(args.junitxml_folder)

    if args.ado_url is None:
        raise ValueError("ado_url is not set")
    
    if args.ado_pat is None:
        raise ValueError("ado_pat is not set")
    
    if args.ado_project is None:
        raise ValueError("ado_project is not set")

    # check if base url has a valid URL regex
    if not args.ado_url.startswith("https://"):
        raise ValueError("Invalid URL format for Azure DevOps")        


    test_execution_engine = TSharpRunner(args.run_id, args.test_folder, args.ado_url, args.ado_pat, args.ado_project, args.verbose, args.junitxml_folder, args.azure_tenant, args.azure_client_id, args.azure_secret)
    test_execution_engine.execute()

if __name__ == "__main__":
    main()
