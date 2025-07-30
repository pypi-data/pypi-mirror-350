from typing import Any, Dict, Optional

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from ambientagi.config.logger import setup_logger

logger = setup_logger("Ambientlibrary.browserwrapper")


class BrowserAgent:
    def __init__(
        self,
        agent_id: str,
        api_key: Optional[str] = None,
        ambient_service: Any = None,
        browser_config: Optional[Dict[str, Any]] = None,
        context_config: Optional[Dict[str, Any]] = None,
    ):

        self.agent_id = agent_id

        self.api_key = api_key  # ✅ store the passed-in user key
        self.ambient_service = ambient_service

        self.browser_config = BrowserConfig(**(browser_config or {}))
        self.context_config = BrowserContextConfig(**(context_config or {}))
        self.browser_config.new_context_config = self.context_config

    async def run_task(self, task: Optional[str] = None, model: str = "gpt-4o"):
        """
        Run the specified browser task using the configured agent and browser settings
        Run the task using the browser agent.
        :param task: The task to run. If None, uses the agent's default task.
        :param model: The model to use for the agent. Default is "gpt-4o".
        :return: The result of the task.
        """
        task = task

        browser = Browser(config=self.browser_config)

        agent = Agent(
            task=task,
            llm=ChatOpenAI(
                model=model,
                api_key=SecretStr(self.api_key) if self.api_key else None,
            ),
            browser=browser,
            browser_context=await browser.new_context(config=self.context_config),
        )
        result = await agent.run()

        # Auto-increment usage if service and agent_id are provided
        if self.agent_id and self.ambient_service:
            logger.info(
                f"Auto-incrementing browser usage for agent_id={self.agent_id}."
            )
            try:
                self.ambient_service._increment_usage(self.agent_id)
            except Exception:
                logger.error("Failed to auto-increment usage")

        return result
