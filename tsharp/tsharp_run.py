import os
import requests

class MainRun:

    def __init__(self):
        self.run_id = os.environ.get("RUN_ID")
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
        self.project = "deixei"
    
    def execute(self):
        print(f"This is a test run {self.run_id}")
        print(f"This is the url {self.url}")
        print(f"This is the pat {self.pat}")

        run = self.get_run_id()
        print(run)

    def get_run_id(self):
        url = f"{self.url}/{self.project}/_apis/test/runs/{self.run_id}?includeDetails=True&api-version=7.1-preview.3"

        response = requests.get(url, auth=('PAT', self.pat))
        data = response.json()

        return data

if __name__ == "__main__":
    main = MainRun()
    main.execute()