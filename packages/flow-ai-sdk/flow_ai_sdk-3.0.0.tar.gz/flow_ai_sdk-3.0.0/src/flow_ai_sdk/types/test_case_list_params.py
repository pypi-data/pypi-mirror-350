# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["TestCaseListParams"]


class TestCaseListParams(TypedDict, total=False):
    batch_id: Optional[str]
    """Filter by Batch ID"""

    created_after: Optional[str]
    """Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)"""

    created_before: Optional[str]
    """Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)"""

    limit: int

    name: Optional[str]
    """Filter by name (partial match)"""

    skip: int

    sort_by: Optional[str]
    """Field to sort by (e.g., 'name', 'created_at')"""

    sort_order: str
    """Sort direction ('asc' or 'desc')"""

    status: Optional[str]
    """Filter by status"""
