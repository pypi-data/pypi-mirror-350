# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["UserRead"]


class UserRead(BaseModel):
    id: str

    created_at: datetime

    updated_at: datetime

    clerk_id: Optional[str] = None

    email: Optional[str] = None

    first_name: Optional[str] = None

    image_url: Optional[str] = None

    is_active: Optional[bool] = None

    last_name: Optional[str] = None

    org_id: Optional[str] = None

    username: Optional[str] = None
