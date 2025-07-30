# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ValidatorCompleteSignupParams"]


class ValidatorCompleteSignupParams(TypedDict, total=False):
    unique_url_key: Required[Annotated[str, PropertyInfo(alias="uniqueUrlKey")]]

    validation_task_id: Required[Annotated[str, PropertyInfo(alias="validationTaskId")]]

    validator_id: Required[Annotated[str, PropertyInfo(alias="validatorId")]]
