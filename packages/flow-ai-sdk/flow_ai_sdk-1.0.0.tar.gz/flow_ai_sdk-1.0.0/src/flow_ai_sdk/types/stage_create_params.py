# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from .._types import FileTypes

__all__ = ["StageCreateParams"]


class StageCreateParams(TypedDict, total=False):
    files: Required[List[FileTypes]]

    project_id: Required[str]

    source_type: Required[
        Literal["agent_rules", "tool_definitions", "database_schema_rules", "custom_data_files", "relational_db_schema"]
    ]
