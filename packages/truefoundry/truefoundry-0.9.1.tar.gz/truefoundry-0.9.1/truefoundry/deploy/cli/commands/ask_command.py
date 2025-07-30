import asyncio
import logging
from typing import Tuple

import rich_click as click
from openai import AsyncOpenAI
from rich.console import Console

from truefoundry.cli.config import CliConfig
from truefoundry.cli.const import COMMAND_CLS
from truefoundry.cli.util import handle_exception_wrapper
from truefoundry.common.constants import (
    ENV_VARS,
    OPENAI_API_KEY_KEY,
    OPENAI_MODEL_KEY,
    TFY_ASK_MODEL_NAME_KEY,
    TFY_ASK_OPENAI_API_KEY_KEY,
    TFY_ASK_OPENAI_BASE_URL_KEY,
)
from truefoundry.common.session import Session
from truefoundry.common.utils import get_tfy_servers_config
from truefoundry.deploy.cli.commands.utils import select_cluster

console = Console()


def _get_openai_client() -> Tuple[AsyncOpenAI, str]:
    """
    Returns an AsyncOpenAI client using either user-provided credentials or TrueFoundry LLM gateway.
    """
    console.print("")
    default_model = "gpt-4o"
    if ENV_VARS.TFY_ASK_OPENAI_BASE_URL and ENV_VARS.TFY_ASK_OPENAI_API_KEY:
        console.print(
            f"Found custom OpenAI API settings ([green]{TFY_ASK_OPENAI_BASE_URL_KEY}[/green], [green]{TFY_ASK_OPENAI_API_KEY_KEY}[/green]) in env"
        )
        client = AsyncOpenAI(
            base_url=ENV_VARS.TFY_ASK_OPENAI_BASE_URL,
            api_key=ENV_VARS.TFY_ASK_OPENAI_API_KEY,
        )
        if ENV_VARS.TFY_ASK_MODEL_NAME:
            openai_model = ENV_VARS.TFY_ASK_MODEL_NAME
            console.print(
                f"Using custom OpenAI model from env [green]{TFY_ASK_MODEL_NAME_KEY}[/green]: [yellow]{openai_model}[/yellow]"
            )
        else:
            openai_model = default_model
            console.print(
                f"Using default OpenAI model: [yellow]{openai_model}[/yellow]"
                f"\n[dim]Tip: To use a different model, set the env var "
                f"[green]{TFY_ASK_MODEL_NAME_KEY}[/green] to the model name you want to use.[/dim]"
            )
        console.print(
            "[dim][yellow]This operation will use tokens from your model provider and may incur costs.[/yellow][/dim]"
        )
        console.print("")
        return client, openai_model
    elif ENV_VARS.OPENAI_API_KEY:
        console.print(f"Found [green]{OPENAI_API_KEY_KEY}[/green] in env")
        client = AsyncOpenAI(
            api_key=ENV_VARS.OPENAI_API_KEY,
        )
        if ENV_VARS.OPENAI_MODEL:
            openai_model = ENV_VARS.OPENAI_MODEL
            console.print(
                f"Using custom OpenAI model from env [green]{OPENAI_MODEL_KEY}[/green]: [yellow]{openai_model}[/yellow]"
            )
        else:
            openai_model = default_model
            console.print(
                f"Using default OpenAI model: [yellow]{openai_model}[/yellow]"
                f"\n[dim]Tip: To use a different OpenAI model, set the env var "
                f"[green]{OPENAI_MODEL_KEY}[/green] to the model name you want to use.[/dim]"
            )
        console.print(
            f"[dim]Tip: To use your own OpenAI API compatible model for the ask command, set the env vars "
            f"[green]{TFY_ASK_OPENAI_BASE_URL_KEY}[/], "
            f"[green]{TFY_ASK_OPENAI_API_KEY_KEY}[/], and "
            f"[green]{TFY_ASK_MODEL_NAME_KEY}[/].[/dim]"
        )
        console.print(
            "[dim][yellow]This operation will use tokens from your OpenAI account and may incur costs.[/yellow][/dim]"
        )
        console.print("")
        return client, openai_model
    else:
        llm_env_instruction = (
            "[dim]No OpenAI API key found in env."
            f"\n- To use your own OpenAI API compatible model for the ask command, set the env vars "
            f"[green]{TFY_ASK_OPENAI_BASE_URL_KEY}[/], "
            f"[green]{TFY_ASK_OPENAI_API_KEY_KEY}[/], and "
            f"[green]{TFY_ASK_MODEL_NAME_KEY}[/] (default: {default_model})."
            f"\n- Alternatively, you can use the default OpenAI model by setting the env vars "
            f"[green]{OPENAI_API_KEY_KEY}[/], "
            f"[green]{OPENAI_MODEL_KEY}[/] (default: {default_model}).[/dim]"
        )
        raise ValueError(llm_env_instruction)


@click.command(name="ask", cls=COMMAND_CLS)
@click.option(
    "-c",
    "--cluster",
    type=str,
    required=False,
    help="The cluster id from TrueFoundry. If not provided, an interactive prompt will list available clusters",
)
@click.pass_context
@handle_exception_wrapper
def ask_command(ctx, cluster: str) -> None:
    """
    Ask questions related to your Cluster in TrueFoundry.
    """
    from truefoundry.deploy.lib.clients.ask_client import ask_client_main

    debug = CliConfig.debug
    if debug:
        _mcp_logger = logging.getLogger("mcp")
        _mcp_logger.setLevel(logging.DEBUG)
        _mcp_logger.addHandler(logging.StreamHandler())

    session = Session.new()
    console.print(
        "\n[bold green]Welcome to the Ask Command![/bold green]\n"
        "Use this command to ask questions and troubleshoot issues in your Kubernetes cluster managed by the TrueFoundry Control Plane.\n"
        "It helps you investigate and identify potential problems across services, pods, deployments, and more.\n"
    )

    if not cluster:
        console.print(
            "[dim]Tip: You can specify a cluster using the '--cluster' option, or select one interactively from the list.[/dim]\n"
        )

    # Get the cluster id from the command line argument
    cluster = select_cluster(cluster)
    openai_client, openai_model = _get_openai_client()
    tfy_servers_config = get_tfy_servers_config(session.tfy_host)
    mcp_server_url = f"{tfy_servers_config.servicefoundry_server_url}/v1/k8s-mcp"
    asyncio.run(
        ask_client_main(
            cluster=cluster,
            server_url=mcp_server_url,
            token=session.access_token,
            openai_client=openai_client,
            openai_model=openai_model,
            debug=debug,
        )
    )


def get_ask_command():
    return ask_command
