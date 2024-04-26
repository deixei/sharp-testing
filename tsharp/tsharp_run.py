import os

class MainRun:

    def __init__(self):
        self.run_id = os.environ.get("RUN_ID")
        self.url = os.environ.get("DX_ADO_URL")
        self.pat = os.environ.get("AZURE_DEVOPS_EXT_PAT")
    
    def execute(self):
        print(f"This is a test run {self.run_id}")
        print(f"This is the url {self.url}")
        print(f"This is the pat {self.pat}")

if __name__ == "__main__":
    main = MainRun()
    main.execute()