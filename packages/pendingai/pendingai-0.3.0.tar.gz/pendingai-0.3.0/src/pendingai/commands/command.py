#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import webbrowser

import rich
import typer

from pendingai import config

console = rich.console.Console(
    theme=config.RICH_CONSOLE_THEME, width=config.CONSOLE_WIDTH
)

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_show_locals=False,
    rich_markup_mode=None,
    context_settings={"max_content_width": config.CONSOLE_WIDTH},
)

# region command: docs -------------------------------------------------


@app.command(
    "docs",
    help="Open documentation in a web browser.",
    short_help="Open documentation in a web browser.",
)
def open_documentation_page() -> bool:
    """
    Notify the user that the documentation redirect url will be opened
    in their browser and attempt to create a new tab for the docs page.

    Returns:
        bool: Success flag from `webbrowser` on whether the tab was
            opened successfully.
    """
    redirect_url: str = config.PENDINGAI_DOCS_REDIRECT_URL
    console.print(f"[warn]! Redirecting to [link]{redirect_url}[/] in your browser...")
    time.sleep(1)
    return webbrowser.open_new_tab(redirect_url)
