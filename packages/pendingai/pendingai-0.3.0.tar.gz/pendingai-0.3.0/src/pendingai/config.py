#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
import typing
from datetime import datetime, tzinfo

import rich.theme
import typer

from pendingai import Environment

# local datetime tzinfo used for setting timezones for datetime objects.
LOCAL_TZINFO: tzinfo | None = datetime.now().tzinfo

# app-name is required for the main command name for the typer app; also
# used for package distribution loading the installed version; package
# should be named this in 'pyproject.toml'.
APPLICATION_NAME: str = "pendingai"

# typer app directory consistent for any operating system and is then
# created if it doesn't already exist.
APPLICATION_DIRECTORY: pathlib.Path = pathlib.Path(
    typer.get_app_dir(APPLICATION_NAME, force_posix=True)
)
APPLICATION_DIRECTORY.mkdir(parents=True, exist_ok=True)

# rich consoles are used and for each a default set of styles are loaded
# to be consistent and concise for application logic; update themes for
# more control below.
RICH_CONSOLE_THEME: rich.theme.Theme = rich.theme.Theme(
    styles={
        "warn": "yellow not bold",
        "success": "green not bold",
        "fail": "red bold",
        "link": "blue bold underline",
    }
)

# console width for help text and rich console output formatting
CONSOLE_WIDTH: int = 88

# upload limit in bytes for api service requests.
FILE_SIZE_UPLOAD_LIMIT: float = 6e6

# httpx package timeout in seconds; matches external api requests.
HTTPX_TIMEOUT_SECONDS: int = 10

# external documentation redirect url for pending.ai docs webpages.
PENDINGAI_DOCS_REDIRECT_URL: str = "https://docs.pending.ai/"

# external api urls for each deployment environment; used when create
# api clients with subdomains for each hidden environment option.
API_BASE_URLS: dict[Environment, str] = {
    Environment.DEVELOPMENT: "https://api.dev.pending.ai/",
    Environment.STAGING: "https://api.stage.pending.ai/",
    Environment.PRODUCTION: "https://api.pending.ai/",
}

# external service subdomains.
RETRO_SUBDOMAIN: str = "/retro/v2"
GENERATOR_SUBDOMAIN: str = "/generator/v1"

# authorizer utility class for storing authorizer fields; required when
# processing authentication jwts and access tokens for access control.
Authorizer = typing.TypedDict(
    "Authorizer", {"domain": str, "client_id": str, "audience": str}
)

# static authorizers use public knowledge for checking and validating
# access tokens with an external authorizer and approved tokens before
# making a request and receiving an unauthorized response.
AUTHORIZERS: dict[Environment, Authorizer] = {
    Environment.DEVELOPMENT: Authorizer(
        domain="pendingai-dev.au.auth0.com",
        client_id="GM1gfvGCnokIySbVO7vjmkRy4tVx5WYm",
        audience="api.dev.pending.ai/external-api",
    ),
    Environment.STAGING: Authorizer(
        domain="pendingai-stage.au.auth0.com",
        client_id="PDWKoudtiP4WZV7aQt5YZbb5xlcmN6ju",
        audience="api.stage.pending.ai/external-api",
    ),
    Environment.PRODUCTION: Authorizer(
        domain="pendingai.us.auth0.com",
        client_id="dH69BCxGo4MyCcMWi64ZBq2YZx3UIoh1",
        audience="api.pending.ai/external-api",
    ),
}
