# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["ProjectGetDatasetResponse"]


class ProjectGetDatasetResponse(BaseModel):
    id: str

    created_at: datetime

    job_id: str

    name: str

    pipeline_run_id: str

    updated_at: datetime

    description: Optional[str] = None
