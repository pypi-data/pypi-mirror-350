# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .stage_details_param import StageDetailsParam

__all__ = ["JobTriggerPipelineParams"]


class JobTriggerPipelineParams(TypedDict, total=False):
    project_id: Required[str]

    body: Required[Iterable[StageDetailsParam]]
