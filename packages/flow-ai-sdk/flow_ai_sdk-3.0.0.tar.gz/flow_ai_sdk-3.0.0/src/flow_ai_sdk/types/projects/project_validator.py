# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ProjectValidator"]


class ProjectValidator(BaseModel):
    id: str
    """The ID of the validator record (project-specific assignment)."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of assignment creation."""

    email: str
    """Email address of the validator."""

    project_id: str = FieldInfo(alias="projectId")
    """The ID of the project."""

    clerk_user_id: Optional[str] = FieldInfo(alias="clerkUserId", default=None)
    """Clerk User ID if user exists, otherwise null."""
