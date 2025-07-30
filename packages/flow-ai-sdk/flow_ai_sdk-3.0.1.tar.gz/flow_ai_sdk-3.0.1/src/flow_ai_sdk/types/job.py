# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Job"]


class Job(BaseModel):
    id: str

    created_at: datetime

    project_id: str

    status: str

    updated_at: datetime

    config: Optional[Dict[str, object]] = None

    end_time: Optional[datetime] = None

    error: Optional[str] = None

    start_time: Optional[datetime] = None
