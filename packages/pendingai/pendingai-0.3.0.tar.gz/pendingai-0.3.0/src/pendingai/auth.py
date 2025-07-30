#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import typing
from datetime import datetime, timezone

import jwt
import pydantic
import rich
import typer

from pendingai import config

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class AccessToken(pydantic.BaseModel):
    """
    Access token data model storing response fields from oauth2 tokens
    with added refresh and id tokens and an expiry flag. Provide added
    helper methods to extract jwt claims and scopes from the token.
    """

    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str

    def decode_jwt_claims(self) -> dict:
        """
        Extract jwt claims from an oauth2 access token without signature
        verification.

        Raises:
            typer.Exit: Access token is malformed and could not be
                decoded as expected.

        Returns:
            dict: Jwt claims from the access token.
        """
        try:
            return jwt.decode(self.access_token, options={"verify_signature": False})
        except Exception:
            console.print("[fail]Invalid access token found, please re-authenticate.")
            raise typer.Exit(1)

    def is_expired(self) -> bool:
        """
        Flag whether an access token has expired.

        Raises:
            typer.Exit: Access token is missing a required expiry jwt
                claim or another error was encountered.

        Returns:
            bool: Access token has reached its expiry time.
        """
        try:
            tz: timezone = timezone.utc
            expires_at: int = self.decode_jwt_claims()["exp"]
            return datetime.fromtimestamp(expires_at, tz=tz) < datetime.now(tz=tz)
        except Exception:
            console.print("[fail]Invalid access token found, please re-authenticate.")
            raise typer.Exit(1)

    def get_jwt_claim(self, claim: str, default: typing.Any = None) -> typing.Any:
        """
        Retrieve a specific jwt claim from the access token. If the
        access token does not have the claim, check if the custom claim
        equivalent for pending ai exists.

        Args:
            claim (str): Access token jwt claim key.
            default (typing.Any, optional): Default value if missing.

        Returns:
            typing.Any: Access token jwt claim value.
        """
        claims: dict = self.decode_jwt_claims()
        if claim in claims:
            return claims[claim]
        if (claim := f"https://pending.ai/claims/{claim}") in claims:
            return claims[claim]
        return default
