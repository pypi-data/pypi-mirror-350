# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["APIKeyListResponse", "APIKey", "Pagination"]


class APIKey(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    key_name: str = FieldInfo(alias="keyName")

    last_used_at: Optional[datetime] = FieldInfo(alias="lastUsedAt", default=None)


class Pagination(BaseModel):
    limit: int

    offset: int

    total_count: int = FieldInfo(alias="totalCount")


class APIKeyListResponse(BaseModel):
    api_keys: List[APIKey] = FieldInfo(alias="apiKeys")

    pagination: Pagination
