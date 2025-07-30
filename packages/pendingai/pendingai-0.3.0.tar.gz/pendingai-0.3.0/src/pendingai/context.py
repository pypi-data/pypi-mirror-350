#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import json
import pathlib

import pydantic
import typer

from pendingai import Environment, config
from pendingai.auth import AccessToken


class CacheContent(pydantic.BaseModel):
    """
    Cache content class used for loading in a json data file from the
    application directory. Provide utilities to overwrite and delete
    cache file contents.

    Args:
        environment (Environment): App runtime environment option.
    """

    access_token: AccessToken | None = None

    @staticmethod
    def _get_filepath(environment: Environment) -> pathlib.Path:
        """
        Get a cache filepath based on the runtime context environment
        and application directory config value.

        Args:
            environment (Environment): App runtime environment option.

        Returns:
            pathlib.Path: Environment-specific cache filepath.
        """
        return config.APPLICATION_DIRECTORY / f".{environment.value}.cache"

    def __init__(self, *, environment: Environment) -> None:
        # initialise the unique class instance only if the cache file
        # exists with valid data; otherwise create an empty cache value.
        cache_filepath: pathlib.Path = self._get_filepath(environment)
        if cache_filepath.exists() and cache_filepath.is_file():
            try:
                contents: dict = json.loads(cache_filepath.read_text())
                super().__init__(**contents)
                return
            except (json.JSONDecodeError, pydantic.ValidationError):
                cache_filepath.unlink(missing_ok=True)
        super().__init__()

    def update_cache_file(self, environment: Environment) -> None:
        """
        Update a cache file for the application based on the runtime
        environment in the app context.

        Args:
            environment (Environment): App runtime environment option.
        """
        cache_filepath: pathlib.Path = self._get_filepath(environment)
        json.dump(self.model_dump(), cache_filepath.open("w"))

    def delete_cache_file(self, environment: Environment) -> None:
        """
        Delete a cache file for the application based on the runtime
        environment in the app context.

        Args:
            environment (Environment): App runtime environment option.
        """
        cache_filepath: pathlib.Path = self._get_filepath(environment)
        cache_filepath.unlink(missing_ok=True)


class ContextContent(pydantic.BaseModel):
    """
    Context object attached to the `click.Context.obj` attribute for
    access across different application components such as callbacks and
    command routines.

    Args:
        environment (Environment): App runtime environment option.
    """

    environment: Environment
    cache: CacheContent

    def __init__(self, environment: Environment, **kwargs) -> None:
        super().__init__(
            environment=environment,
            cache=CacheContent(environment=environment),
            **kwargs,
        )

    def update_cache(self) -> None:
        """
        Update a cache file for the application based on the runtime
        environment in the app context.
        """
        self.cache.update_cache_file(self.environment)

    def delete_cache(self) -> None:
        """
        Delete a cache file for the application based on the runtime
        environment in the app context.
        """
        self.cache.delete_cache_file(self.environment)


class Context(typer.Context):
    """
    Helper class for type annotating and supporting mypy type correction
    by overloading the arbitrary `obj` of `click.Context` with the pre-
    initialised `ContextContent` class defined above.
    """

    obj: ContextContent
