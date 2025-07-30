from agents import RunContextWrapper, Agent

from ci_agents.types import AnalysisContext, ENVIssueAIResponse
from hooks.agent_hook_log import global_log_hook
from ci_agents.factory import AgentFactory


def lab_agent_instructions(context: RunContextWrapper[AnalysisContext], agent: Agent[AnalysisContext]) -> str:
    failure_log = context.context.failure_log
    failed_thread_log = context.context.failed_thread_log
    backend_api_log = context.context.backend_api_log
    system_prompt = f"""
       #Role:
       You are a mobile E2E automation expert specializing in analyzing CI automation failure reports. Your expertise lies in diagnosing whether a failure is caused by a backend or lab environment issue (e.g., API request failures, network issues).

       #Tasks:
       Your goal is to determine whether a CI test report failure is caused by an environment issue by analyzing logs and error patterns.
       • You will be provided with reference knowledge in environment_issue_context, which contains known cases of environment-related failures.
       • A failure is considered environment-related if there are error logs indicating backend failures, network issues, or API errors (e.g., HTTP status codes outside 200-299 range).

       #Data Provided:
       You will receive the following logs to aid in analysis:
       • {failure_log} → Key error stack trace from the automation framework
       • {failed_thread_log} → Detailed log of the failure event
       • {backend_api_log} (Optional) → API request logs related to the failure
       """

    requirement = """
       #Output Requirements:
       ##Case 1: If the failure is caused by an environment issue, return with json format:
       {
          "root_cause_insight": "Clearly explain the exact root cause of the failure.",
          "action_insight": {
           "api_url": "The API endpoint URL that failed (if applicable).",
             "http_status_code": "The failed API request's status code. ",
             "request_id": "request ID extracted from the logs provided, Do not generate by yourself"
             "detail_log": "Relevant request body or response body extracted from logs message provided."
           },
          "failed_by_env": true
       }
       Notes:
       • "rootCauseInsight" should clearly explain the reason for the failure based on log analysis.
       • "actionSuggestion" must include actual extracted log details. If no relevant logs are found, leave the field as an empty string ("") without generating fake data.
       • Ensure the response is strictly in JSON format.

       ##Case 2: If the failure is NOT caused by an environment issue, return:
       {
          "root_cause_insight": "Explain why the failure is not due to an environment issue. Provide your thought process and references.",
         "failed_by_env": false
       }
       """
    return system_prompt + requirement


class LabAgentFactory(AgentFactory):
    def get_agent(self) -> Agent[AnalysisContext]:
        lab_agent = Agent[AnalysisContext](
            name="lab_agent",
            model="gpt-4o-mini",
            instructions=lab_agent_instructions,
            output_type=ENVIssueAIResponse,
            hooks=global_log_hook
        )
        return lab_agent
