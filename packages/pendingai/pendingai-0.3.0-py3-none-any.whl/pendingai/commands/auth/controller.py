#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import time
import webbrowser

import httpx
import pydantic
import rich
import typer

from pendingai import config
from pendingai.auth import AccessToken
from pendingai.context import Context

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class AuthController:
    """
    Controller for `pendingai auth` subcommands. Controls authentication
    flows with respect to Auth0 and parses the chosen authorizer from an
    app runtime context environment.

    Args:
        context (Context): App runtime context.
    """

    device_code_retries: int = 25
    access_token_scopes: str = "openid profile email offline_access generator:admin"
    device_code_grant_type: str = "urn:ietf:params:oauth:grant-type:device_code"

    def __init__(self, context: Context) -> None:
        # parse the app context to get the auth0 authorizer details
        # required from making http requests to the server.
        self.context: Context = context
        authorizer: config.Authorizer = config.AUTHORIZERS[context.obj.environment]
        self.auth_domain: str = authorizer["domain"]
        self.auth_client_id: str = authorizer["client_id"]
        self.auth_audience: str = authorizer["audience"]

    def login(self) -> AccessToken:
        """
        Execute the Auth0 device code authentication flow by requesting
        a device code session from Auth0, opening the browser for the
        user to authenticate, requesting the access token and exiting
        the flow once compelte.

        Raises:
            typer.Exit: Failed to complete any step during the login
                process such as device code retrieval, session timeout,
                invalid token response; all with non-zero status.

        Returns:
            AccessToken: Auth0 jwt access token.
        """
        # request for a device code from auth0 using a pre-defined env-
        # based authorizer client; fields are defined when setting up
        # the controller.
        with console.status("Requesting device authorization code..."):
            r: httpx.Response = httpx.post(
                url=f"https://{self.auth_domain}/oauth/device/code",
                data={
                    "client_id": self.auth_client_id,
                    "audience": self.auth_audience,
                    "scope": self.access_token_scopes,
                },
            )
        if r.status_code == 200:
            console.print("[success]✓ Device code generated.")
        else:
            console.print("[fail]Failed to generate device code, try again.")
            raise typer.Exit(1)
        int_wait: int = r.json()["interval"]
        usr_code: str = r.json()["user_code"]
        dev_code: str = r.json()["device_code"]
        ping_uri: str = r.json()["verification_uri_complete"]

        # redirect a user to the login page and output where they are
        # going with a short delay with their user code.
        console.print(f"- Navigate to the url on your device: {ping_uri}")
        console.print(f"- Enter the following code: [b]{usr_code}[/]")
        time.sleep(2)
        webbrowser.open_new_tab(ping_uri)

        # iterate for a number of retries until the user has entered the
        # authentication account from the redirect, ping auth0 and check
        # the status of each response to capture any edge cases.
        with console.status("Waiting for device authentication..."):
            for _ in range(self.device_code_retries):
                r = httpx.post(
                    url=f"https://{self.auth_domain}/oauth/token",
                    data={
                        "device_code": dev_code,
                        "audience": self.auth_audience,
                        "client_id": self.auth_client_id,
                        "grant_type": self.device_code_grant_type,
                    },
                )
                if r.status_code == 200:
                    try:
                        access_token: AccessToken = AccessToken.model_validate(r.json())
                        console.print("[success]✓ Authenticated session created.")
                        return access_token
                    except pydantic.ValidationError:
                        console.print("[fail]Authentication failed, try again.")
                        raise typer.Exit(1)

                elif r.status_code == 403:
                    # capture errors from auth0 that describe if the
                    # authentication process is still pending or if it
                    # has expired already.
                    if r.json().get("error", None) == "authorization_pending":
                        pass
                    elif r.json().get("error", None) == "expired_token":
                        console.print("[fail]Authenticated session closed, try again.")
                        raise typer.Exit(1)
                else:
                    console.print("[fail]Authentication failed, try again.")
                    raise typer.Exit(1)
                time.sleep(int_wait)

        # capture when the max retry limit is met during authentication.
        console.print("[fail]Authentication timed out, try again.")
        raise typer.Exit(1)

    def refresh_token(self, refresh_token: str | None) -> AccessToken | None:
        """
        Refresh a given `refresh_token` from Auth0 using the refresh
        authentication grant type and return conditionally depending on
        if the token refresh was successful.

        Args:
            refresh_token (str, optional): Auth0 refresh token.

        Returns:
            AccessToken: Auth0 jwt access token.
        """
        if refresh_token is None:
            return None

        console.print("[warn]! Refreshing authenticated session.")
        with console.status("Refreshing device authentication token..."):
            r: httpx.Response = httpx.post(
                url=f"https://{self.auth_domain}/oauth/token",
                data={
                    "client_id": self.auth_client_id,
                    "audience": self.auth_audience,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            )

        try:
            access_token: AccessToken = AccessToken.model_validate(r.json())
            console.print("[success]✓ Access token refreshed successfully.")
            return access_token
        except Exception:
            console.print("[warn]! Unable to refresh the authenticated session.")
            return None
