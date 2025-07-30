# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["ValidationTaskRetrieveResponse"]


class ValidationTaskRetrieveResponse(BaseModel):
    id: str

    batch_id: str

    created_at: datetime

    status: str

    updated_at: datetime
