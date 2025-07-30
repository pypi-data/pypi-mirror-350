from collections import defaultdict
from typing import Any

from agents import AgentHooks, RunContextWrapper, TContext, Agent, Tool
import logging

from ci_agents.types import save_response_to_context

logger = logging.getLogger(__name__)


class AgentHooksForLog(AgentHooks):
    def __init__(self):
        self.events: dict[str, int] = defaultdict(int)

    def reset(self):
        self.events.clear()

    async def on_start(self, context: RunContextWrapper[TContext], agent: Agent[TContext]) -> None:
        print(f"\nDebugging agent {agent.name} on_start")
        logger.info(f"Agent {agent.name} started with context: {context.context}")
        self.events["on_start"] += 1

    async def on_end(self, context: RunContextWrapper[TContext], agent: Agent[TContext], output: Any) -> None:
        print(f"Debugging agent {agent.name} on_end")
        save_response_to_context(context.context, output)
        self.events["on_end"] += 1

    async def on_handoff(self, context: RunContextWrapper[TContext], agent: Agent[TContext], source: Agent[TContext]) -> None:
        self.events["on_handoff"] += 1

    async def on_tool_start(self, context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool) -> None:
        print(f"Debugging agent {agent.name} on_tool_start")
        self.events["on_tool_start"] += 1

    async def on_tool_end(self, context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool, result: str) -> None:
        print(f"Debugging agent {agent.name} on_tool_end")
        if "fetch_appium_log" in tool.name.lower() and hasattr(context.context, "appium_log"):
            print(f"Adding appium_log to context...")
            context.context.appium_log = result
        self.events["on_tool_end"] += 1


global_log_hook = AgentHooksForLog()
