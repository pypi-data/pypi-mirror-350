# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from .._models import BaseModel

__all__ = ["BatchCreateValidationTaskResponse", "ValidatorURL"]


class ValidatorURL(BaseModel):
    clerk_user_id: str

    url: str

    validator_id: str


class BatchCreateValidationTaskResponse(BaseModel):
    batch_id: str

    created_at: datetime

    status: str

    validation_task_id: str

    validator_urls: List[ValidatorURL]
