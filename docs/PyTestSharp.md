# PyTest Sharp documentation

Purpose of this helper class is to give us a easy access to relevant test case information, as well to get the Azure Client credentials set from the pipeline.

This step in the release pipeline, passes some credential to the runner, that in turn passed to the PyTestSharp component.

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

Python section of the runner passing variable to pytest. This parameters are defined in the 'conftest.py' file as a fixture

```python
...
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
...                
```

All this makes it possible to inject the parameters into the test case function that will be executed.

```python
...
def test_am_1_track_asset_inventory_and_their_risks(ado_config, test_run_id, test_result_id, ado_url, ado_pat, ado_project, print_verbose, azure_tenant, azure_client_id, azure_secret):
...                
```

## Author

[Marcio Parente](https://github.com/deixei) from deixei.com

To understand the overall context of this project read this book: [ENTERPRISE SOFTWARE DELIVERY: A ROADMAP FOR THE FUTURE](https://www.amazon.de/-/en/Marcio-Parente/dp/B0CXTJZJ2X/)