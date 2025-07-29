import argparse
import asyncio
import glob
import logging
import os

import gradio as gr  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Only load dotenv once, at the start
load_dotenv()

from browser_use.agent.service import Agent  # type: ignore
from browser_use.browser.browser import Browser, BrowserConfig  # type: ignore
from browser_use.browser.context import BrowserContextConfig  # type: ignore
from browser_use.browser.context import BrowserContextWindowSize

# Themes
from gradio.themes import Glass  # type: ignore
from gradio.themes import Base, Citrus, Default, Monochrome, Ocean, Origin, Soft
from langchain_ollama import ChatOllama  # type: ignore
from playwright.async_api import async_playwright  # type: ignore

from ambientagi.utils.webui.agent.custom_agent import CustomAgent
from ambientagi.utils.webui.agent.custom_prompts import (
    CustomAgentMessagePrompt,
    CustomSystemPrompt,
)
from ambientagi.utils.webui.browser.custom_browser import CustomBrowser
from ambientagi.utils.webui.browser.custom_context import (
    BrowserContextConfig as CustomContextConfig,
)
from ambientagi.utils.webui.browser.custom_context import CustomBrowserContext
from ambientagi.utils.webui.controller.custom_controller import CustomController
from ambientagi.utils.webui.utils import utils

# AmbientAGI / custom modules
from ambientagi.utils.webui.utils.agent_state import AgentState
from ambientagi.utils.webui.utils.default_config_settings import (
    default_config,
    load_config_from_file,
    save_config_to_file,
    save_current_config,
    update_ui_from_config,
)
from ambientagi.utils.webui.utils.utils import (
    capture_screenshot,
    get_latest_files,
    update_model_dropdown,
)

logger = logging.getLogger(__name__)

# Global state
_global_browser = None
_global_browser_context = None
_global_agent_state = AgentState()  # a single global agent state

# Map of theme names to actual Gradio theme objects
theme_map = {
    "Default": gr.themes.Default(),
    "Soft": gr.themes.Soft(),
    "Monochrome": gr.themes.Monochrome(),
    "Glass": gr.themes.Glass(),
    "Origin": gr.themes.Origin(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Base": gr.themes.Base(),
}


async def run_org_agent(
    llm,
    use_own_browser,
    keep_browser_open,
    headless,
    disable_security,
    window_w,
    window_h,
    save_recording_path,
    save_agent_history_path,
    save_trace_path,
    task,
    max_steps,
    use_vision,
    max_actions_per_step,
    tool_calling_method,
):
    """
    Runs the 'org' style agent using the global browser & context.
    """
    global _global_browser, _global_browser_context, _global_agent_state
    try:
        _global_agent_state.clear_stop()

        extra_chromium_args = [f"--window-size={window_w},{window_h}"]
        if use_own_browser:
            chrome_path = os.getenv("CHROME_PATH", None) or None
            chrome_user_data = os.getenv("CHROME_USER_DATA", None)
            if chrome_user_data:
                extra_chromium_args.append(f"--user-data-dir={chrome_user_data}")
        else:
            chrome_path = None

        # Create the global browser if needed
        if _global_browser is None:
            _global_browser = Browser(
                config=BrowserConfig(
                    headless=headless,
                    disable_security=disable_security,
                    chrome_instance_path=chrome_path,
                    extra_chromium_args=extra_chromium_args,
                )
            )

        # Create or reuse context
        if _global_browser_context is None:
            _global_browser_context = await _global_browser.new_context(
                config=BrowserContextConfig(
                    trace_path=save_trace_path or None,
                    save_recording_path=save_recording_path or None,
                    no_viewport=False,
                    browser_window_size=BrowserContextWindowSize(
                        width=window_w, height=window_h
                    ),
                )
            )

        agent = Agent(
            task=task,
            llm=llm,
            use_vision=use_vision,
            browser=_global_browser,
            browser_context=_global_browser_context,
            max_actions_per_step=max_actions_per_step,
            tool_calling_method=tool_calling_method,
        )

        history = await agent.run(max_steps=max_steps)

        # Save agent history
        history_file = os.path.join(save_agent_history_path, f"{agent.agent_id}.json")
        agent.save_history(history_file)

        final_result = history.final_result()
        errors = history.errors()
        model_actions = history.model_actions()
        model_thoughts = history.model_thoughts()

        trace_file = get_latest_files(save_trace_path)

        return (
            final_result,
            errors,
            model_actions,
            model_thoughts,
            trace_file.get(".zip"),
            history_file,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        errors = str(e) + "\n" + traceback.format_exc()
        return "", errors, "", "", None, None

    finally:
        if not keep_browser_open:
            # Close context
            if _global_browser_context:
                await _global_browser_context.close()
                _global_browser_context = None
            # Close browser
            if _global_browser:
                await _global_browser.close()
                _global_browser = None


async def run_custom_agent(
    llm,
    use_own_browser,
    keep_browser_open,
    headless,
    disable_security,
    window_w,
    window_h,
    save_recording_path,
    save_agent_history_path,
    save_trace_path,
    task,
    add_infos,
    max_steps,
    use_vision,
    max_actions_per_step,
    tool_calling_method,
):
    """
    Runs the 'custom' style agent using the global browser & context.
    """
    global _global_browser, _global_browser_context, _global_agent_state
    try:
        _global_agent_state.clear_stop()

        extra_chromium_args = [f"--window-size={window_w},{window_h}"]
        if use_own_browser:
            chrome_path = os.getenv("CHROME_PATH", None) or None
            chrome_user_data = os.getenv("CHROME_USER_DATA", None)
            if chrome_user_data:
                extra_chromium_args.append(f"--user-data-dir={chrome_user_data}")
        else:
            chrome_path = None

        controller = CustomController()

        if _global_browser is None:
            _global_browser = CustomBrowser(
                config=BrowserConfig(
                    headless=headless,
                    disable_security=disable_security,
                    chrome_instance_path=chrome_path,
                    extra_chromium_args=extra_chromium_args,
                )
            )

        if _global_browser_context is None:
            _global_browser_context = await _global_browser.new_context(
                config=BrowserContextConfig(
                    trace_path=save_trace_path or None,
                    save_recording_path=save_recording_path or None,
                    no_viewport=False,
                    browser_window_size=BrowserContextWindowSize(
                        width=window_w, height=window_h
                    ),
                )
            )

        agent = CustomAgent(
            task=task,
            add_infos=add_infos,
            use_vision=use_vision,
            llm=llm,
            browser=_global_browser,
            browser_context=_global_browser_context,
            controller=controller,
            system_prompt_class=CustomSystemPrompt,
            agent_prompt_class=CustomAgentMessagePrompt,
            max_actions_per_step=max_actions_per_step,
            agent_state=_global_agent_state,
            tool_calling_method=tool_calling_method,
        )

        history = await agent.run(max_steps=max_steps)

        history_file = os.path.join(save_agent_history_path, f"{agent.agent_id}.json")
        agent.save_history(history_file)

        final_result = history.final_result()
        errors = history.errors()
        model_actions = history.model_actions()
        model_thoughts = history.model_thoughts()

        trace_file = get_latest_files(save_trace_path)

        return (
            final_result,
            errors,
            model_actions,
            model_thoughts,
            trace_file.get(".zip"),
            history_file,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        errors = str(e) + "\n" + traceback.format_exc()
        return "", errors, "", "", None, None

    finally:
        if not keep_browser_open:
            if _global_browser_context:
                await _global_browser_context.close()
                _global_browser_context = None
            if _global_browser:
                await _global_browser.close()
                _global_browser = None


async def close_global_browser():
    """
    Closes global browser and context, if present.
    """
    global _global_browser, _global_browser_context
    if _global_browser_context:
        await _global_browser_context.close()
        _global_browser_context = None

    if _global_browser:
        await _global_browser.close()
        _global_browser = None


class WebUIAgent:
    """
    A wrapper class for the Gradio-based browser agent UI.
    """

    def __init__(self, config=None, theme="Ocean", ip="127.0.0.1", port=7788):
        self.config = config or default_config()
        self.theme = theme
        self.ip = ip
        self.port = port
        self.demo = None

    @staticmethod
    async def stop_agent():
        """
        Signal the agent to stop.
        """
        global _global_agent_state
        try:
            _global_agent_state.request_stop()
            message = "Stop requested - the agent will halt at the next safe point"
            logger.info(f"🛑 {message}")
            return (
                message,
                gr.update(value="Stopping...", interactive=False),  # stop_button
                gr.update(interactive=False),  # run_button
            )
        except Exception as e:
            error_msg = f"Error during stop: {str(e)}"
            logger.error(error_msg)
            return (
                error_msg,
                gr.update(value="Stop", interactive=True),
                gr.update(interactive=True),
            )

    @staticmethod
    async def run_browser_agent(
        agent_type,
        llm_provider,
        llm_model_name,
        llm_temperature,
        llm_base_url,
        llm_api_key,
        use_own_browser,
        keep_browser_open,
        headless,
        disable_security,
        window_w,
        window_h,
        save_recording_path,
        save_agent_history_path,
        save_trace_path,
        enable_recording,
        task,
        add_infos,
        max_steps,
        use_vision,
        max_actions_per_step,
        tool_calling_method,
    ):
        """
        Master function that decides which agent to run (“org” or “custom”).
        Then returns a tuple of (final_result, errors, model_actions, model_thoughts,
        latest_video, trace_file, history_file, stop_button_update, run_button_update)
        """
        global _global_agent_state
        _global_agent_state.clear_stop()

        try:
            # Disable recording if not checked
            if not enable_recording:
                save_recording_path = None

            # If recording, ensure the directory exists
            if save_recording_path:
                os.makedirs(save_recording_path, exist_ok=True)

            # Keep track of existing videos before run
            existing_videos = set()
            if save_recording_path:
                existing_videos = set(
                    glob.glob(os.path.join(save_recording_path, "*.[mM][pP]4"))
                    + glob.glob(os.path.join(save_recording_path, "*.[wW][eE][bB][mM]"))
                )

            # Build the LLM
            llm = utils.get_llm_model(
                provider=llm_provider,
                model_name=llm_model_name,
                temperature=llm_temperature,
                base_url=llm_base_url,
                api_key=llm_api_key,
            )

            # Run the selected agent
            if agent_type == "org":
                (
                    final_result,
                    errors,
                    model_actions,
                    model_thoughts,
                    trace_file,
                    history_file,
                ) = await run_org_agent(
                    llm=llm,
                    use_own_browser=use_own_browser,
                    keep_browser_open=keep_browser_open,
                    headless=headless,
                    disable_security=disable_security,
                    window_w=window_w,
                    window_h=window_h,
                    save_recording_path=save_recording_path,
                    save_agent_history_path=save_agent_history_path,
                    save_trace_path=save_trace_path,
                    task=task,
                    max_steps=max_steps,
                    use_vision=use_vision,
                    max_actions_per_step=max_actions_per_step,
                    tool_calling_method=tool_calling_method,
                )
            elif agent_type == "custom":
                (
                    final_result,
                    errors,
                    model_actions,
                    model_thoughts,
                    trace_file,
                    history_file,
                ) = await run_custom_agent(
                    llm=llm,
                    use_own_browser=use_own_browser,
                    keep_browser_open=keep_browser_open,
                    headless=headless,
                    disable_security=disable_security,
                    window_w=window_w,
                    window_h=window_h,
                    save_recording_path=save_recording_path,
                    save_agent_history_path=save_agent_history_path,
                    save_trace_path=save_trace_path,
                    task=task,
                    add_infos=add_infos,
                    max_steps=max_steps,
                    use_vision=use_vision,
                    max_actions_per_step=max_actions_per_step,
                    tool_calling_method=tool_calling_method,
                )
            else:
                raise ValueError(f"Invalid agent type: {agent_type}")

            # Identify any new video files created
            latest_video = None
            if save_recording_path:
                new_videos = set(
                    glob.glob(os.path.join(save_recording_path, "*.[mM][pP]4"))
                    + glob.glob(os.path.join(save_recording_path, "*.[wW][eE][bB][mM]"))
                )
                new_creations = new_videos - existing_videos
                if new_creations:
                    # Typically you'd expect only one new video, but just in case
                    latest_video = list(new_creations)[0]

            return (
                final_result,
                errors,
                model_actions,
                model_thoughts,
                latest_video,
                trace_file,
                history_file,
                gr.update(value="Stop", interactive=True),  # stop button re-enable
                gr.update(interactive=True),  # run button re-enable
            )

        except gr.Error:
            # Gradio-specific error, raise it
            raise
        except Exception as e:
            import traceback

            traceback.print_exc()
            errors = str(e) + "\n" + traceback.format_exc()
            return (
                "",
                errors,
                "",
                "",
                None,
                None,
                None,
                gr.update(value="Stop", interactive=True),
                gr.update(interactive=True),
            )

    @staticmethod
    async def run_with_stream(
        agent_type,
        llm_provider,
        llm_model_name,
        llm_temperature,
        llm_base_url,
        llm_api_key,
        use_own_browser,
        keep_browser_open,
        headless,
        disable_security,
        window_w,
        window_h,
        save_recording_path,
        save_agent_history_path,
        save_trace_path,
        enable_recording,
        task,
        add_infos,
        max_steps,
        use_vision,
        max_actions_per_step,
        tool_calling_method,
    ):
        """
        Run the browser agent in a streaming mode for Gradio UI updates.
        """
        global _global_agent_state

        # We'll define some dimensions for the displayed screenshot
        stream_vw = 80
        stream_vh = int(80 * window_h // window_w)

        # If not headless, just run once (no mid-run screenshot needed)
        if not headless:
            result = await WebUIAgent.run_browser_agent(
                agent_type=agent_type,
                llm_provider=llm_provider,
                llm_model_name=llm_model_name,
                llm_temperature=llm_temperature,
                llm_base_url=llm_base_url,
                llm_api_key=llm_api_key,
                use_own_browser=use_own_browser,
                keep_browser_open=keep_browser_open,
                headless=headless,
                disable_security=disable_security,
                window_w=window_w,
                window_h=window_h,
                save_recording_path=save_recording_path,
                save_agent_history_path=save_agent_history_path,
                save_trace_path=save_trace_path,
                enable_recording=enable_recording,
                task=task,
                add_infos=add_infos,
                max_steps=max_steps,
                use_vision=use_vision,
                max_actions_per_step=max_actions_per_step,
                tool_calling_method=tool_calling_method,
            )
            html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Using browser...</h1>"
            yield [html_content] + list(result)

        else:
            # Headless mode: run in background, but periodically update screenshots
            try:
                _global_agent_state.clear_stop()
                agent_task = asyncio.create_task(
                    WebUIAgent.run_browser_agent(
                        agent_type=agent_type,
                        llm_provider=llm_provider,
                        llm_model_name=llm_model_name,
                        llm_temperature=llm_temperature,
                        llm_base_url=llm_base_url,
                        llm_api_key=llm_api_key,
                        use_own_browser=use_own_browser,
                        keep_browser_open=keep_browser_open,
                        headless=headless,
                        disable_security=disable_security,
                        window_w=window_w,
                        window_h=window_h,
                        save_recording_path=save_recording_path,
                        save_agent_history_path=save_agent_history_path,
                        save_trace_path=save_trace_path,
                        enable_recording=enable_recording,
                        task=task,
                        add_infos=add_infos,
                        max_steps=max_steps,
                        use_vision=use_vision,
                        max_actions_per_step=max_actions_per_step,
                        tool_calling_method=tool_calling_method,
                    )
                )

                html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Using browser...</h1>"
                final_result = ""
                errors = ""
                model_actions = ""
                model_thoughts = ""
                latest_videos = None
                trace = None
                history_file = None

                # While the agent task is running, periodically yield screenshots
                while not agent_task.done():
                    try:
                        encoded_screenshot = await capture_screenshot(
                            _global_browser_context
                        )
                        if encoded_screenshot:
                            html_content = (
                                f'<img src="data:image/jpeg;base64,{encoded_screenshot}" '
                                f'style="width:{stream_vw}vw; height:{stream_vh}vh; border:1px solid #ccc;">'
                            )
                        else:
                            html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>"
                    except Exception:
                        html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>"

                    # Check if stop was requested
                    if _global_agent_state.is_stop_requested():
                        yield [
                            html_content,
                            final_result,
                            errors,
                            model_actions,
                            model_thoughts,
                            latest_videos,
                            trace,
                            history_file,
                            gr.update(value="Stopping...", interactive=False),
                            gr.update(interactive=False),
                        ]
                        break
                    else:
                        yield [
                            html_content,
                            final_result,
                            errors,
                            model_actions,
                            model_thoughts,
                            latest_videos,
                            trace,
                            history_file,
                            gr.update(value="Stop", interactive=True),
                            gr.update(interactive=True),
                        ]

                    await asyncio.sleep(0.05)

                # Once the agent finishes, get final results
                try:
                    result = await agent_task
                    (
                        final_result,
                        errors,
                        model_actions,
                        model_thoughts,
                        latest_videos,
                        trace,
                        history_file,
                        stop_button,
                        run_button,
                    ) = result
                except gr.Error:
                    final_result = ""
                    model_actions = ""
                    model_thoughts = ""
                    latest_videos = None
                    trace = None
                    history_file = None
                except Exception as e:
                    errors = f"Agent error: {str(e)}"

                yield [
                    html_content,
                    final_result,
                    errors,
                    model_actions,
                    model_thoughts,
                    latest_videos,
                    trace,
                    history_file,
                    stop_button,
                    run_button,
                ]

            except Exception as e:
                import traceback

                error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
                yield [
                    f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>",
                    "",
                    error_msg,
                    "",
                    "",
                    None,
                    None,
                    None,
                    gr.update(value="Stop", interactive=True),
                    gr.update(interactive=True),
                ]

    def create_ui(self, config, theme_name: str):
        """
        Build and return the entire Gradio Blocks interface.
        """
        css = """
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
            padding-top: 20px !important;
        }
        .header-text {
            text-align: center;
            margin-bottom: 30px;
        }
        .theme-section {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
        }
        """

        chosen_theme = theme_map.get(theme_name, gr.themes.Ocean())

        with gr.Blocks(
            title="AmbientAGI Browser Use WebUI Agent", theme=chosen_theme, css=css
        ) as demo:

            # ---------- HEADER ----------
            with gr.Row():
                gr.Markdown(
                    """
                    # 🌐 AmbientAGI Browser Use WebUI Agent
                    ### Control your browser with AI assistance
                    """,
                    elem_classes=["header-text"],
                )

            # ---------- TABS ----------
            with gr.Tabs() as tabs:

                # ---- Tab 1: Agent Settings
                with gr.TabItem("⚙️ Agent Settings", id=1):
                    with gr.Group():
                        agent_type = gr.Radio(
                            ["org", "custom"],
                            label="Agent Type",
                            value=config["agent_type"],
                            info="Select the type of agent to use",
                        )
                        with gr.Column():
                            max_steps = gr.Slider(
                                minimum=1,
                                maximum=200,
                                value=config["max_steps"],
                                step=1,
                                label="Max Run Steps",
                                info="Maximum number of steps the agent will take",
                            )
                            max_actions_per_step = gr.Slider(
                                minimum=1,
                                maximum=20,
                                value=config["max_actions_per_step"],
                                step=1,
                                label="Max Actions per Step",
                                info="Maximum number of actions the agent will take per step",
                            )
                        with gr.Column():
                            use_vision = gr.Checkbox(
                                label="Use Vision",
                                value=config["use_vision"],
                                info="Enable visual processing capabilities",
                            )
                            tool_calling_method = gr.Dropdown(
                                label="Tool Calling Method",
                                value=config["tool_calling_method"],
                                interactive=True,
                                allow_custom_value=True,
                                choices=["auto", "json_schema", "function_calling"],
                                info="Method for calling the tool",
                                visible=False,  # Hide if you don't need it currently
                            )

                # ---- Tab 2: LLM Configuration
                with gr.TabItem("🔧 LLM Configuration", id=2):
                    with gr.Group():
                        llm_provider = gr.Dropdown(
                            choices=[
                                provider
                                for provider, model in utils.model_names.items()
                            ],
                            label="LLM Provider",
                            value=config["llm_provider"],
                            info="Select your preferred language model provider",
                        )
                        llm_model_name = gr.Dropdown(
                            label="Model Name",
                            choices=utils.model_names.get("openai", []),
                            value=config["llm_model_name"],
                            interactive=True,
                            allow_custom_value=True,
                            info="Select a model or type a custom name",
                        )
                        llm_temperature = gr.Slider(
                            minimum=0.0,
                            maximum=2.0,
                            value=config["llm_temperature"],
                            step=0.1,
                            label="Temperature",
                            info="Controls randomness in model outputs",
                        )
                        with gr.Row():
                            llm_base_url = gr.Textbox(
                                label="Base URL",
                                value=config["llm_base_url"],
                                info="API endpoint URL (if required)",
                            )
                            llm_api_key = gr.Textbox(
                                label="API Key",
                                type="password",
                                value=config["llm_api_key"],
                                info="Your API key (leave blank to use .env)",
                            )

                # ---- Tab 3: Browser Settings
                with gr.TabItem("🌐 Browser Settings", id=3):
                    with gr.Group():
                        with gr.Row():
                            use_own_browser = gr.Checkbox(
                                label="Use Own Browser",
                                value=config["use_own_browser"],
                                info="Use your existing browser instance",
                            )
                            keep_browser_open = gr.Checkbox(
                                label="Keep Browser Open",
                                value=config["keep_browser_open"],
                                info="Keep Browser Open between tasks",
                            )
                            headless = gr.Checkbox(
                                label="Headless Mode",
                                value=config["headless"],
                                info="Run browser without GUI",
                            )
                            disable_security = gr.Checkbox(
                                label="Disable Security",
                                value=config["disable_security"],
                                info="Disable browser security features",
                            )
                            enable_recording = gr.Checkbox(
                                label="Enable Recording",
                                value=config["enable_recording"],
                                info="Enable saving browser recordings",
                            )

                        with gr.Row():
                            window_w = gr.Number(
                                label="Window Width",
                                value=config["window_w"],
                                info="Browser window width",
                            )
                            window_h = gr.Number(
                                label="Window Height",
                                value=config["window_h"],
                                info="Browser window height",
                            )

                        save_recording_path = gr.Textbox(
                            label="Recording Path",
                            placeholder="e.g. ./tmp/record_videos",
                            value=config["save_recording_path"],
                            info="Path to save browser recordings",
                            interactive=True,
                        )

                        save_trace_path = gr.Textbox(
                            label="Trace Path",
                            placeholder="e.g. ./tmp/traces",
                            value=config["save_trace_path"],
                            info="Path to save Agent traces",
                            interactive=True,
                        )

                        save_agent_history_path = gr.Textbox(
                            label="Agent History Save Path",
                            placeholder="e.g., ./tmp/agent_history",
                            value=config["save_agent_history_path"],
                            info="Specify directory to save agent history",
                            interactive=True,
                        )

                # ---- Tab 4: Run Agent
                with gr.TabItem("🤖 Run Agent", id=4):
                    task = gr.Textbox(
                        label="Task Description",
                        lines=4,
                        placeholder="Enter your task here...",
                        value=config["task"],
                        info="Describe what you want the agent to do",
                    )
                    add_infos = gr.Textbox(
                        label="Additional Information",
                        lines=3,
                        placeholder="Add any extra context or instructions...",
                    )

                    with gr.Row():
                        run_button = gr.Button(
                            "▶️ Run Agent", variant="primary", scale=2
                        )
                        stop_button = gr.Button("⏹️ Stop", variant="stop", scale=1)

                    with gr.Row():
                        browser_view = gr.HTML(
                            value="<h1 style='width:80vw; height:50vh'>Waiting for browser session...</h1>",
                            label="Live Browser View",
                        )

                # ---- Tab 5: Configuration load/save
                with gr.TabItem("📁 Configuration", id=5):
                    with gr.Group():
                        config_file_input = gr.File(
                            label="Load Config File",
                            file_types=[".pkl"],
                            interactive=True,
                        )

                        load_config_button = gr.Button(
                            "Load Existing Config From File", variant="primary"
                        )
                        save_config_button = gr.Button(
                            "Save Current Config", variant="primary"
                        )

                        config_status = gr.Textbox(
                            label="Status", lines=2, interactive=False
                        )

                    load_config_button.click(
                        fn=update_ui_from_config,
                        inputs=[config_file_input],
                        outputs=[
                            agent_type,
                            max_steps,
                            max_actions_per_step,
                            use_vision,
                            tool_calling_method,
                            llm_provider,
                            llm_model_name,
                            llm_temperature,
                            llm_base_url,
                            llm_api_key,
                            use_own_browser,
                            keep_browser_open,
                            headless,
                            disable_security,
                            enable_recording,
                            window_w,
                            window_h,
                            save_recording_path,
                            save_trace_path,
                            save_agent_history_path,
                            task,
                            config_status,
                        ],
                    )

                    save_config_button.click(
                        fn=save_current_config,
                        inputs=[
                            agent_type,
                            max_steps,
                            max_actions_per_step,
                            use_vision,
                            tool_calling_method,
                            llm_provider,
                            llm_model_name,
                            llm_temperature,
                            llm_base_url,
                            llm_api_key,
                            use_own_browser,
                            keep_browser_open,
                            headless,
                            disable_security,
                            enable_recording,
                            window_w,
                            window_h,
                            save_recording_path,
                            save_trace_path,
                            save_agent_history_path,
                            task,
                        ],
                        outputs=[config_status],
                    )

                # ---- Tab 6: Results
                with gr.TabItem("📊 Results", id=6):
                    with gr.Group():
                        recording_display = gr.Video(label="Latest Recording")

                        gr.Markdown("### Results")
                        with gr.Row():
                            with gr.Column():
                                final_result_output = gr.Textbox(
                                    label="Final Result", lines=3, show_label=True
                                )
                            with gr.Column():
                                errors_output = gr.Textbox(
                                    label="Errors", lines=3, show_label=True
                                )
                        with gr.Row():
                            with gr.Column():
                                model_actions_output = gr.Textbox(
                                    label="Model Actions", lines=3, show_label=True
                                )
                            with gr.Column():
                                model_thoughts_output = gr.Textbox(
                                    label="Model Thoughts", lines=3, show_label=True
                                )

                        trace_file = gr.File(label="Trace File")
                        agent_history_file = gr.File(label="Agent History")

                    # Bind the stop button click event
                    stop_button.click(
                        fn=WebUIAgent.stop_agent,
                        inputs=[],
                        outputs=[errors_output, stop_button, run_button],
                    )

                    # Run button click event
                    run_button.click(
                        fn=WebUIAgent.run_with_stream,
                        inputs=[
                            agent_type,
                            llm_provider,
                            llm_model_name,
                            llm_temperature,
                            llm_base_url,
                            llm_api_key,
                            use_own_browser,
                            keep_browser_open,
                            headless,
                            disable_security,
                            window_w,
                            window_h,
                            save_recording_path,
                            save_agent_history_path,
                            save_trace_path,
                            enable_recording,
                            task,
                            add_infos,
                            max_steps,
                            use_vision,
                            max_actions_per_step,
                            tool_calling_method,
                        ],
                        outputs=[
                            browser_view,
                            final_result_output,
                            errors_output,
                            model_actions_output,
                            model_thoughts_output,
                            recording_display,
                            trace_file,
                            agent_history_file,
                            stop_button,
                            run_button,
                        ],
                    )

                # ---- Tab 7: Recordings
                with gr.TabItem("🎥 Recordings", id=7):

                    def list_recordings(path_to_recordings):
                        if not os.path.exists(path_to_recordings):
                            return []

                        # Gather all video files
                        recordings = glob.glob(
                            os.path.join(path_to_recordings, "*.[mM][pP]4")
                        ) + glob.glob(
                            os.path.join(path_to_recordings, "*.[wW][eE][bB][mM]")
                        )
                        recordings.sort(key=os.path.getctime)  # sort by creation time
                        numbered = [
                            (rec, f"{i}. {os.path.basename(rec)}")
                            for i, rec in enumerate(recordings, start=1)
                        ]
                        return numbered

                    recordings_gallery = gr.Gallery(
                        label="Recordings",
                        value=list_recordings(config["save_recording_path"]),
                        columns=3,
                        height="auto",
                        object_fit="contain",
                    )

                    refresh_button = gr.Button(
                        "🔄 Refresh Recordings", variant="secondary"
                    )
                    refresh_button.click(
                        fn=list_recordings,
                        inputs=save_recording_path,
                        outputs=recordings_gallery,
                    )

            # Automatically update model_name dropdown when llm_provider changes
            llm_provider.change(
                lambda provider, api_key, base_url: update_model_dropdown(
                    provider, api_key, base_url
                ),
                inputs=[llm_provider, llm_api_key, llm_base_url],
                outputs=llm_model_name,
            )

            # If recording is disabled, gray out the path
            enable_recording.change(
                lambda enabled: gr.update(interactive=enabled),
                inputs=enable_recording,
                outputs=save_recording_path,
            )

            # If we change these, let's close the browser so new settings apply
            use_own_browser.change(fn=close_global_browser)
            keep_browser_open.change(fn=close_global_browser)

        return demo

    def launch(self):
        """
        Command-line entry: parse arguments, launch the Gradio app.
        """
        parser = argparse.ArgumentParser(description="Gradio UI for Browser Agent")
        parser.add_argument(
            "--ip", type=str, default=self.ip, help="IP address to bind to"
        )
        parser.add_argument(
            "--port", type=int, default=self.port, help="Port to listen on"
        )
        parser.add_argument(
            "--theme",
            type=str,
            default=self.theme,
            choices=theme_map.keys(),
            help="Theme to use for the UI",
        )
        parser.add_argument("--dark-mode", action="store_true", help="Enable dark mode")
        args = parser.parse_args()

        demo = self.create_ui(config=self.config, theme_name=args.theme)
        demo.launch(server_name=args.ip, server_port=args.port, share=True)


def main():
    """
    Standalone entry point if you run: python webui_agent.py --port 7788
    """
    agent = WebUIAgent()
    agent.launch()


if __name__ == "__main__":
    main()
