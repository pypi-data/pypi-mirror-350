# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["JobListParams"]


class JobListParams(TypedDict, total=False):
    limit: int
    """Page size limit"""

    offset: int
    """Page offset"""

    status: Optional[str]
    """Filter by status"""
