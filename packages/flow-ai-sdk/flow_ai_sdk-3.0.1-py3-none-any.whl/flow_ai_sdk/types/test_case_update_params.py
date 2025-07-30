# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["TestCaseUpdateParams", "TestCaseIn"]


class TestCaseUpdateParams(TypedDict, total=False):
    current_user_payload: Required[Dict[str, object]]

    test_case_in: Required[TestCaseIn]
    """Schema for updating a test case (all fields optional)"""


class TestCaseIn(TypedDict, total=False):
    description: Optional[str]

    expected_output: Optional[str]

    is_active: Optional[bool]

    name: Optional[str]

    status: Optional[str]
