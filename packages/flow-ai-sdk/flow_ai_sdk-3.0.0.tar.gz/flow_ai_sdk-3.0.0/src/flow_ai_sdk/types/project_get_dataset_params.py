# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ProjectGetDatasetParams"]


class ProjectGetDatasetParams(TypedDict, total=False):
    version: Optional[str]
    """Optional specific dataset version ID to retrieve.

    If omitted, the latest is returned.
    """
