from typing import Any, Dict, Optional

from agents import Agent, Runner, function_tool

from ambientagi.config.logger import setup_logger

logger = setup_logger("Ambientlibrary.openaiwrapper")


class OpenAIAgentWrapper:
    def __init__(self, api_key: str, scheduler=None, ambient_service=None):
        """
        :param api_key: The user's OpenAI API key, if you need to set openai.api_key or store it.
        :param scheduler: Optional APScheduler (or similar) instance for scheduling.
        :param ambient_service: Reference to the AmbientAgentService for usage increments.
        """
        self.agents: Dict[str, Any] = {}
        self.scheduler = scheduler
        self.ambient_service = ambient_service
        self.api_key: str = api_key

    def create_agent(self, name: str, instructions: str) -> Agent:
        agent = Agent(name=name, instructions=instructions)
        self.agents[name] = agent
        return agent

    def run_agent(
        self, agent_name: str, input_text: str, agent_id: Optional[str] = None
    ) -> str:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")

        result = Runner.run_sync(agent, input_text)
        final_output = result.final_output

        if agent_id and self.ambient_service:
            logger.info(f"Auto-incrementing usage for agent_id={agent_id}.")
            self.ambient_service._increment_usage(agent_id)

        return final_output

    async def run_agent_async(
        self, agent_name: str, input_text: str, agent_id: Optional[str] = None
    ) -> str:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")

        result_obj = await Runner.run(agent, input_text)
        final_output = result_obj.final_output

        if agent_id and self.ambient_service:
            logger.info(f"Auto-incrementing usage for agent_id={agent_id} (async).")
            self.ambient_service._increment_usage(agent_id)

        return final_output

    def add_function_tool(self, agent_name: str, func):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")

        decorated_func = function_tool(func)
        agent.tools.append(decorated_func)

    def schedule_agent(self, agent_name: str, input_text: str, interval: int):
        if self.scheduler is None:
            raise ValueError("Scheduler is not set.")

        def run_task():
            output = self.run_agent(agent_name, input_text)
            logger.info(f"[Scheduled Output from '{agent_name}']: {output}")

        self.scheduler.add_job(
            job_id=f"openai_agent_{agent_name}",
            func=run_task,
            trigger="interval",
            seconds=interval,
        )
        logger.info(f"Agent '{agent_name}' scheduled every {interval} seconds.")
