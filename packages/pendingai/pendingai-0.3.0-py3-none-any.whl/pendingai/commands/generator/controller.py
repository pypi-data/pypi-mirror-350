#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import http

import httpx
import rich
import typer

from pendingai import config
from pendingai.api import ApiClient
from pendingai.commands.generator.models import Model
from pendingai.context import Context

console = rich.console.Console(
    theme=config.RICH_CONSOLE_THEME, width=config.CONSOLE_WIDTH, soft_wrap=True
)


class GeneratorController:
    """
    Controller for `pendingai generator` subcommands. Controls specific
    generator operations for captured named commands in the app like
    retrieving models and sampling.

    Args:
        context (Context): App runtime context.
    """

    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.api: ApiClient = ApiClient(
            base_url=config.API_BASE_URLS[self.context.obj.environment],
            subdomain=config.GENERATOR_SUBDOMAIN,
            bearer_token=self.context.obj.cache.access_token,
        )

    def retrieve_models(self) -> list[tuple[Model, str]]:
        """
        Retrieve all generator models resources from the api layer
        and coerce into the expected data model.

        Returns:
            list[tuple[Model, str]]: Generator models.
        """
        # provide a spinner to show the request is being made to get all
        # generator models from the api client.
        models: list[Model] = []
        with console.status("Retrieving models..."):
            pagination_key: str | None = None
            while True:
                try:
                    params: dict = {"limit": 100, "pagination-key": pagination_key}
                    r: httpx.Response = self.api.get("/models", params=params)
                    response_models: list[dict] = r.json().get("data", [])
                    models.extend([Model.model_validate(x) for x in response_models])
                    if not r.json().get("has_more", False):
                        break
                    pagination_key = models[-1].get("id")
                except Exception:
                    break

        statuses: list[str] = []
        for model in models:
            with console.status(f"Retrieving model status for {model.id}..."):
                r = self.api.get(f"/models/{model.id}/status")
                if r.status_code == 200:
                    statuses.append(r.json().get("status", "offline"))
                else:
                    statuses.append("offline")

        return list(zip(models, statuses))

    def generate_sample_by_model(self, model_id: str, samples: int) -> list[str]:
        # generate samples from the generator service from a specific
        # model and set number of samples

        params: dict = {"samples": samples}
        route: str = f"/generate/{model_id}"
        # make post request to api client for the generator model
        # condition and sampling parameters
        r: httpx.Response = self.api.post(route, params=params, skip_errors=True)

        if r.status_code == http.HTTPStatus.OK:
            # client was able to successfully generate a sample of
            # molecule smiles in and returned as a list
            return r.json().get("smiles", [])

        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            # requested model id was not found for the service
            console.stderr = True
            console.print(f"[warn]\n! Model '{model_id}' was not found.")
            raise typer.Exit(1)

        # requested model id was reachable but was unable to be used
        # for generating molecules and was offline
        console.stderr = True
        console.print(f"[warn]\n! Model '{model_id}' was offline.")
        raise typer.Exit(1)

    def generate_sample_by_random(self, samples: int) -> list[str]:
        # generate samples from the generator service from a random
        # model and set number of samples

        params: dict = {"samples": samples}
        route: str = "/generate"
        # make post request to api client for the generator model
        # condition and sampling parameters
        r: httpx.Response = self.api.post(route, params=params, skip_errors=True)

        if r.status_code == http.HTTPStatus.OK:
            # client was able to successfully generate a sample of
            # molecule smiles in and returned as a list
            return r.json().get("smiles", [])

        # all models were offline or timed out and could not sample
        # molecules from the service
        console.stderr = True
        console.print("[warn]\n! All models were offline.")
        raise typer.Exit(1)

    def generate_sample(self, model_id: str | None, samples: int) -> list[str]:
        # route to the correct sampling method depending on the given
        # config options such as the model id
        if model_id is not None:
            return self.generate_sample_by_model(model_id, samples)
        return self.generate_sample_by_random(samples)
