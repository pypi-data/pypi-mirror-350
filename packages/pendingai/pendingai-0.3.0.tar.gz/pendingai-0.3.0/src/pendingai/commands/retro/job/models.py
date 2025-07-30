#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime, timezone

import pydantic


class JobParameters(pydantic.BaseModel):
    """
    Retrosynthesis job parameters data model. Required nested model when
    requesting a job to be submitted or when parsing results given back
    from the api layer attached to a job.
    """

    retrosynthesis_engine: str
    building_block_libraries: list[str]
    number_of_routes: int = 20
    processing_time: int = 300
    reaction_limit: int = 3
    building_block_limit: int = 3


class RouteStep(pydantic.BaseModel):
    """
    Retrosynthesis route step data model. Required nested model in a
    route result for a retrosynthesis job. Expects at least one step to
    be contained in a route.
    """

    reaction_smiles: str
    order: int = 1


class JobRoute(pydantic.BaseModel):
    """
    Retrosynthesis route data model. Nested model in a retrosynthesis
    job denoted as a result from the retrosynthesis engine. Added simple
    extra fields as dictionaries to prevent validation errors.
    """

    summary: str
    building_blocks: list[dict] = pydantic.Field(default_factory=list)
    steps: list[RouteStep] = pydantic.Field(default_factory=list)


class Job(pydantic.BaseModel):
    """
    Retrosynthesis job data model. Contains all relevant metadata for
    each job document and has many default values defined for responses
    to minimise possible validation errors.
    """

    id: str
    query: str
    status: str
    parameters: JobParameters
    created: datetime = datetime.now(timezone.utc)
    updated: datetime = datetime.now(timezone.utc)
    routes: list[JobRoute] = pydantic.Field(default_factory=list)


class JobPage(pydantic.BaseModel):
    """
    Paginated retrosynthesis job results data model. A container model
    to store pagination information and retrosynthesis job results.
    """

    data: list[Job] = pydantic.Field(default_factory=list)
    has_more: bool = False
