#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import rich
import typer

from pendingai import config
from pendingai.commands.auth.controller import AuthController
from pendingai.context import Context

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)

app = typer.Typer(
    name="auth",
    help="Authenticate with the Pending AI platform.",
    short_help="Authenticate with the Pending AI platform.",
    no_args_is_help=True,
    add_completion=False,
)


# region command: login ------------------------------------------------


@app.command(
    "login",
    help=(
        "Login to a Pending AI account. Device authorization will open a web "
        "browser window. \n\nFor any account problems, contact Pending AI via "
        "email at support@pending.ai."
    ),
    short_help="Login to a Pending AI account.",
)
def session_login(context: Context) -> None:
    """
    Execute a user login auth0 authentication flow; check if an access
    token exists already cached and if it has expired attempt to refresh
    the token; otherwise login the user if that fails or has no token.

    Args:
        context (Context): App runtime context.
    """
    controller = AuthController(context)

    # check the token exists and if it has expired, then refresh the
    # token, if that fails or no token is found then the login flow is
    # run and then the cache is updated.
    if context.obj.cache.access_token and context.obj.cache.access_token.is_expired():
        console.print("[warn]! Authentication has expired, requesting a session token.")
        refresh_token: str | None = context.obj.cache.access_token.refresh_token
        context.obj.cache.access_token = controller.refresh_token(refresh_token)
    if context.obj.cache.access_token is None:
        context.obj.cache.access_token = controller.login()
    context.obj.update_cache()

    # pull the user email claim from the token jwt if it exists and show
    # feedback to the user; return the jwt access token.
    email: str = context.obj.cache.access_token.get_jwt_claim("email", "Pending AI")
    console.print("[success]✓ Authentication complete.")
    console.print(f"[success]✓ Logged in as [b underline]{email}[/].")


# region command: logout -----------------------------------------------


@app.command(
    "logout",
    help=(
        "Logout of a Pending AI account. Removes locally cached authentication details."
    ),
    short_help="Logout of a Pending AI account.",
)
def session_logout(context: Context) -> None:
    """
    Log out the user from a current access token "session" and delete it
    from the cache file by setting to `None` and updating the file.

    Args:
        context (Context): App runtime context.
    """
    # check if the token exists and report back the user email claim if
    # it is in the jwt token and delete from the cache file; otherwise
    # tell the user they are already logged out.
    if context.obj.cache.access_token:
        email: str = context.obj.cache.access_token.get_jwt_claim("email", "Pending AI")
        context.obj.cache.access_token = None
        context.obj.update_cache()
        console.print(f"[success]✓ Logged out [b underline]{email}[/].")
    else:
        console.print("[warn]! Already logged out.")


# region command: refresh ----------------------------------------------


@app.command(
    "refresh",
    help="Refresh an active authenticated session.",
    short_help="Refresh an active authenticated session.",
)
def refresh_active_session(context: Context) -> str:
    """
    Refresh an active authenticated session; identical logic to if the
    user performed `pendingai auth login` with an expired access token.

    Args:
        context (Context): App runtime context.

    Raises:
        typer.Exit: Session token does not exist in the cache or the
            existing token from the cache is expired; failed to refresh
            the access token.

    Returns:
        str: Auth0 jwt access token.
    """
    controller = AuthController(context)

    # check if the access token does not exist and redirect to the login
    # command, exit with non-zero status.
    if context.obj.cache.access_token is None:
        console.print("[warn]! No logged in user, use [code]pendingai auth login[/].")
        raise typer.Exit(1)

    # attempt to refresh the access token if it exists and if that fails
    # redirect to the login command, exit with non-zero status.
    if context.obj.cache.access_token is None:
        console.print("[warn]! No refresh token found, unable to refresh session.")
        raise typer.Exit(1)
    context.obj.cache.access_token = controller.refresh_token(
        context.obj.cache.access_token.refresh_token
    )
    context.obj.update_cache()
    if context.obj.cache.access_token:
        return context.obj.cache.access_token.access_token
    raise typer.Exit(1)


# region command: status -----------------------------------------------


@app.command(
    "status",
    help="Show active session information.",
    short_help="Show active session information.",
)
def active_session_info(context: Context) -> None:
    """
    Parse an access token jwt claims and output session information like
    the remaining time, the registered user account and organization but
    only if they exist in the claims.

    Args:
        context (Context): App runtime context.

    Raises:
        typer.Exit: Session token does not exist in the cache or the
            existing token from the cache is expired; failed to extract
            the expiry time from the access token jwt claims.
    """
    # check if the access token does not exist and redirect to the login
    # command, check if the access token has expired and redirect to the
    # refresh command, exit both with non-zero status.
    if context.obj.cache.access_token is None:
        console.print("[warn]! No logged in user, use [code]pendingai auth login[/].")
        raise typer.Exit(1)
    elif context.obj.cache.access_token.is_expired():
        console.print("[warn]! Access has expired, use [code]pendingai auth refresh[/].")
        raise typer.Exit(1)

    # extract relevant fields from the token jwt and display them on the
    # conditional they exist in the access token jwt claims; parse the
    # expiry time into human readable format.
    token_exp: int | None = context.obj.cache.access_token.get_jwt_claim("exp")
    user_email: str | None = context.obj.cache.access_token.get_jwt_claim("email")
    user_org_name: str | None = context.obj.cache.access_token.get_jwt_claim("org_name")
    if token_exp is None:
        console.print("[fail]Invalid session, use [code]pendingai auth login[/].")
        context.obj.delete_cache()
        raise typer.Exit(1)

    # output session information like the formatted remaining time, the
    # user email and organization if they exist in the custom claims.
    delta: timedelta = datetime.fromtimestamp(token_exp, timezone.utc) - datetime.now(
        timezone.utc
    )
    if delta.days >= 1:
        console.print("[success]✓ Session is active: Over 1 day remaining")
    elif delta.total_seconds() < 60:
        console.print("[warn]! Session is closing soon: Less than 1 minute remaining")
    else:
        time_left: str = str(delta).split(".")[0]
        console.print(f"[success]✓ Session is active: [not b]{time_left} remaining")

    if user_email is not None:
        console.print(f"- Session user account: [b underline]{user_email}")
    if user_org_name is not None:
        console.print(f"- Session organization: [b]{user_org_name}")


# region command: token ------------------------------------------------


@app.command(
    "token",
    help="Get the access token of the current session.",
    short_help="Get the access token of the current session.",
)
def show_session_token(context: Context) -> None:
    """
    Verify that a session token exists for in the runtime context and it
    has not expired. Output the session token to standard out with extra
    information for the user.

    Args:
        context (Context): App runtime context.

    Raises:
        typer.Exit: Session token does not exist in the cache or the
            existing token from the cache is expired.
    """
    # capture conditions when the session token is not provided or if a
    # session token that is found has already expired; print feedback on
    # what to do and exit with non-zero status.
    if context.obj.cache.access_token is None:
        suggestion: str = "[code]pendingai auth login[/]"
        console.print(f"[warn]! No logged in user, use {suggestion}.")
        raise typer.Exit(1)
    elif context.obj.cache.access_token.is_expired():
        suggestion = "[code]pendingai auth refresh[/]"
        console.print(f"[warn]! Access token has expired; use {suggestion}.")
        raise typer.Exit(1)

    # output the access token to the user with their email if it is in
    # the token custom claims; return the access token and print cleanly
    # for potentially missing email claim.
    email: str = context.obj.cache.access_token.get_jwt_claim("email", "Pending AI")
    console.print(f"[success]✓ Access token for [b underline]{email}[/].")
    console.print(f"\b{context.obj.cache.access_token.access_token}")
