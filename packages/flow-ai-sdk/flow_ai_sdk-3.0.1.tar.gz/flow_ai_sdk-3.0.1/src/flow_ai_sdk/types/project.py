# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Project"]


class Project(BaseModel):
    id: str

    created_at: datetime

    is_active: bool

    name: str
    """Name of the project."""

    updated_at: datetime

    user_id: str

    description: Optional[str] = None
    """Description of the project."""
