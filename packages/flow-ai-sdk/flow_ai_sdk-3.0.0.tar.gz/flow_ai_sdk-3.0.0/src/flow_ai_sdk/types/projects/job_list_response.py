# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..job import Job
from ..._models import BaseModel
from ..pagination_details import PaginationDetails

__all__ = ["JobListResponse"]


class JobListResponse(BaseModel):
    jobs: List[Job]

    pagination: PaginationDetails
