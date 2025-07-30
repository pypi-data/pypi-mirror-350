#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import enum
from datetime import datetime

import pydantic
import pydantic.alias_generators


# string enum used to defined the typing literal for valid batch status
# values and is handled by typer.
class BatchStatus(str, enum.Enum):
    """Batch status enumeration."""

    COMPLETED = "completed"
    FAILED = "failed"
    SUBMITTED = "submitted"
    PROCESSING = "processing"


class DefaultModel(pydantic.BaseModel):
    """
    Default `pydantic` model enforces shared model config like aliasing
    for validation and serialization to be camel-case and reflect the
    output from the api layer; in-code aliasing will be snake-case.
    """

    model_config = pydantic.ConfigDict(
        alias_generator=pydantic.AliasGenerator(
            validation_alias=pydantic.alias_generators.to_camel,
            serialization_alias=pydantic.alias_generators.to_camel,
        )
    )


class Batch(DefaultModel):
    """
    Batch data model with minimal fields and simple defaults to avoid
    future schema breaking changes and allow incomplete data from the
    api layer to be returned.
    """

    batch_id: str
    created_at: datetime
    number_of_jobs: int
    filename: str | None = None


class BatchPage(DefaultModel):
    """
    Paginated container for batches based with added metadata for a
    lookup key offset and a flag for more results in the page response.
    Added model validation will quietly coerce pagination metadata for
    inconsistent paging data.
    """

    data: list[Batch] = pydantic.Field(default_factory=list)
    has_more: bool = False


class BatchJobResult(DefaultModel):
    """
    Batch job screening result nested data model used to show a single
    results for a retrosynthesis job. No default data is used, jobs need
    to return accurate data so stricter validation is user per command.
    """

    job_id: str
    smiles: str
    success: bool
    synthesizable: bool
