# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["APIKeyUpdateResponse"]


class APIKeyUpdateResponse(BaseModel):
    id: str

    created_at: datetime

    is_active: bool

    key_prefix: str

    updated_at: datetime

    user_id: str

    key_name: Optional[str] = None
    """Optional user-friendly name for the key"""

    last_used_at: Optional[datetime] = None
