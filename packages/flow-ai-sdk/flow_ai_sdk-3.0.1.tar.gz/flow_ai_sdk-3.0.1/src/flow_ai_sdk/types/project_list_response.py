# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .project import Project
from .._models import BaseModel
from .pagination_details import PaginationDetails

__all__ = ["ProjectListResponse"]


class ProjectListResponse(BaseModel):
    pagination: PaginationDetails

    projects: List[Project]
