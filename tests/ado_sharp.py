

# source: https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash
class ADOLog:
    @staticmethod
    def group(message):
        print(f"##[group]{message}")

    @staticmethod
    def warning(message):
        print(f"##[warning]{message}")

    @staticmethod
    def error(message):
        print(f"##[error]{message}")

    @staticmethod
    def section(message):
        print(f"##[section]{message}")

    @staticmethod
    def debug(message):
        print(f"##[debug]{message}")

    @staticmethod
    def command(message):
        print(f"##[command]{message}")

    @staticmethod
    def endgroup():
        print("##[endgroup]")

class ADOTask:
    @staticmethod
    def logissue(message, type:str="warning", sourcepath:str=None, linenumber:str=None, columnnumber:str=None, code:str=None):
        command = ""
        if sourcepath:
            command += f"sourcepath={sourcepath};"
        if linenumber:
            command += f"linenumber={linenumber};"
        if columnnumber:
            command += f"columnnumber={columnnumber};"
        if code:
            command += f"code={code};"

        if not type:
            raise ValueError("No type provided")

        if not message:
            raise ValueError("No message provided")

        print(f"##[task.logissue type={type};{command}]{message}")

    @staticmethod
    def logwarming(message, sourcepath:str=None, linenumber:str=None, columnnumber:str=None, code:str=None):
        ADOTask.logissue("warning", message, sourcepath, linenumber, columnnumber, code)

    @staticmethod
    def logerror(message, sourcepath:str=None, linenumber:str=None, columnnumber:str=None, code:str=None):
        ADOTask.logissue("error", message, sourcepath, linenumber, columnnumber, code)


    ##vso[task.setprogress value=$i;]Sample Progress Indicator
    @staticmethod
    def setprogress(value:int, message:str="Progress Indicator"):
        value_str = str(value)
        print(f"##[task.setprogress value={value_str};]{message}")

    @staticmethod
    def setvariable(variable:str, value:str, issecret:bool=False, isoutput:bool=False, isreadonly:bool=False):
        print(f"##[setvariable variable={variable};issecret={issecret};isoutput={isoutput};isreadonly={isreadonly}]{value}")

    ##vso[task.setsecret]value
    @staticmethod
    def setsecret(value:str):
        print(f"##[task.setsecret]{value}")

    @staticmethod
    def complete(result:str="Succeeded", message:str="Done"):
        ##vso[task.complete result=Failed;]"
        print(f"##[task.complete result={result}]{message}")

    @staticmethod
    def complete_succeeded(message:str="Done"):
        ADOTask.complete("Succeeded", message)

    @staticmethod
    def complete_failed(message:str="Failed"):
        ADOTask.complete("Failed", message)

    @staticmethod
    def complete_succeeded_with_issues(message:str="SucceededWithIssues"):
        ADOTask.complete("SucceededWithIssues", message)

    @staticmethod
    def setendpoint(id:str="000-0000-0000", field:str="url", key:str="https://www.deixei.com"):
        #id = service connection ID (Required)
        #field = field type, one of authParameter, dataParameter, or url (Required)
        #key = key (Required, unless field = url)
        if field == "url" and not key:
            raise ValueError("Key is required for field=url")
        if field == "url":
            print(f"##[task.setendpoint id={id};field={field}]{key}")
        else:
            print(f"##[task.setendpoint id={id};field={field};key={key}]")


    ##vso[task.addattachment type=myattachmenttype;name=myattachmentname;]c:\myattachment.txt
    ##vso[task.addattachment type=Distributedtask.Core.Summary;name=testsummaryname;]c:\testsummary.md
    @staticmethod
    def addattachment(type:str, name:str, path:str):
        print(f"##[task.addattachment type={type};name={name};]{path}")

    ##vso[task.uploadsummary]local file path
    @staticmethod
    def uploadsummary(path:str):
        print(f"##[task.uploadsummary]{path}")

    ##vso[task.uploadfile]local file path
    @staticmethod
    def uploadfile(path:str):
        print(f"##[task.uploadfile]{path}")

    ##vso[task.prependpath]local file path
    @staticmethod
    def prependpath(path:str):
        print(f"##[task.prependpath]{path}")
