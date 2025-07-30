# test_headless_false.py

import asyncio
import os

from dotenv import load_dotenv

from ambientagi.services.agent_service import AmbientAgentService

load_dotenv()


async def main():
    service = AmbientAgentService(
        api_key=os.getenv("OPENAI_API_KEY")
    )  # your OpenAI key

    agent = service.create_agent(
        agent_name="VisibleAgent",
        wallet_address="0xVISIBLE",
        description="Open Google and report the title",
    )

    browser_agent = service.create_browser_agent(agent_id=agent["agent_id"])

    result = await browser_agent.run_task(
        model="gpt-4o",
        task="Go to https://google.com and report the page title.",
    )

    print("\n[VISIBLE RESULT]:", result.final_result())


if __name__ == "__main__":
    asyncio.run(main())
