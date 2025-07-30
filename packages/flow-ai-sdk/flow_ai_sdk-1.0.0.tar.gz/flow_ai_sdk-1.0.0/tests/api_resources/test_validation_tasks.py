# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import ValidationTaskRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidationTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        validation_task = client.validation_tasks.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.validation_tasks.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation_task = response.parse()
        assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.validation_tasks.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation_task = response.parse()
            assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_task_id` but received ''"):
            client.validation_tasks.with_raw_response.retrieve(
                "",
            )


class TestAsyncValidationTasks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        validation_task = await async_client.validation_tasks.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validation_tasks.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation_task = await response.parse()
        assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validation_tasks.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation_task = await response.parse()
            assert_matches_type(ValidationTaskRetrieveResponse, validation_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_task_id` but received ''"):
            await async_client.validation_tasks.with_raw_response.retrieve(
                "",
            )
