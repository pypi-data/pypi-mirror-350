# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .project_validator import ProjectValidator

__all__ = ["ValidatorListResponse"]


class ValidatorListResponse(BaseModel):
    validators: List[ProjectValidator]
