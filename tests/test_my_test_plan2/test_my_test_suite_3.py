# This is autogenerated test suite file for sharp testing
import os
import pytest
from pytestsharp import PyTestSharp

@pytest.mark.test_id(29)
def test_my_test_case_5(ado_config, test_run_id, test_result_id, ado_url, ado_pat, ado_project, print_verbose, azure_tenant, azure_client_id, azure_secret):
	"""
	My test case description
	Details:{'configuration': {'name': 'my_config'}, 'description': 'My test case description', 'id': 29, 'name': 'my_test_case_5'}

	Args:
		ado_config: The ADO configuration.
		test_run_id: The ID of the test run.
		test_result_id: The ID of the test result.
		ado_url: The ADO URL.
		ado_pat: The ADO PAT.
		ado_project: The ADO Project.
		print_verbose: The verbosity level.
		azure_tenant: The Azure Tenant.
		azure_client_id: The Azure Client ID.
		azure_secret: The Azure Secret.

	Returns:
		None
	"""
	work_item_id=29
	test_case_description="My test case description"
	sharp = PyTestSharp(ado_config, test_run_id, test_result_id, work_item_id, test_case_description, ado_url, ado_pat, ado_project, print_verbose, azure_tenant, azure_client_id, azure_secret)

	sharp.show_inputs()

	assert True


@pytest.mark.test_id(30)
def test_my_test_case_4(ado_config, test_run_id, test_result_id, ado_url, ado_pat, ado_project, print_verbose, azure_tenant, azure_client_id, azure_secret):
	"""
	My test case description
	Details:{'configuration': {'name': 'my_config'}, 'description': 'My test case description', 'id': 30, 'name': 'my_test_case_4'}

	Args:
		ado_config: The ADO configuration.
		test_run_id: The ID of the test run.
		test_result_id: The ID of the test result.
		ado_url: The ADO URL.
		ado_pat: The ADO PAT.
		ado_project: The ADO Project.
		print_verbose: The verbosity level.
		azure_tenant: The Azure Tenant.
		azure_client_id: The Azure Client ID.
		azure_secret: The Azure Secret.

	Returns:
		None
	"""
	work_item_id=30
	test_case_description="My test case description"
	sharp = PyTestSharp(ado_config, test_run_id, test_result_id, work_item_id, test_case_description, ado_url, ado_pat, ado_project, print_verbose, azure_tenant, azure_client_id, azure_secret)

	sharp.show_inputs()

	
	for item in sharp.azure_sharp.query_management_groups():
		print(item)

	assert True

