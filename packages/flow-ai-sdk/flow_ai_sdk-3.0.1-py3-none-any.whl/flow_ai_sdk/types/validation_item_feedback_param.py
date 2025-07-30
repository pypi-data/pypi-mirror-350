# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ValidationItemFeedbackParam"]


class ValidationItemFeedbackParam(TypedDict, total=False):
    item_id: Required[Annotated[str, PropertyInfo(alias="itemId")]]

    feedback: Optional[str]
