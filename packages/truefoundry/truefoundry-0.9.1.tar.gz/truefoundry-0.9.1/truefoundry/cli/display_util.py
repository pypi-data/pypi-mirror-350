import datetime
import json
from collections.abc import Iterable
from typing import Optional, cast

from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
    ChatCompletionMessageToolCallParam,
)
from rich import box
from rich import print_json as _rich_print_json
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from truefoundry.cli.config import CliConfig
from truefoundry.cli.console import console
from truefoundry.cli.const import DISPLAY_DATETIME_FORMAT


def json_default_encoder(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()
    raise TypeError(f"Cannot json encode {type(o)}: {o}")


def print_json(data, default=json_default_encoder):
    return _rich_print_json(
        json.dumps(data, default=default), highlight=False, default=default
    )


NO_WRAP_COLUMNS = {"fqn"}


def get_table(title):
    return Table(title=title, show_lines=False, safe_box=True, box=box.MINIMAL)


def stringify(x):
    if isinstance(x, datetime.datetime):
        return x.astimezone().strftime(DISPLAY_DATETIME_FORMAT)
    elif isinstance(x, str):
        return x
    else:
        return str(x)


def display_time_passed(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    result = ""
    if d != 0:
        result = f"{int(d)}D"
    elif h != 0 and m != 0:
        result = f"{int(h)}h {int(m)}m"
    elif h != 0:
        result = f"{int(h)}h"
    elif m != 0 and s != 0:
        result = f"{int(m)}m {int(s)}s"
    elif m != 0:
        result = f"{int(m)}m"
    elif s != 0:
        result = f"{int(s)}s"
    return result


def print_entity_list(title, items):
    items = [item.list_row_data() for item in items]
    if CliConfig.json:
        print_json(data=items)
        return

    table = get_table(title)

    columns = []
    if items:
        columns = items[0].keys()
        for column in columns:
            no_wrap = column in NO_WRAP_COLUMNS
            table.add_column(column, justify="left", overflow="fold", no_wrap=no_wrap)

    for item in items:
        row = []
        for c in columns:
            row.append(stringify(item[c]))
        table.add_row(*row)
    console.print(table)


def print_obj(title, item, columns=None):
    if CliConfig.json:
        print_json(data=item)
        return

    table = get_table(title)

    if not columns:
        columns = item.keys()

    # transpose
    keys, columns = columns, ["key", "value"]

    for column in columns:
        no_wrap = column in NO_WRAP_COLUMNS
        table.add_column(column, justify="left", overflow="fold", no_wrap=no_wrap)
    for key in keys:
        table.add_row(f"[bold]{stringify(key)}[/]", stringify(item[key]))
    console.print(table)


def print_entity_obj(title, entity):
    if CliConfig.json:
        print_json(data=entity)
        return

    table = get_table(title)

    columns = entity.get_data().keys()

    # transpose
    keys, columns = columns, ["key", "value"]

    for column in columns:
        no_wrap = "FQN" in column or "Name" in column
        table.add_column(column, justify="left", overflow="fold", no_wrap=no_wrap)
    entity_data = entity.get_data()
    for key in keys:
        table.add_row(f"[bold]{stringify(key)}[/]", stringify(entity_data[key]))
    console.print(table)


def log_chat_completion_message(
    message: ChatCompletionMessageParam, console_: Optional[Console] = None
) -> None:
    timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    code_theme = "github-dark"
    target_console = console_ or console
    try:
        _content = message.get("content") or ""
        message_content = f"```json\n{json.dumps(json.loads(_content), indent=2)}\n```"
    except (TypeError, ValueError):
        message_content = str(message.get("content") or "")

    tool_calls: Iterable[ChatCompletionMessageToolCallParam] = cast(
        list[ChatCompletionMessageToolCallParam],
        message.get("tool_calls", []),
    )

    rendered_content: list[Markdown | Text] = []

    if bool(message_content.strip()):
        rendered_content.append(Markdown(markup=message_content, code_theme=code_theme))

    for call in tool_calls:
        assert isinstance(call, ChatCompletionMessageToolCall)
        name = call.function.name
        args = call.function.arguments
        rendered_content.append(
            Text.from_markup(
                "[bold magenta]Tool Calls:[/bold magenta]\n",
                overflow="fold",
            )
        )
        rendered_content.append(
            Markdown(markup=f"```python\n▶ {name}({args})\n```", code_theme=code_theme)
        )

    if not rendered_content:
        return

    panel = Panel(
        Group(*rendered_content, fit=True),
        title=f"[bold blue]{timestamp}[/bold blue]",
        title_align="left",
        border_style="bright_blue",
        padding=(1, 2),
        expand=True,
        width=console.width,
    )
    target_console.print(panel)
