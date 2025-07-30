# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ValidationListParams"]


class ValidationListParams(TypedDict, total=False):
    current_user_payload: Required[object]

    created_after: Optional[str]
    """Filter by creation date (ISO format)"""

    created_before: Optional[str]
    """Filter by creation date (ISO format)"""

    is_accepted: Optional[bool]
    """Filter by acceptance status"""

    limit: int

    skip: int

    sort_by: Optional[str]
    """Field to sort by"""

    sort_order: str
    """Sort direction (asc or desc)"""

    test_case_id: Optional[str]
    """Filter by test case ID"""

    validator_id: Optional[str]
    """Filter by validator user ID"""
