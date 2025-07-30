# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .validation_item_feedback_param import ValidationItemFeedbackParam

__all__ = ["ValidationCreateParams"]


class ValidationCreateParams(TypedDict, total=False):
    current_user_payload: Required[object]

    is_accepted: Required[bool]

    test_case_id: Required[str]

    validation_task_id: Required[str]

    validator_task_id: Required[str]

    feedback: Optional[str]

    item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]]
