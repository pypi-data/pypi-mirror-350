# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import GetInfoResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_info(self, client: FlowAISDK) -> None:
        client_ = client.get_info()
        assert_matches_type(GetInfoResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_info(self, client: FlowAISDK) -> None:
        response = client.with_raw_response.get_info()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(GetInfoResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_info(self, client: FlowAISDK) -> None:
        with client.with_streaming_response.get_info() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(GetInfoResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_info(self, async_client: AsyncFlowAISDK) -> None:
        client = await async_client.get_info()
        assert_matches_type(GetInfoResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_info(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.with_raw_response.get_info()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(GetInfoResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_info(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.with_streaming_response.get_info() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(GetInfoResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True
