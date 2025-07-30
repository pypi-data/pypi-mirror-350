# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .stage_details import StageDetails

__all__ = ["StageCreateResponse"]

StageCreateResponse: TypeAlias = List[StageDetails]
