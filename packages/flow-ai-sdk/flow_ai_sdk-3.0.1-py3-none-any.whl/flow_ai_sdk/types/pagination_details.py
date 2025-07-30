# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["PaginationDetails"]


class PaginationDetails(BaseModel):
    limit: int
    """The limit for the number of projects returned per page."""

    offset: int
    """The offset for pagination."""

    total_count: int
    """Total number of projects matching the filter."""
