# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["StageUpdateParams"]


class StageUpdateParams(TypedDict, total=False):
    original_filename: Optional[str]
    """New original filename for the stage."""
