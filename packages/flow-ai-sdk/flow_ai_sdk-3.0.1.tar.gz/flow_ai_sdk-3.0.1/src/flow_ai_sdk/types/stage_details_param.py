# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["StageDetailsParam"]


class StageDetailsParam(TypedDict, total=False):
    id: Required[str]

    project_id: Required[str]

    s3_path: Required[str]

    source_type: Required[str]

    original_filename: Optional[str]
