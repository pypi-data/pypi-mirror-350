# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .stage_details import StageDetails

__all__ = ["StageListResponse"]


class StageListResponse(BaseModel):
    limit: int

    skip: int

    stages: List[StageDetails]

    total: int
