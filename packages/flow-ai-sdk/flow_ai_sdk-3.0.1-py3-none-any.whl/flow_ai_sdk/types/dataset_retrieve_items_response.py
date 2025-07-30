# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from datetime import datetime

from .._models import BaseModel
from .pagination_details import PaginationDetails

__all__ = ["DatasetRetrieveItemsResponse", "Item"]


class Item(BaseModel):
    id: str

    created_at: datetime

    dataset_id: str

    item_data: Dict[str, object]

    updated_at: datetime


class DatasetRetrieveItemsResponse(BaseModel):
    items: List[Item]

    pagination: PaginationDetails
