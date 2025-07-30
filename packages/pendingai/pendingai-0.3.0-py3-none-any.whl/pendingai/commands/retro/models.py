#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime, timezone

import pydantic


class RetrosynthesisEngine(pydantic.BaseModel):
    """
    Retrosynthesis engine data model. Response model for `/engines` in
    the retrosynthesis API layer. Additional default values are given to
    minimise validation errors.
    """

    id: str
    name: str = "unknown"
    default: bool = False
    last_alive: datetime = datetime.now(timezone.utc)


class BuildingBlockLibrary(pydantic.BaseModel):
    """
    Building block library data model. Response model for `/libraries`
    in the retrosynthesis API layer. Additional default values are given
    to minimise validation errors.
    """

    id: str
    name: str = "unknown"
    version: str = "unknown"
