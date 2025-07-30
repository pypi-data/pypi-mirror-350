# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .validation_item_feedback_param import ValidationItemFeedbackParam

__all__ = ["ValidationUpdateParams"]


class ValidationUpdateParams(TypedDict, total=False):
    current_user_payload: Required[object]

    feedback: Optional[str]

    is_accepted: Optional[bool]

    item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]]
