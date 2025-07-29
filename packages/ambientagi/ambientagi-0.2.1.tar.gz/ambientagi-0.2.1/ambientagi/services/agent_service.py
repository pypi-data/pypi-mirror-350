from typing import Any, Dict, Optional, Set

import requests
from eth_account import Account

from ambientagi.config.logger import setup_logger
from ambientagi.providers.email_provider import EmailProvider
from ambientagi.providers.telegram_provider import TelegramProvider
from ambientagi.providers.twitter_provider import TwitterService
from ambientagi.services.ambient_blockchain import BlockchainService
from ambientagi.services.ambient_browser import BrowserAgent
from ambientagi.services.openai_agent_wrapper import OpenAIAgentWrapper
from ambientagi.services.scheduler import AgentScheduler
from ambientagi.services.webui_agent import WebUIAgent
from ambientagi.utils.http_client import HttpClient

logger = setup_logger("Ambientlibrary.openaiwrapper")


class AmbientAgentService:
    """
    A single central service for:
      - Creating and updating agents via FastAPI.
      - Running local OpenAI-based agents with usage tracking.
    """

    DEFAULT_BASE_URL = "https://api-gpt.ambientagi.ai/api/v1/agent-usage"
    BURN_USD = 10.0
    LOCAL_CHAIN_API = "https://api-eth.ambientagi.ai"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        scheduler: Optional[AgentScheduler] = None,
    ):
        """
        Initialize the AmbientAgentService with a centralized HTTP client
        and an internal OpenAIAgentWrapper for local agent handling.
        """
        default_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.client = HttpClient(
            base_url=base_url or self.DEFAULT_BASE_URL,
            default_headers=default_headers,
        )
        self.scheduler = scheduler

        # Our internal wrapper for local agent logic
        self.openai_wrapper = OpenAIAgentWrapper(
            api_key=api_key, scheduler=self.scheduler, ambient_service=self
        )

    @staticmethod
    def _wallet_from_key(private_key: str) -> str:
        try:
            acct = Account.from_key(private_key)
            return acct.address  # already EIP-55 checksum
        except Exception as exc:
            raise ValueError(f"Invalid private key: {exc}") from exc

    # ------------------------------------------------------------------
    #  FastAPI-based Agent Methods (Creation, Retrieval, Updating, etc.)
    # ------------------------------------------------------------------

    def create_agent(
        self,
        agent_name: str,
        private_key: str,  # ← was wallet_address
        description: str = "",
        coin_address: Optional[str] = None,
        twitter_handle: Optional[str] = None,
        twitter_id: Optional[str] = None,
        status: str = "active",
    ) -> Dict[str, Any]:
        """
        Create an agent **without ever storing** the user's private key.

        Flow:
        1. POST /burnAmbi  on the local Node API (hard-coded $2 burn).
        2. Reject if that wallet already has an agent with the same name
        3. On success → extract 'wallet' from JSON and POST /agent/create.
        4. On failure → bubble the error payload straight back.
        """
        # --- 1) derive wallet by burning $2 of AMBI --------------------
        wallet_address = self._wallet_from_key(private_key)
        logger.info("Derived wallet %s for agent '%s'", wallet_address, agent_name)

        # 2) duplicate check (assumes GET /agent/exists?wallet&name=)

        try:
            # list[AgentRecordResponse] or [] if none found
            records = self.client.get(f"/agent/wallet/{wallet_address}")
        except Exception as exc:
            logger.error("Wallet-lookup call failed: %s", exc, exc_info=True)
            return {"success": False, "error": "Wallet-lookup endpoint failed"}

        # Pick out records that clash with this agent_name
        dup_records = [rec for rec in records if rec["agent_name"] == agent_name]

        if dup_records:
            logger.warning(
                "Duplicate agent attempt: wallet=%s name=%s", wallet_address, agent_name
            )
            return {
                "success": False,
                "duplicate": True,
                "message": "This wallet already has an agent with that name.",
                "agent_records": dup_records,  # send the full list back
            }
        # 3) burn $2 AMBI to verify ownership
        burn_payload = {"privateKey": private_key, "usd": self.BURN_USD}
        try:
            burn_resp = requests.post(
                f"{self.LOCAL_CHAIN_API}/burnAmbi", json=burn_payload, timeout=60
            ).json()
        except Exception as exc:
            logger.error("Burn API unreachable: %s", exc, exc_info=True)
            return {"success": False, "error": str(exc)}

        if not burn_resp.get("success"):
            return burn_resp  # bubble readable error

        # 4) create agent in DB
        payload = {
            "agent_name": agent_name,
            "wallet_address": wallet_address,
            "description": description,
            "coin_address": coin_address,
            "twitter_handle": twitter_handle,
            "twitter_id": twitter_id,
            "status": status,
        }
        agent = self.client.post("/agent/create", json=payload)

        # 5) attach burn proof for transparency
        agent["burn_tx"] = {
            "txHash": burn_resp["txHash"],
            "amountUSD": burn_resp["amountUSD"],
            "amountTokens": burn_resp["amountTokens"],
        }
        return agent

    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """
        GET /agent/{agent_id}
        """
        agent_id = agent_id.strip()
        logger.info(f"Fetching agent info for agent_id={agent_id}")
        return self.client.get(f"/agent/{agent_id}")

    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        PATCH /agent/{agent_id}/update
        """
        agent_id = agent_id.strip()
        logger.info(f"Updating agent_id={agent_id} with {updates}")
        return self.client.patch(f"/agent/{agent_id}/update", json=updates)

    def _increment_usage(self, agent_id: str) -> Dict[str, Any]:
        """
        Internal method that increments usage_count in the DB via POST /agent/{agent_id}/increment.
        """
        agent_id = agent_id.strip()
        logger.info(f"Incrementing usage for agent_id={agent_id}")
        return self.client.post(f"/agent/{agent_id}/increment")

    # ------------------------------------------------------------------
    #  Methods Exposing OpenAI Agent Logic (All in One Place)
    # ------------------------------------------------------------------

    def create_openai_agent(self, local_agent_name: str, instructions: str):
        """
        Creates a local agent (NOT the same as your DB agent). This is for local LLM usage.
        """
        return self.openai_wrapper.create_agent(local_agent_name, instructions)

    def run_openai_agent(self, local_agent_name: str, input_text: str, agent_id: str):
        """
        Runs a local openai-based agent. If agent_id is supplied, usage increments.
        """
        return self.openai_wrapper.run_agent(
            local_agent_name, input_text, agent_id=agent_id
        )

    async def run_openai_agent_async(
        self, local_agent_name: str, input_text: str, agent_id: str
    ):
        """
        Runs a local openai-based agent asynchronously.
        """
        return await self.openai_wrapper.run_agent_async(
            local_agent_name, input_text, agent_id=agent_id
        )

    # ------------------------------------------------------------------
    #  Additional Service Methods (Email, Telegram, Blockchain, etc.)
    # ------------------------------------------------------------------

    def schedule_agent(self, agent_id: str, func, interval: int, **kwargs):
        """
        Generic scheduling for any arbitrary function (non-OpenAI usage).
        """
        if self.scheduler is None:
            raise ValueError("Scheduler is not set.")

        job_id = f"agent_{agent_id}"
        logger.info(f"Scheduling agent_id={agent_id} every {interval} seconds.")
        self.scheduler.add_job(
            job_id=job_id, func=func, trigger="interval", seconds=interval, **kwargs
        )

    def create_browser_agent(
        self,
        agent_id: str,
        browser_config: Optional[dict] = None,
        context_config: Optional[dict] = None,
    ):
        """
        Creates a BrowserAgent for automating complex browser interactions using Playwright,
        including dynamic content extraction, form submissions, single-page application navigation,
        and real-time data handling.

        This agent is built on top of Playwright, providing powerful support for headless and headful browsing,
        advanced context management, and JavaScript execution, making it ideal for scraping modern, dynamic websites.

        Parameters:
        - agent_id (str): A unique identifier for the agent, used to link the BrowserAgent instance to a specific agent configuration.
        - browser_config (Optional[dict]): An optional dictionary containing settings for the Playwright browser instance, such as:
            - headless (bool): Whether to run the browser in headless mode (default is True).
            - user_data_path (str): Path to a user data directory to maintain browser state.
            - extensions (list[str]): List of paths to browser extensions to load.
            - devtools (bool): Whether to enable developer tools (default is False).
            - js_enabled (bool): Whether to enable JavaScript execution (default is True).
            - network_interception (bool): Whether to enable network request interception (default is False).
        - context_config (Optional[dict]): An optional dictionary for context-specific settings, such as:
            - viewport_size (tuple[int, int]): Width and height of the browser window.
            - user_agent (str): Custom user agent string for the browser.
            - tracing (bool): Whether to enable tracing for performance analysis (default is False).
            - cookies (list[dict]): Preload cookies for the browser context.
            - permissions (list[str]): List of permissions to grant to the browser context (e.g., 'geolocation', 'notifications').
            - wait_for_load_state (str): Specifies the load state to wait for (e.g., 'domcontentloaded', 'networkidle') for SPA support.
            - wait_for_selector (str): CSS selector to wait for, ensuring dynamic content is loaded before extracting data.
            - timeout (int): Maximum wait time for elements to load (default is 30 seconds).
            - ignore_https_errors (bool): Whether to ignore HTTPS errors (default is False).

        Returns:
        - BrowserAgent: An instance of the BrowserAgent class, pre-configured with the specified agent, browser, and context settings,
        including support for dynamic content extraction via Playwright.
        """
        return BrowserAgent(
            agent_id,
            ambient_service=self,
            api_key=self.openai_wrapper.api_key,
            browser_config=browser_config,
            context_config=context_config,
        )

    def add_blockchain(self, agent_id: str):
        """
        Creates a BlockchainService for the specified agent, providing support for Ethereum and Solana coin creation,
        smart contract interactions, and on-chain data management.

        This function initializes a BlockchainService, enabling the agent to interact with decentralized networks like Ethereum and Solana,
        including creating new tokens, managing wallets, and performing on-chain transactions.

        Parameters:
        - agent_id (str): The ID of the agent to attach to the blockchain service. This ID should correspond to a valid agent with a
                        configured wallet address and blockchain settings.

        Returns:
        - BlockchainService: An instance of the BlockchainService class, pre-configured with the agent's blockchain settings,
        including support for Ethereum (ERC-20, ERC-721) and Solana (SPL tokens) coin creation.

        Capabilities:
        - Token Creation:
            - Ethereum (ERC-20, ERC-721)
            - Solana (SPL Tokens)
        - Smart Contract Deployment
        - On-Chain Data Management
        - Transaction Signing and Gas Optimization
        - Wallet Management and Balance Tracking
        - Decentralized Application (DApp) Integration
        - Cross-Chain Interactions

        """
        logger.info(f"Creating BlockchainService for agent_id={agent_id}")
        agent = self.get_agent_info(agent_id)
        return BlockchainService(agent)

    def create_twitter_agent(self, agent_id: str):
        """
        Creates a TwitterService for the specified agent, allowing automated interactions on Twitter (X),
        including posting tweets, replying, liking, retweeting, and direct messaging.

        This function initializes a TwitterService instance, enabling the agent to manage a Twitter account programmatically,
        making it ideal for social media bots, marketing campaigns, and personalized content distribution.

        Parameters:
        - agent_id (str): The ID of the agent to attach to the Twitter service. This ID should correspond to a valid agent
                        with the required API keys and Twitter account credentials.

        Returns:
        - TwitterService: An instance of the TwitterService class, pre-configured with the agent's Twitter API credentials,
        including support for posting, replying, liking, retweeting, and user interactions.

        Capabilities:
        - Post and Schedule Tweets
        - Reply to Tweets
        - Like and Retweet Posts
        - Follow and Unfollow Users
        - Send Direct Messages
        - Retrieve Mentions and Notifications
        - Perform Sentiment Analysis on Tweets
        - Hashtag Tracking and Trend Analysis


        Notes:
        - Ensure the agent is configured with valid Twitter API keys and permissions.
        - Consider rate limits and API usage costs when automating large volumes of activity.
        """
        logger.info(f"Creating TwitterService for agent_id={agent_id}")
        agent = self.get_agent_info(agent_id)
        return TwitterService(agent)

    def add_webui_agent(
        self,
        agent_id: str,
        config: Optional[Dict[str, Any]] = None,
        theme="Ocean",
        ip="127.0.0.1",
        port=7788,
    ) -> WebUIAgent:
        """
        Creates and returns a WebUIAgent for controlling a browser-based AI interface, enabling
        real-time interactions, task management, and data visualization through a customizable
        web dashboard.

        This function initializes a WebUIAgent, providing a graphical interface for managing the agent's
        activities, interactions, and performance. It supports various themes, customizable configurations,
        and local or remote hosting.

        Parameters:
        - agent_id (str): The unique identifier for the agent to attach to the Web UI.
        - config (Optional[Dict[str, Any]]): An optional dictionary for customizing the Web UI settings.
        - theme (str): The visual theme for the Web UI (default is 'Ocean').
        - ip (str): The IP address to bind the Web UI server to (default is '127.0.0.1' for local hosting).
        - port (int): The port number for the Web UI server (default is 7788).

        Returns:
        - WebUIAgent: An instance of the WebUIAgent class, pre-configured with the specified agent ID and UI settings.

        Capabilities:
        - Real-Time Data Visualization
        - Interactive Task Management
        - API Integration and Monitoring
        - Customizable UI Themes
        - Secure Local and Remote Hosting
        - User Authentication and Access Control

        Example Usage:
        ```python
        webui_agent = add_webui_agent(agent_id="1234", theme="Dark", ip="0.0.0.0", port=8080)
        webui_agent.start_server()
        webui_agent.display_dashboard()
        ```

        Notes:
        - Ensure the default configuration is properly loaded if no custom settings are provided.
        - Use secure IP and port settings for production environments.
        """
        logger.info(f"Creating WebUIAgent for agent_id={agent_id}")

        if config is None:
            from ambientagi.utils.webui.utils.default_config_settings import (
                default_config,
            )

            config = default_config()

        config["agent_id"] = agent_id
        return WebUIAgent(config=config, theme=theme, ip=ip, port=port)

    def create_email_agent(
        self,
        agent_id: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ):
        """
        Creates an EmailProvider for the specified agent, enabling automated email sending,
        notifications, and message management using customizable SMTP settings.

        Parameters:
        - agent_id (str): The ID of the agent to attach to the email service.
        - smtp_server (str): The SMTP server address (default is 'smtp.gmail.com').
        - smtp_port (int): The port number for the SMTP server (default is 587 for TLS).
        - username (Optional[str]): The username or email address for authentication.
        - password (Optional[str]): The password for authentication.
        - use_tls (bool): Whether to use TLS for secure communication (default is True).

        Returns:
        - EmailProvider: An instance of the EmailProvider class, pre-configured with the specified SMTP settings.

        Capabilities:
        - Send Automated Emails
        - Bulk Email Campaigns
        - Personalized Email Templates
        - SMTP Configuration and Authentication
        - HTML and Plain Text Support
        - Attachment Handling
        - Email Tracking and Analytics
        - Auto-Responder and Drip Campaigns
        - Integration with Other Services (e.g., CRM, Marketing Platforms)
        Notes:
        - Ensure the agent is configured with valid SMTP credentials and permissions.
        - If using Gmail, consider enabling "Less secure app access" or using an App Password for 2FA accounts.
        - For other email providers, adjust the SMTP server and port settings accordingly.
        - For security reasons, avoid hardcoding sensitive credentials in your code.

        """
        agent_info = self.get_agent_info(agent_id)
        return EmailProvider(
            agent_info=agent_info,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            username=username,
            password=password,
            use_tls=use_tls,
        )

    def create_telegram_agent(
        self,
        agent_id: str,
        bot_token: str,
        mentions: Optional[Set[str]] = None,
    ) -> TelegramProvider:
        """
        Creates a TelegramProvider for the specified agent, allowing automated message handling,
        group management, and real-time bot interactions on the Telegram platform.

        Parameters:
        - agent_id (str): The ID of the agent to attach to the Telegram service.
        - bot_token (str): The bot token for authenticating with the Telegram API.
        - mentions (Optional[Set[str]]): An optional set of usernames or keywords to filter incoming messages.

        Returns:
        - TelegramProvider: An instance of the TelegramProvider class, pre-configured with the bot's authentication and mention filters.

        Capabilities:
        - Send and Receive Messages
        - Group and Channel Management
        - Message Filtering and Moderation
        - Bot Command Handling
        - User Mentions and Keyword Triggers
        - Media and File Sharing
        - Inline Query Handling
        - Polls and Surveys
        - Webhook and Long Polling Support
        Notes:
        - Ensure the agent is configured with a valid bot token from BotFather.
        - Consider rate limits and API usage costs when automating large volumes of activity.
        - For security reasons, avoid hardcoding sensitive credentials in your code.
        - For more information on creating and managing Telegram bots, refer to the official Telegram Bot API documentation.
        - https://core.telegram.org/bots/api
        - https://core.telegram.org/bots#botfather
        - https://core.telegram.org/bots/api#markdownv2-style
        - https://core.telegram.org/bots/api#html-style
        - https://core.telegram.org/bots/api#markdown-style
        - https://core.telegram.org/bots/api#sendmessage
        """
        agent_info = self.get_agent_info(agent_id)
        return TelegramProvider(
            agent_info=agent_info, bot_token=bot_token, mentions=mentions
        )
