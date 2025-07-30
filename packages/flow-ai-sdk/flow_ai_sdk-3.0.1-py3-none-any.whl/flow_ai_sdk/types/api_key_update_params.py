# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["APIKeyUpdateParams"]


class APIKeyUpdateParams(TypedDict, total=False):
    is_active: Optional[bool]

    key_name: Optional[str]
    """Optional user-friendly name for the key"""
