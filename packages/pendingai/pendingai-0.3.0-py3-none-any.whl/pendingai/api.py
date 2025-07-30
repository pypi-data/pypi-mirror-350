#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import http
import typing
import urllib.parse

import httpx
import rich
import typer

from pendingai import config
from pendingai.auth import AccessToken

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class ApiClient(httpx.Client):
    """
    API client using the `httpx` package to instantiate a prefixed url
    request handler to capture known exceptions at runtime.

    Args:
        base_url (str, optional): API client base url for prefixing all
            requests for the given domain.
        subdomain (str, optional): Added subdomain to the prefix, used
            when routing against different host names in the base url.
        bearer_token (AccessToken, optional): Authorization header
            bearer token optionally used to make all requests with auth.
    """

    def __init__(
        self,
        base_url: str = "",
        subdomain: str = "",
        bearer_token: AccessToken | None = None,
        **kwargs: typing.Any,
    ) -> None:
        # build default headers for requests with the added bearer
        # token header if it is provided for authentication, otherwise
        # leave empty.
        headers: dict[str, str] = {}
        if bearer_token is not None:
            headers["Authorization"] = "Bearer " + bearer_token.access_token

        # build a httpx client normally with the added base url and
        # headers with an extra timeout value to capture long-hanging
        # requests at runtime.
        super().__init__(
            headers=headers,
            base_url=urllib.parse.urljoin(base_url, subdomain),
            timeout=config.HTTPX_TIMEOUT_SECONDS,
            **kwargs,
        )

    def check_aliveness(self) -> bool:
        """
        Request `/alive` and check the client responds with `200 OK`.

        Returns:
            bool: Aliveness endpoint responds with `200 OK`.
        """
        with console.status("Checking service is available..."):
            return super().request("GET", "/alive").status_code == 200

    def check_authorization(self) -> bool:
        """
        Request `/alive` and check the client responds with a status
        that indicates authorized access i.e., not `401 UNAUTHORIZED`
        or `403 FORBIDDEN`.

        Returns:
            bool: Aliveness endpoint responds with authorized status.
        """
        with console.status("Checking session information..."):
            return super().request("GET", "/alive").status_code not in [401, 403]

    def request(
        self,
        *args: typing.Any,
        skip_errors: bool = False,
        **kwargs: typing.Any,
    ) -> httpx.Response:
        """
        Overload the request method which is routed through by all extra
        `httpx` request http method wrapper functions. Capture known
        exceptions from `httpx` and common http status code errors.

        Args:
            skip_errors (bool, optional): Skip handling known status
                code errors, requires code to catch them individually.

        Raises:
            typer.Exit: Request failed with a known or unexpected API
                status code error.

        Returns:
            httpx.Response: API response.
        """
        try:
            # make the request with the client and either skip error
            # handling for known status codes, or capture specific codes
            # with known errors for the client.
            response: httpx.Response = super().request(*args, **kwargs)
            if skip_errors:
                return response

            if response.status_code == http.HTTPStatus.UNAUTHORIZED:
                console.print(
                    "[fail]Unauthorized access, try re-authenticating with "
                    "[code]pendingai auth refresh[/] or contact support."
                )
            elif response.status_code == http.HTTPStatus.FORBIDDEN:
                if "customer_not_subscribed" in response.content.decode():
                    console.print(
                        "[fail]You are not subscribed to this service, "
                        "contact support to sign up now.",
                    )
                else:
                    console.print(
                        "[fail]Access denied to the service, try re-authenticating with "
                        "[code]pendingai auth refresh[/] or contact support."
                    )
            elif response.status_code == http.HTTPStatus.NOT_FOUND:
                console.print(
                    "[fail]Server resource not found or is unavailable, see "
                    "[code]pendingai docs[/] for more information.",
                )
            elif response.status_code == http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
                console.print(
                    "[fail]Payload is too large, reduce the size of your "
                    "request or contact support."
                )
            elif response.status_code == http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
                console.print(
                    "[fail]Server received an unsupported media type, see "
                    "[code]pendingai docs[/] for more information or contact support.",
                )
            elif response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
                console.print(
                    "[fail]Server has received too many requests, please "
                    "wait shortly before trying again.",
                )
            elif response.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
                console.print(
                    "[fail]Server error encountered, please try again shortly "
                    "or contact support.",
                )
            elif response.status_code == http.HTTPStatus.GATEWAY_TIMEOUT:
                console.print(
                    "[fail]Server timed out, please try again shortly or "
                    "see [code]pendingai docs[/] for more information.",
                )
            elif response.status_code == http.HTTPStatus.REQUEST_TIMEOUT:
                console.print(
                    "[fail]Request timed out, please try again shortly or "
                    "see [code]pendingai docs[/] for more information.",
                )
            elif response.status_code >= 400:
                console.print(
                    "[fail]Unexpected error encountered, please try again shortly or "
                    "contact support if the error continues.",
                )
            else:
                return response

        # handle extra exceptions at the client layer such as the added
        # timeout, connection errors or general runtime errors that
        # occur unexpectedly.
        except httpx.ConnectError:
            console.print("[fail]Unable to connect to Pending AI, try again shortly.")
        except (httpx.ConnectTimeout, httpx.ReadTimeout):
            console.print("[fail]Request to Pending AI timed out, try again shortly.")
        except Exception:
            console.print("[fail]Request failed, try again shortly or contact support.")

        # assumedly exited already with the httpx response, exit with a
        # non-zero status from the app runtime.
        raise typer.Exit(1)

    def get(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.get` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.post` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("POST", *args, **kwargs)

    def delete(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.delete` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("DELETE", *args, **kwargs)

    def put(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.put` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("PUT", *args, **kwargs)

    def options(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.options` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("OPTIONS", *args, **kwargs)

    def patch(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.patch` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("PATCH", *args, **kwargs)

    def head(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.head` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("HEAD", *args, **kwargs)

    def trace(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.trace` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("TRACE", *args, **kwargs)

    def connect(self, *args, **kwargs) -> httpx.Response:
        """
        Overload `httpx.Client.connect` command to allow for adding
        additional parameters to the main `request` method.

        Returns:
            httpx.Response: Process `httpx.Client` request.
        """
        return self.request("CONNECT", *args, **kwargs)
