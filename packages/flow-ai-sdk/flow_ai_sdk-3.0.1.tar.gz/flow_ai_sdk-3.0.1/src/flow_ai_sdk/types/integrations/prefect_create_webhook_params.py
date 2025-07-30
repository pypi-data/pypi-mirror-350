# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PrefectCreateWebhookParams", "FlowRun"]


class PrefectCreateWebhookParams(TypedDict, total=False):
    flow_run: Required[FlowRun]

    queue_name: Optional[str]


class FlowRun(TypedDict, total=False):
    prefect_flow_run_id: Required[str]

    prefect_flow_run_name: Optional[str]

    state_message: Optional[str]

    state_timestamp: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    state_type: Optional[str]
