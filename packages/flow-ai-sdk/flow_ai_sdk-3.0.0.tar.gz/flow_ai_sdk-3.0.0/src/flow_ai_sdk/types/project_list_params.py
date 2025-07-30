# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ProjectListParams"]


class ProjectListParams(TypedDict, total=False):
    limit: int
    """Maximum number of projects to return."""

    offset: int
    """Number of projects to skip for pagination."""

    status: Optional[str]
    """Filter projects by status: 'active', 'all', 'archived'."""
