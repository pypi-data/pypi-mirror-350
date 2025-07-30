# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .test_case_validation import TestCaseValidation

__all__ = ["ValidationListResponse"]


class ValidationListResponse(BaseModel):
    has_more: bool

    items: List[TestCaseValidation]

    page: int

    pages: int

    total: int
