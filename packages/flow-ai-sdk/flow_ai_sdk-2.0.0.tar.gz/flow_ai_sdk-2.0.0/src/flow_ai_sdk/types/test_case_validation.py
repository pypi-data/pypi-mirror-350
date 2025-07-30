# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["TestCaseValidation", "ItemFeedback"]


class ItemFeedback(BaseModel):
    id: str

    created_at: datetime

    feedback_text: str

    test_case_validation_id: str

    trajectory_item_id: str

    updated_at: datetime


class TestCaseValidation(BaseModel):
    __test__ = False
    id: str

    created_at: datetime

    is_accepted: bool

    test_case_id: str

    updated_at: datetime

    validation_task_id: str

    validator_task_id: str

    validator_user_id: str

    feedback: Optional[str] = None

    item_feedbacks: Optional[List[ItemFeedback]] = None
