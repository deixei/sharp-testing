# This is autogenerated test suite file for sharp testing
import os
import pytest

@pytest.mark.test_id(27)
def test_my_test_case_2(ado_config):
	# wi: 27
	# tc: My test case description
	print("This is a test function")
	assert True


@pytest.mark.test_id(28)
def test_my_test_case_3(ado_config):
	# wi: 28
	# tc: My test case description
	print("This is a test function")
	print(f"test_print_name_3(name): {ado_config}")
	#print(f"test_print_name_2(name): {pytestconfig.getoption('name')}")
	assert True

