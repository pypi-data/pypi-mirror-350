# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidators:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_complete_signup(self, client: FlowAISDK) -> None:
        validator = client.auth.validators.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_complete_signup(self, client: FlowAISDK) -> None:
        response = client.auth.validators.with_raw_response.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = response.parse()
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_complete_signup(self, client: FlowAISDK) -> None:
        with client.auth.validators.with_streaming_response.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = response.parse()
            assert_matches_type(object, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_verify_access(self, client: FlowAISDK) -> None:
        validator = client.auth.validators.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_verify_access(self, client: FlowAISDK) -> None:
        response = client.auth.validators.with_raw_response.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = response.parse()
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_verify_access(self, client: FlowAISDK) -> None:
        with client.auth.validators.with_streaming_response.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = response.parse()
            assert_matches_type(object, validator, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncValidators:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_complete_signup(self, async_client: AsyncFlowAISDK) -> None:
        validator = await async_client.auth.validators.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_complete_signup(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.auth.validators.with_raw_response.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = await response.parse()
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_complete_signup(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.auth.validators.with_streaming_response.complete_signup(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = await response.parse()
            assert_matches_type(object, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_verify_access(self, async_client: AsyncFlowAISDK) -> None:
        validator = await async_client.auth.validators.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_verify_access(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.auth.validators.with_raw_response.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = await response.parse()
        assert_matches_type(object, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_verify_access(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.auth.validators.with_streaming_response.verify_access(
            unique_url_key="uniqueUrlKey",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = await response.parse()
            assert_matches_type(object, validator, path=["response"])

        assert cast(Any, response.is_closed) is True
