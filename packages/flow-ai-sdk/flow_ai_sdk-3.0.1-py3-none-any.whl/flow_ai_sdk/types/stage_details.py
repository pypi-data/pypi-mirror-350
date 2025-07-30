# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["StageDetails"]


class StageDetails(BaseModel):
    id: str

    project_id: str

    s3_path: str

    source_type: str

    original_filename: Optional[str] = None
