# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TestCase", "Trajectory", "TrajectoryMessage", "TrajectoryToolCall", "TrajectoryToolCallToolOutput"]


class TrajectoryMessage(BaseModel):
    id: str

    created_at: datetime

    role: str

    updated_at: datetime

    content: Optional[str] = None

    trajectory_item_id: Optional[str] = None


class TrajectoryToolCallToolOutput(BaseModel):
    id: str

    created_at: datetime

    output: Dict[str, object]

    tool_call_id: str

    updated_at: datetime


class TrajectoryToolCall(BaseModel):
    id: str

    arguments: Dict[str, object]

    created_at: datetime

    tool_name: str

    updated_at: datetime

    tool_output: Optional[TrajectoryToolCallToolOutput] = None

    trajectory_item_id: Optional[str] = None


class Trajectory(BaseModel):
    id: str

    created_at: datetime

    item_type: Literal["message", "tool_call", "unknown"]
    """Derives the type of the trajectory item."""

    order: int

    test_case_id: str

    updated_at: datetime

    message: Optional[TrajectoryMessage] = None

    tool_call: Optional[TrajectoryToolCall] = None


class TestCase(BaseModel):
    __test__ = False
    id: str

    created_at: datetime

    expected_output: str

    status: str

    updated_at: datetime

    user_id: str

    description: Optional[str] = None

    is_active: Optional[bool] = None

    name: Optional[str] = None

    trajectory: Optional[List[Trajectory]] = None

    validation_criteria: Optional[List[str]] = None
