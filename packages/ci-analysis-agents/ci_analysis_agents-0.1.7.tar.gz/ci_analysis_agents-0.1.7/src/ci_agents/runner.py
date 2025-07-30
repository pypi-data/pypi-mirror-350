from agents import Runner, ItemHelpers
from ci_agents.hub_agent import HubAgentFactory
from ci_agents.lab_agent import LabAgentFactory
from ci_agents.types import AnalysisContext, AIResponse, dispatch_ai_response
from hooks.agent_hook_log import global_log_hook
from ci_agents.log_config import configure_root_logger
from langfuse.langfuse_decorate import langfuse_task

configure_root_logger()


@langfuse_task
async def analyze_failure(analysis_context: AnalysisContext) -> AIResponse:
    """
    Analyze the failure logs and return the analysis result.
    """
    hub_agent_factory = await HubAgentFactory.create()
    hub_agent = hub_agent_factory.get_agent()
    result = await Runner.run(
        starting_agent=hub_agent,
        input="Can you analyze the root cause of the CI failure with using the tools",
        context=analysis_context
    )
    print(global_log_hook.events.__sizeof__())
    print(global_log_hook.events)
    generic_response: AIResponse = result.final_output
    specific_response = dispatch_ai_response(generic_response, analysis_context)
    return specific_response


async def analyze_failure_parallel(analysis_context: AnalysisContext) -> AIResponse:
    # fixme: might be removed if the agent as tool performance is good.
    hub_agent_factory = await HubAgentFactory.create()

    hub_agent = hub_agent_factory.get_agent()
    lab_agent = LabAgentFactory().get_agent()
    lab_result = await Runner.run(
        starting_agent=lab_agent,
        input="Can you analyze if the root cause of the CI failure is caused by lab environment issue",
        context=analysis_context
    )

    result = await Runner.run(
        starting_agent=hub_agent,
        input=f"Can you analyze the root cause of the CI failure with the context and the result from lab agent {ItemHelpers.text_message_outputs(lab_result.new_items)}",
        context=analysis_context
    )

    print(global_log_hook.events.__sizeof__())
    print(global_log_hook.events)
    return result.final_output
