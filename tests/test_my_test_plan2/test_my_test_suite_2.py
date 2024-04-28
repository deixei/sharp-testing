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
	
	for config_item in ado_config:
		name = config_item["name"]
		value = config_item["value"]

		print(f"{name}: {value}")

		if name == "my_var":
			assert value == "my_value"

		if name == "my_var2":
			assert value == "my_value3"


		assert value != "Windows 10"
	

