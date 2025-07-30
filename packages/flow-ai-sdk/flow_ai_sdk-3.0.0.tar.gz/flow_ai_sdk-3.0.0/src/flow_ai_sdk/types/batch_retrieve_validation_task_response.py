# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from .._models import BaseModel

__all__ = ["BatchRetrieveValidationTaskResponse", "Validator"]


class Validator(BaseModel):
    clerk_user_id: str

    status: str

    url: str

    validator_id: str

    validator_task_id: str


class BatchRetrieveValidationTaskResponse(BaseModel):
    id: str

    batch_id: str

    created_at: datetime

    status: str

    updated_at: datetime

    validators: List[Validator]
