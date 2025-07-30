# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidatorTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_test_cases(self, client: FlowAISDK) -> None:
        validator_task = client.validator_tasks.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_test_cases(self, client: FlowAISDK) -> None:
        response = client.validator_tasks.with_raw_response.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator_task = response.parse()
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_test_cases(self, client: FlowAISDK) -> None:
        with client.validator_tasks.with_streaming_response.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator_task = response.parse()
            assert_matches_type(object, validator_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_test_cases(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_task_id` but received ''"):
            client.validator_tasks.with_raw_response.list_test_cases(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_submit(self, client: FlowAISDK) -> None:
        validator_task = client.validator_tasks.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_submit(self, client: FlowAISDK) -> None:
        response = client.validator_tasks.with_raw_response.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator_task = response.parse()
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_submit(self, client: FlowAISDK) -> None:
        with client.validator_tasks.with_streaming_response.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator_task = response.parse()
            assert_matches_type(object, validator_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_submit(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_task_id` but received ''"):
            client.validator_tasks.with_raw_response.submit(
                "",
            )


class TestAsyncValidatorTasks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_test_cases(self, async_client: AsyncFlowAISDK) -> None:
        validator_task = await async_client.validator_tasks.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_test_cases(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validator_tasks.with_raw_response.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator_task = await response.parse()
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_test_cases(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validator_tasks.with_streaming_response.list_test_cases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator_task = await response.parse()
            assert_matches_type(object, validator_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_test_cases(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_task_id` but received ''"):
            await async_client.validator_tasks.with_raw_response.list_test_cases(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit(self, async_client: AsyncFlowAISDK) -> None:
        validator_task = await async_client.validator_tasks.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_submit(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validator_tasks.with_raw_response.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator_task = await response.parse()
        assert_matches_type(object, validator_task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_submit(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validator_tasks.with_streaming_response.submit(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator_task = await response.parse()
            assert_matches_type(object, validator_task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_submit(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_task_id` but received ''"):
            await async_client.validator_tasks.with_raw_response.submit(
                "",
            )
