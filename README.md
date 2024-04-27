# Introduction 

Need a command to upload a test case id with a function

Need a command to create test suites; test Plans and Test cases;


## APIS
https://learn.microsoft.com/en-us/rest/api/azure/devops/test/configurations/create?view=azure-devops-rest-5.0&tabs=HTTP


# run

python3 tsharp/tsharp.py


# notes on testing stuff

pytest pytest-azurepipelines

pytest --doctest-modules --junitxml=junit/test-results.xml

pytest test_my_test_plan2/test_my_test_suite_2.py::test_my_test_case_3 --junitxml=junit/test-results.xml