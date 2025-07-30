try:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client
    from mcp.types import TextContent
except ImportError:
    import sys

    python_version = sys.version_info
    raise ImportError(
        f"This feature requires Python 3.10 or higher. Your current Python version is '{python_version.major}.{python_version.minor}.{python_version.micro}'. "
        "Please upgrade to a supported version."
    ) from None

import json
from contextlib import AsyncExitStack
from typing import List, Optional, Union

import rich_click as click
from openai import NOT_GIVEN, AsyncOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel
from rich.console import Console
from rich.status import Status

from truefoundry.cli.display_util import log_chat_completion_message
from truefoundry.common.constants import ENV_VARS
from truefoundry.logger import logger

console = Console(soft_wrap=False)


class AskClient:
    """Handles the chat session lifecycle between the user and the assistant via OpenAI and MCP."""

    def __init__(
        self,
        cluster: str,
        token: str,
        openai_model: str,
        debug: bool = False,
        openai_client: Optional[AsyncOpenAI] = None,
    ):
        self.cluster = cluster
        self.token = token
        self.debug = debug

        self.async_openai_client = openai_client or AsyncOpenAI()
        # Initialize the OpenAI client with the session
        self.openai_model = openai_model
        self._log_message(
            f"\nInitialize OpenAI client with model: {self.openai_model!r}, base_url: {str(self.async_openai_client.base_url)!r}\n"
        )

        self.exit_stack = AsyncExitStack()
        self.history: List[ChatCompletionMessageParam] = []
        self._cached_tools: Optional[List[ChatCompletionToolParam]] = None

    async def connect(self, server_url: str, prompt_name: Optional[str] = None):
        """Initialize connection to the SSE-based MCP server and prepare the chat session."""
        try:
            logger.debug(f"Starting a new client for {server_url}")
            self._streams_context = streamablehttp_client(
                url=server_url, headers=self._auth_headers()
            )
            (
                read_stream,
                write_stream,
                _,
            ) = await self._streams_context.__aenter__()
            self._session_context = ClientSession(
                read_stream=read_stream, write_stream=write_stream
            )
            self.session = await self._session_context.__aenter__()
            await self.session.initialize()
            self._log_message("Connected and session initialized.")
            await self._list_tools()  # Pre-load tool definitions for tool-calling
            self._log_message(
                "\nTFY ASK is ready. Type 'exit' to quit.", log=self.debug
            )

            await self._load_initial_prompt(prompt_name)

        except Exception as e:
            self._log_message(f"❌ Connection error: {e}")
            await self.cleanup()
            raise
        finally:
            await self.exit_stack.__aenter__()

    async def cleanup(self):
        """Properly close all async contexts opened during session initialization."""
        for context in [
            getattr(self, "_session_context", None),
            getattr(self, "_streams_context", None),
        ]:
            if context:
                await context.__aexit__(None, None, None)

    async def chat_loop(self):
        """Interactive loop: accepts user queries and returns responses until interrupted or 'exit' is typed."""
        await self.process_query()  # Optional greeting message from assistant

        while True:
            try:
                query = click.prompt(click.style("User", fg="yellow"), type=str)
                if not query:
                    self._log_message("Empty query. Type 'exit' to quit.", log=True)
                    continue

                if query.lower() in ("exit", "quit"):
                    self._log_message("Exiting chat...")
                    break

                await self.process_query(query)

            except (KeyboardInterrupt, EOFError, click.Abort):
                self._log_message("\nChat interrupted.")
                break

    async def process_query(self, query: Optional[str] = None, max_turns: int = 50):
        """Handles sending user input to the assistant and processing the assistant’s reply."""
        if query:
            self._append_message(
                ChatCompletionUserMessageParam(role="user", content=query),
                log=self.debug,
            )

        tools = await self._list_tools()  # Fetch or use cached tool list

        turn: int = 0
        # Backup history to revert if OpenAI call fails
        _checkpoint_idx = len(self.history)

        with console.status(status="Thinking...", spinner="dots") as spinner:
            while True:
                try:
                    if turn >= max_turns:
                        self._log_message("Max turns reached. Exiting.")
                        break
                    spinner.update("Thinking...", spinner="dots")
                    response = await self._call_openai(
                        model=self.openai_model, tools=tools
                    )
                    turn += 1
                    message = response.choices[0].message

                    if message.tool_calls:
                        await self._handle_tool_calls(message, spinner)
                    elif message.content:
                        self._append_message(
                            ChatCompletionAssistantMessageParam(
                                role="assistant", content=message.content
                            )
                        )
                        break
                    else:
                        self._log_message("No assistant response.")
                        break
                except Exception as e:
                    self._log_message(f"OpenAI call failed: {e}", log=self.debug)
                    console.print(
                        "Something went wrong. Please try rephrasing your query."
                    )
                    self.history = self.history[
                        :_checkpoint_idx
                    ]  # Revert to safe state
                    turn = 0
                    break

    async def _list_tools(self) -> Optional[List[ChatCompletionToolParam]]:
        """Fetch and cache the list of available tools from the MCP session."""
        if self._cached_tools:
            return self._cached_tools

        self._cached_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in (await self.session.list_tools()).tools
        ]

        self._log_message("\nAvailable tools:")
        for tool in self._cached_tools or []:
            self._log_message(
                f"  - {tool['function']['name']}: {tool['function']['description']}"
            )
        return self._cached_tools

    async def _load_initial_prompt(self, prompt_name: Optional[str]) -> None:
        """Load a system prompt to set assistant behavior at session start."""
        if not (self.session and prompt_name):
            return

        result = await self.session.get_prompt(name=prompt_name)
        if not result:
            self._log_message("Failed to get initial system prompt.")
            return

        for message in result.messages:
            data = message.model_dump() if isinstance(message, BaseModel) else message
            content = None
            if isinstance(data, dict):
                content = (
                    data.get("content", {}).get("text")
                    if isinstance(data.get("content"), dict)
                    else data.get("content")
                )
            else:
                content = data

            # First message is system prompt?

            if content:
                self._append_message(
                    ChatCompletionSystemMessageParam(role="system", content=content),
                    log=self.debug,
                )

    async def _call_openai(
        self, model: str, tools: Optional[List[ChatCompletionToolParam]]
    ):
        """Make a chat completion request to OpenAI with optional tool support."""
        return await self.async_openai_client.chat.completions.create(
            model=model,
            messages=self.history,
            tools=tools or NOT_GIVEN,
            temperature=0.0,  # Set to 0 for deterministic behavior
            top_p=1,
        )

    async def _handle_tool_calls(self, message, spinner: Status):
        """Execute tool calls returned by the assistant and return the results."""
        for tool_call in message.tool_calls:
            try:
                spinner.update(
                    f"Executing tool: {tool_call.function.name}", spinner="aesthetic"
                )
                args = json.loads(tool_call.function.arguments)
                result = await self.session.call_tool(tool_call.function.name, args)
                content = getattr(result, "content", result)
                result_content = self._format_tool_result(content)
            except Exception as e:
                result_content = f"Tool `{tool_call.function.name}` call failed: {e}"

            # Log assistant's tool call
            self._append_message(
                ChatCompletionAssistantMessageParam(
                    role="assistant", content=None, tool_calls=[tool_call]
                ),
                log=self.debug,
            )

            # Log tool response
            self._append_message(
                ChatCompletionToolMessageParam(
                    role="tool", tool_call_id=tool_call.id, content=result_content
                ),
                log=self.debug,
            )

    def _format_tool_result(self, content) -> str:
        """Format tool result into a readable string or JSON block."""
        if isinstance(content, list):
            content = (
                content[0].text
                if len(content) == 1 and isinstance(content[0], TextContent)
                else content
            )
            if isinstance(content, list):
                return (
                    "```\n"
                    + "\n".join(
                        (
                            item.model_dump_json(indent=2)
                            if isinstance(item, BaseModel)
                            else str(item)
                        )
                        for item in content
                    )
                    + "\n```"
                )

        if isinstance(content, (BaseModel, dict)):
            return (
                "```\n"
                + json.dumps(
                    content.model_dump() if isinstance(content, BaseModel) else content,
                    indent=2,
                )
                + "\n```"
            )

        if isinstance(content, str):
            try:
                return "```\n" + json.dumps(json.loads(content), indent=2) + "\n```"
            except Exception:
                return content

        return str(content)

    def _append_message(self, message: ChatCompletionMessageParam, log: bool = True):
        """Append a message to history and optionally log it."""
        self._log_message(message, log)
        self.history.append(message)

    def _auth_headers(self):
        """Generate authorization headers for connecting to the SSE server."""
        return {
            "Authorization": f"Bearer {self.token}",
            "X-TFY-Cluster-Id": self.cluster,
        }

    def _log_message(
        self,
        message: Union[str, ChatCompletionMessageParam],
        log: bool = False,
    ):
        """Display a message using Rich console, conditionally based on debug settings."""
        if not self.debug and not log:
            return
        if isinstance(message, str):
            console.print(message)
        else:
            log_chat_completion_message(message, console_=console)


async def ask_client_main(
    cluster: str,
    server_url: str,
    token: str,
    openai_model: str,
    debug: bool = False,
    openai_client: Optional[AsyncOpenAI] = None,
):
    """Main entrypoint for launching the AskClient chat loop."""
    ask_client = AskClient(
        cluster=cluster,
        token=token,
        debug=debug,
        openai_client=openai_client,
        openai_model=openai_model,
    )
    try:
        await ask_client.connect(
            server_url=server_url, prompt_name=ENV_VARS.TFY_ASK_SYSTEM_PROMPT_NAME
        )
        await ask_client.chat_loop()
    except Exception as e:
        console.print(
            f"[red]An unexpected error occurred while running the assistant: {e}[/red], Check with TrueFoundry support for more details."
        )
    except KeyboardInterrupt:
        console.print("[yellow]Chat interrupted.[/yellow]")
    finally:
        await ask_client.cleanup()
