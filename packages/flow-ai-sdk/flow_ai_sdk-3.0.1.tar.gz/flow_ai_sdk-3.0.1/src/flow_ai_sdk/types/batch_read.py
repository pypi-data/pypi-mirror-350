# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel
from .test_case import TestCase

__all__ = ["BatchRead"]


class BatchRead(BaseModel):
    id: str

    completed_test_cases: int

    created_at: datetime

    pipeline_run_id: str

    project_id: str

    total_test_cases: int

    updated_at: datetime

    description: Optional[str] = None

    error: Optional[str] = None

    name: Optional[str] = None

    test_cases: Optional[List[TestCase]] = None
