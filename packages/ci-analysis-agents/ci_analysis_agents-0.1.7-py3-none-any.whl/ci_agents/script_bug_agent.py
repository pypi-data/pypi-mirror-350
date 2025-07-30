from agents import RunContextWrapper, Agent, function_tool
import subprocess

from ci_agents.factory import AgentFactory
from ci_agents.types import AnalysisContext, ATScriptAIResponse
from hooks.agent_hook_log import global_log_hook
from agents.mcp import MCPServer, MCPServerSse


@function_tool
def execute_terminal_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"execute terminal command failed: {e.stderr}"


def script_agent_instructions(context: RunContextWrapper[AnalysisContext], agent: Agent[AnalysisContext]) -> str:
    # failure_log = context.context.failure_log
    # failed_thread_log = context.context.failed_thread_log
    # • {failure_log} → Key error stack trace from the automation framework
    # • {failed_thread_log} → Detailed log of the failure event
    test_id = context.context.test_id
    system_prompt = f"""
    #Role:
    You are a mobile E2E automation expert specializing in analyzing CI automation failure reports. 
    Your expertise lies in diagnosing whether a failure is caused by AT script issue.AT script issue includes expired locators, scripts bugs, apps UI/Bugs/Flow introduced.
    #Data Provided:
    You can call mcp server by test_id {test_id} to retrieve the failed case metadata.
    #Rule
    All download can use curl command to download and upload to LLM
    #Steps:
     1.Load the failed test case metadata using testId={test_id}.
     2.If the cause does not obviously appear to be an environment issue like api exception, load the metadata for the last successful run of the same test.
     3.Retrieve the latest successful screenshots for the same test case.Compare UI elements, states, and transitions between the failed and successful runs, and highlight any differences in the screenshots
     4.Analyze the root cause using all available data:
     If the UI appears correct in screenshots, the PageSource is normal, but the test still fails,
     If the UI is incomplete, screenshots show device or network issues, or the PageSource is empty, malformed, or missing critical components,Classify the issue as a Lab Environment Issue.
     If the UI appears visually incorrect or frozen, or the PageSource indicates an unexpected app state or logic error (such as the wrong page being loaded),Classify the issue as an App Bug.
    """

    requirement = """
    #Output Requirements:
    ##Case 1: If the failure is caused by AT Script, return with json format:
    {
       "root_cause_insight": "Clearly explain the exact root cause of the failure.",
       "action_insight": {
          "code_line": "Extracted code line from the logs that caused the failure.",
        },
       "failed_by_at_script": true
    }
    Notes:
    • "rootCauseInsight" should clearly explain the reason for the failure based on log analysis.
    • "actionSuggestion" must include actual extracted log details. If no relevant logs are found, leave the field as an empty string ("") without generating fake data.
    • Ensure the response is strictly in JSON format.

    ##Case 2: If the failure is NOT caused by an at script, return:
    {
      "root_cause_insight": "Explain why the failure is not due to an environment issue. Provide your thought process and references.",
      "failed_by_at_script": false
    }
    """
    please_note = """
      #Important:
      • You MUST finish your analysis and produce a complete JSON response within 3 step.
      • Do NOT ask follow-up questions or request additional clarification.
      """
    return system_prompt + requirement


class ScriptBugAgentFactory(AgentFactory):

    def __init__(self, mcp: MCPServer = None):
        super().__init__()
        self.mcp = mcp

    def get_agent(self) -> Agent[AnalysisContext]:
        if not self.mcp:
            raise ValueError("MCPServer must be provided to ScriptBugAgentFactory")
            
        script_analyse_agent = Agent[AnalysisContext](
            name="script_analyse_agent",
            model="gpt-4o",
            instructions=script_agent_instructions,
            mcp_servers=[self.mcp],
            output_type=ATScriptAIResponse,
            hooks=global_log_hook,
            tools=[execute_terminal_command]
        )
        return script_analyse_agent
