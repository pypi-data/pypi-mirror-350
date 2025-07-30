# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["BatchRetrieveStatusResponse"]


class BatchRetrieveStatusResponse(BaseModel):
    batch_id: str

    pipeline_run_id: str

    pipeline_run_updated_at: datetime

    status: str

    external_run_id: Optional[str] = None
