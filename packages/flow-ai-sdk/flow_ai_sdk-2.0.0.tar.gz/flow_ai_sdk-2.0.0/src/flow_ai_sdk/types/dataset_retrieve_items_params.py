# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DatasetRetrieveItemsParams"]


class DatasetRetrieveItemsParams(TypedDict, total=False):
    limit: int
    """Maximum number of dataset items to return."""

    offset: int
    """Number of dataset items to skip for pagination."""
