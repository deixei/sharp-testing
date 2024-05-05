import os
import yaml
import argparse

from tsharp_constants import TARGET_ADO_URL, TARGET_ADO_PROJECT
from tsharp_base import TSharpBase, TSharpConfig
from tsharp_variables import TestVariables
from tsharp_configurations import TestConfigurations
from tsharp_test_plans import TestPlans
from tsharp_test_suites import TestSuites
from tsharp_workitems import WorkItem

class Main(TSharpBase):
    def __init__(self, 
                 config_folder:str=None, dataset:str=None, test_folder:str=None, 
                 ado_url:str=None, ado_pat:str=None, ado_project:str=None, 
                 verbose:str="v", 
                 run_var_update:str="y", run_config_update:str="y", run_tc_update:str="y"):
        
        super().__init__(ado_url, ado_pat, ado_project, verbose)
        self.test_folder = test_folder

        self.dataset = TSharpConfig(config_folder, dataset, verbose)

        self.run_var_update = run_var_update
        self.run_config_update = run_config_update
        self.run_tc_update = run_tc_update

    def run(self):
        print(f"#"*80)
        print(f"# Sharp Testing")
        print(f"#"*80)

        if "y" not in self.run_var_update:
            print("## Skipping Updating variables")
        else:
            self.update_variables()
        
        if "y" not in self.run_config_update:
            print("## Skipping Updating configurations")
        else:
            self.update_configurations()

        if "y" not in self.run_tc_update:
            print("## Skipping Updating test cases")
        else:
            self.update_test_plans()

        self.dataset.save_all()

        if self.verbose and "v" in self.verbose:
            print("## Dataset")
            if "y" not in self.run_var_update:
                print("### Variables")
                print(yaml.dump(self.dataset.vars))
            
            if "y" not in self.run_config_update:
                print("### Configurations")
                print(yaml.dump(self.dataset.configs))
            
            if "y" not in self.run_tc_update:
                print("### Test Cases")
                print(yaml.dump(self.dataset.testcases))

        

    def update_variables(self):
        print("## Updating variables")
        test_variables = TestVariables(self.ado_url, self.ado_pat, self.ado_project, self.verbose)
        for test_variable in self.dataset.vars["variables"]:
            item = test_variables.create_test_variable_if_not_exists(test_variable)
            test_variable["id"] = item["id"]

    def update_configurations(self):
        print("## Updating configurations")
        test_configurations = TestConfigurations(self.ado_url, self.ado_pat, self.ado_project, self.verbose)
        for test_configuration in self.dataset.configs["configurations"]:
            item = test_configurations.create_test_configuration_if_not_exists(test_configuration)
            test_configuration["id"] = item["id"]

    def set_test_folder(self, folder):
        if self.verbose and "vvv" in self.verbose:
            print(f"Creating test folder for {folder}")

        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)

        test_folder = os.path.join(self.test_folder, f"test_{folder}")

        if self.verbose and "vvv" in self.verbose:
            print(f"Test folder: {test_folder}")

        if not os.path.exists(test_folder):
            os.makedirs(test_folder)

        return test_folder
    
    def set_test_file(self, folder, file):
        test_file = os.path.join(folder, f"test_{file}.py")
        
        if not os.path.exists(test_file):
            with open(test_file, 'w') as f:
                f.write("# This is autogenerated test suite file for sharp testing\n")
                f.write("import os\n")
                f.write("import pytest\n")

        return test_file

    def set_test_function(self, file, function_name, test_case, work_item):
        # create the function if it does not exist
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if f"def test_{function_name}(" in line:
                    return

        with open(file, 'a') as f:
            f.write(f"\n")
            f.write(f"@pytest.mark.test_id({work_item['id']})\n")
            f.write(f"def test_{function_name}(ado_config, test_run_id, test_result_id):\n")

            f.write(f"\t\"\"\"\n")
            f.write(f"\t{test_case['description']}\n")
            f.write(f"\tDetails:{test_case}\n")
            f.write(f"\n")
            f.write(f"\tArgs:\n")
            f.write(f"\t\tado_config: The ADO configuration.\n")
            f.write(f"\t\ttest_run_id: The ID of the test run.\n")
            f.write(f"\t\ttest_result_id: The ID of the test result.\n")
            f.write(f"\n")
            f.write(f"\tReturns:\n")
            f.write(f"\t\tNone\n")
            f.write(f"\t\"\"\"\n")

            f.write(f"\twork_item_id={work_item['id']}\n")
            f.write(f"\ttest_case_description=\"{test_case['description']}\"\n")

            f.write(f"\tprint(\"ado_config:\", ado_config)\n")
            f.write(f"\tprint(\"test_run_id:\", test_run_id)\n")
            f.write(f"\tprint(\"test_result_id:\", test_result_id)\n")
            
            f.write(f"\tassert True\n")
            f.write(f"\n")

    def update_test_plans(self):
        print("## Updating test plans")
        test_plans = TestPlans(self.ado_url, self.ado_pat, self.ado_project, self.verbose)
        for test_plan in self.dataset.testcases["test_plans"]:
            tp = test_plans.create_test_plan_if_not_exists(test_plan["name"], test_plan["description"])

            f = self.set_test_folder(test_plan["name"])

            test_plan_id = tp["id"]
            test_plan["id"] = test_plan_id

            root_suite_id = tp["rootSuite"]["id"]
            test_suites = TestSuites(test_plan_id, root_suite_id, self.ado_url, self.ado_pat, self.ado_project, self.verbose)
            
            if self.verbose and "v" in self.verbose: print(f"PlanId: {test_plan_id}")
            if self.verbose and "vv" in self.verbose: print(tp)
            
            print("### Updating test suites")
            for test_suite in test_plan.get("test_suites", []):
                test_suite_name = test_suite["name"]
                ts = test_suites.create_test_suite_if_not_exists(test_suite_name, test_suite["description"])

                t = self.set_test_file(f, test_suite_name)

                test_suite_id = ts["id"]
                test_suite["id"] = test_suite_id
                if self.verbose and "v" in self.verbose: print(f"Test Suite Id: {test_suite_id}")
                if self.verbose and "vv" in self.verbose: print(ts)
                for test_case in test_suite.get("test_cases", []):
                    if self.verbose and "v" in self.verbose: print(" - Test Case processing")
                    if self.verbose and "vv" in self.verbose: print(test_case)
                    test_case_id = test_case.get("id", 0)
                    work_item = WorkItem("Test Case", test_case["name"], test_case_id, self.ado_url, self.ado_pat, self.ado_project, self.verbose)
                    work_item.description = test_case.get("description", "")
                    work_item.test_plan = test_plan["name"]
                    work_item.suite_name = test_suite_name


                    work_item.get()
                    wi = work_item.create_if_not_exists()
                    if self.verbose and "v" in self.verbose: print("Work Item")
                    if self.verbose and "vv" in self.verbose: print(wi)
                    test_case["id"] = wi["id"]

                    self.set_test_function(t, test_case["name"], test_case, wi)

                    test_suites.add_test_case(test_suite_id, test_case["id"])


def parse_args():
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.join(script_dir, "..")

    default_config_folder = os.path.join(parent_dir, "configurations")
    default_test_folder = os.path.join(parent_dir, "tests")

    parser = argparse.ArgumentParser(description='Sharp Testing from deixei')
    parser.add_argument('--config_folder', type=str, default=default_config_folder, help='Configuration folder')
    parser.add_argument('--dataset', type=str, default='data_set_1', help='Configuration Dataset folder name')
    parser.add_argument('--test_folder', type=str, default=default_test_folder, help='Folder for PyTest Test Cases')

    parser.add_argument('--ado_url', type=str, default=os.environ.get('DX_ADO_URL', TARGET_ADO_URL), help='Azure DevOps URL: https://dev.azure.com/deixeicom')
    parser.add_argument('--ado_project', type=str, default=os.environ.get('AZURE_DEVOPS_EXT_PROJECT', TARGET_ADO_PROJECT), help='Azure DevOps Project: deixei')
    parser.add_argument('--ado_pat', type=str, default=os.environ.get('AZURE_DEVOPS_EXT_PAT'), help='Azure DevOps PAT')

    parser.add_argument('--verbose', type=str, default="v", help='Verbose output')

    parser.add_argument('--run_var_update', type=str, default="y", choices=["y", "n"] ,help='Update variables')
    parser.add_argument('--run_config_update', type=str, default="y", choices=["y", "n"] ,help='Update configurations')
    parser.add_argument('--run_tc_update', type=str, default="y", choices=["y", "n"] ,help='Update test cases')

    return parser.parse_args()

def main():
    """
    Entry point of the program.
    
    Parses command line arguments, validates the input, and runs the main logic.
    """
    args = parse_args()

    if args.config_folder is None:
        raise ValueError("config_folder is not set")
    
    if os.path.exists(args.config_folder) is False:
        raise ValueError("config_folder does not exist")
    
    if args.dataset is None:
        raise ValueError("dataset is not set")
    
    dataset_folder = os.path.join(args.config_folder, args.dataset)
    if os.path.exists(dataset_folder) is False:
        raise ValueError("dataset does not exist")
    
    if args.test_folder is None:
        raise ValueError("test_folder is not set")
    
    if os.path.exists(args.test_folder) is False:
        # TODO: potentially create the folder if it does not exist
        raise ValueError("test_folder does not exist")

    if args.ado_url is None:
        raise ValueError("ado_url is not set")
    
    if args.ado_pat is None:
        raise ValueError("ado_pat is not set")
    
    if args.ado_project is None:
        raise ValueError("ado_project is not set")

    # check if base url has a valid URL regex
    if not args.ado_url.startswith("https://"):
        raise ValueError("Invalid URL format for Azure DevOps")

    main = Main(args.config_folder, args.dataset, args.test_folder, args.ado_url, args.ado_pat, args.ado_project, args.verbose, args.run_var_update, args.run_config_update, args.run_tc_update)
    main.run()

if __name__ == "__main__":
    main()
    

