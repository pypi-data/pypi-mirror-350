from agents import RunContextWrapper, Agent, function_tool

from ci_agents.factory import AgentFactory
from ci_agents.types import AnalysisContext, InfraIssueAIResponse
from hooks.agent_hook_log import global_log_hook


def infra_agent_instructions(context: RunContextWrapper[AnalysisContext], agent: Agent[AnalysisContext]) -> str:
    failure_log = context.context.failure_log
    failed_thread_log = context.context.failed_thread_log
    device_log = context.context.device_log
    appium_log = context.context.appium_log
    system_prompt = f"""
    #Role:
    You are a mobile E2E automation expert specializing in analyzing CI automation failure reports. Your expertise lies in diagnosing whether a failure is caused by the infrastructure issues (e.g.device issue, driver issue, network issues).

    #Tasks:
    Your goal is to determine whether a CI test report failure is caused by infrastructure issue by analyzing logs
    • A failure is considered infrastructure-related if there are error logs indicating:
      - device_issue (unavailable, disconnected, etc.)
      - driver_issue (initialization failures, session problems, etc.)
        NOTE: Element location failures such as 'NoSuchElementException', 'AssertionError', or 'TimeoutException' while waiting for elements are typically NOT driver issues.
      - app_issue (installation failures, launch problems, etc.)
      - network_issue (connectivity problems with devices, etc.)

    #Data Provided:
    You will receive the following logs to aid in analysis:
    • {failure_log} → Key error stack trace from the automation framework
    • {failed_thread_log} → Detailed log of the failure event
    • {device_log} → Record all devices information(such as device_host, device_udid, device_record,case_report_info, case_running_detail) during the period for the test
    • {appium_log} (Optional) → appium logs related to the failure, or when other logs cannot identify which specific device encountered issues

    #Important Instructions:
    1. First, carefully analyze {device_log} to check if it contains multiple device information (e.g., multiple device_udid and device_host entries)
    2. If multiple devices are present, you MUST pay special attention to determine which device is experiencing issues
    3. If you cannot clearly identify the problematic device or the exact nature of the infrastructure issue from the logs provided, you MUST call the dynamic_fetch_appium_log() function,dynamic_fetch_appium_log() function should be called ONLY ONCE
    4. If you call dynamic_fetch_appium_log(), you will receive additional appium logs that should be analyzed alongside {device_log} to identify the correct device_udid and device_host
    5. After analyzing all logs, if you determine this is failed_by_infra=False, you MUST call fetch_failed_step_images() to gather more information about the actual failure. You can call this function ONLY ONCE.

    """
    requirement = """
    #Output Requirements:
    ##Case 1: If the failure is caused by an infrastructure issue, return with json format:
    {
       "root_cause_insight": "Clearly explain the exact root cause of the failure.",
       "action_insight": {
          "device_udid": "The UDID of the device that failed",
          "device_host": "The host where the device is connected",
          "detail_log": "Relevant log excerpts supporting the analysis",
          "error_type": "The type of infrastructure error,must be one of: device_issue, driver_issue, app_issue, or network_issue",
        },
       "failed_by_infra": true
    }
    Notes:
    • "rootCauseInsight" should clearly explain the reason for the failure based on log analysis.
    • "actionInsight" must include actual extracted information from logs.

    ##Case 2: If the failure is NOT caused by an infrastructure issue, return:
    {
       "root_cause_insight": "Explain why the failure is not due to an infrastructure issue.",
       "failed_by_infra": false
    }
    """
    return system_prompt + requirement


class InfraAgentFactory(AgentFactory):
    def get_agent(self) -> Agent[AnalysisContext]:
        dynamic_fetch_appium_log = self.create_dynamic_fetch_appium_log()
        fetch_failed_step_images = self.create_fetch_failed_step_images()

        infra_agent = Agent[AnalysisContext](
            name="infra_agent",
            model="gpt-4o-mini",
            instructions=infra_agent_instructions,
            output_type=InfraIssueAIResponse,
            hooks=global_log_hook,
            tools=[dynamic_fetch_appium_log, fetch_failed_step_images]
        )
        return infra_agent

    def create_dynamic_fetch_appium_log(self):
        @function_tool
        def dynamic_fetch_appium_log(context: RunContextWrapper[AnalysisContext]) -> str:
            """
            Fetches Appium logs related to the test ID.
            """
            print("dynamic_fetch_appium_log function called! Fetching appium logs...")
            beats_metadata = context.context.beats_metadata
            current_test_id = context.context.test_id
            if not current_test_id:
                return "Unable to get test ID."
            try:
                appium_log = beats_metadata.get_appium_error_log_data(current_test_id)
                return appium_log
            except Exception as e:
                return f"Error occurred while fetching Appium logs: {str(e)}"

        return dynamic_fetch_appium_log

    def create_fetch_failed_step_images(self):
        @function_tool
        def fetch_failed_step_images(context: RunContextWrapper[AnalysisContext]) -> str:
            """
            Fetches URLs to screenshots from the failed test step.
            """
            print("fetch_failed_step_images function called! Retrieving failed step screenshots...")

            beats_metadata = context.context.beats_metadata
            current_test_id = context.context.test_id
            if not current_test_id:
                return "Unable to get test ID."

            try:
                formatted_urls = ""
                failed_step = beats_metadata.case_meta_data(current_test_id)['failed_step']
                if not failed_step['current_step_image_file_urls']:
                    return "No screenshot images found for the failed step."
                image_urls = failed_step['current_step_image_file_urls']
                if image_urls:
                    formatted_urls = "\n".join([f"Screenshot URL: {url}" for url in image_urls])

                return formatted_urls

            except Exception as e:
                return f"Error occurred while fetching failed step images: {str(e)}"

        return fetch_failed_step_images
