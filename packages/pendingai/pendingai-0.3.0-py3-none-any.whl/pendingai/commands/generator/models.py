#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pydantic


class Model(pydantic.BaseModel):
    id: str
    name: str | None = None
    desc: str | None = None
    version: str | None = None
    summary: dict = {}
    metadata: dict = {}
