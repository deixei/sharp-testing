# Sharp Testing Framework

Sharpe Testing is an open source framework for defining test plans, test suites and test cases in YAML format. It also allows defining different configurations and configuration variables for testing. The framework integrates with Azure DevOps Testing hub by generating the required work items, and generates pytest files linked to the test cases. It takes advantage of the pytest framework and uploads the execution report.

## Installation

You can install Sharp Testing using this repo:

Clone me and adapt the CI pipeline

## Usage

CLI

The helper command for Sharpe Testing is tsharp. You can use it to create a new test plan, test suite or test case:

python3 tsharp/tsharp.py

You can also use the tsharp command to run tests:

python3 tsharp/tsharp_run.py --run_id 1000215

You can load and map variables dynamically from external sources, the idea is to load ADO test variable and ADO test configurations from azure based information; it can later be extended to work with your CMDB, or other APIs.

python3 tsharp/tsharp_map.py

## Azure DevOps Integration

The Sharpe Testing framework integrates with Azure DevOps Testing hub. It generates the required work items for testing. You can use the tsharp_run runner in Azure DevOps to run tests.

## YAML Configuration

The Sharpe Testing framework allows defining test plans, test suites and test cases in YAML format. You can define different configurations and configuration variables for testing. Here is an example of a test plan YAML file:

```yaml
name: My Test Plan
description: This is my test plan
...
```

## License

Sharpe Testing is licensed under the MIT License. See the LICENSE file for more information.

## Introduction

Based in Python, YAML, PyTest and Azure DevOps

Need a command to upload a test case id with a function

Need a command to create test suites; test Plans and Test cases;

## APIS

https://learn.microsoft.com/en-us/rest/api/azure/devops/test/configurations/create?view=azure-devops-rest-5.0&tabs=HTTP

## Other Notes


### run

python3 tsharp/tsharp.py

### notes on testing stuff

pytest pytest-azurepipelines

pytest --doctest-modules --junitxml=junit/test-results.xml

pytest test_my_test_plan2/test_my_test_suite_2.py::test_my_test_case_3 --junitxml=junit/test-results.xml


## Pipelines setup

### Build

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest
strategy:
  matrix:
    Python310:
      python.version: '3.10'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '$(python.version)'
  displayName: 'Use Python $(python.version)'

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)'
    ArtifactName: 'drop'
    publishLocation: Container
  displayName: 'Publish Artifact'
```

### Release

```yaml
steps:
- task: VSTest@2
  displayName: 'Test run for Test plans'
  inputs:
    testSelector: testRun
    vsTestVersion: toolsInstaller
    runInParallel: false
    runTestsInIsolation: false
    codeCoverageEnabled: false
  continueOnError: true
  condition: false

```

```yaml
steps:
- task: UsePythonVersion@0
  displayName: 'Use Python 3.10.x'
  inputs:
    versionSpec: 3.10.x
```

```yaml
steps:
- bash: |
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   
  workingDirectory: '$(System.DefaultWorkingDirectory)/_deixei.sharp-testing/drop'
  displayName: 'pip install requirements'
```

```yaml
steps:
- bash: 'python tsharp/tsharp_runner.py --verbose vvv'
  workingDirectory: '$(System.DefaultWorkingDirectory)/_deixei.sharp-testing/drop'
  displayName: 'Run Test Cases'
  env:
    RUN_ID: $(test.RunId)
    DX_ADO_URL: https://dev.azure.com/deixeicom
    AZURE_DEVOPS_EXT_PAT: $(System.AccessToken)
    AZURE_DEVOPS_EXT_PROJECT: deixei
    AZURE_TENANT: $(AZURE_TENANT)
    AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
    AZURE_SECRET: $(AZURE_SECRET)
```